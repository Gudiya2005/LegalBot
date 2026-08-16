from fastapi import APIRouter, UploadFile, File, HTTPException

import tempfile
import os

from faster_whisper import WhisperModel


router = APIRouter(
    prefix="/voice",
    tags=["voice"]
)


# -----------------------------------------
# LOAD WHISPER MODEL
# -----------------------------------------

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


# -----------------------------------------
# TRANSCRIBE AUDIO
# -----------------------------------------

@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...)
):

    temp_path = None

    try:

        # ---------------------------------
        # Validate uploaded audio
        # ---------------------------------

        content = await audio.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="No audio was received."
            )

        # Ignore extremely small recordings
        # because they are usually empty/silence.
        if len(content) < 1000:
            raise HTTPException(
                status_code=400,
                detail="Audio recording is too short."
            )


        # ---------------------------------
        # Determine file extension
        # ---------------------------------

        filename = audio.filename or "recording.webm"

        suffix = os.path.splitext(filename)[1]

        if not suffix:
            suffix = ".webm"


        # ---------------------------------
        # Save temporary audio file
        # ---------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_path = temp_file.name

            temp_file.write(content)


        print(
            f"LegalBot: Received audio "
            f"({len(content)} bytes, {suffix})"
        )


        # ---------------------------------
        # Whisper transcription
        # ---------------------------------

        segments, info = model.transcribe(
            temp_path,
            task="transcribe",
            beam_size=5,
            temperature=0,
            condition_on_previous_text=False,
            initial_prompt=(
                "LegalBot cyber crime assistant. "
                "The speaker may use English, Hindi, or Hinglish. "
                "Preserve the spoken language. "
                "Common terms include Instagram, account, hacked, "
                "cyber crime, scam, phishing, UPI, OTP, password, "
                "bank account, Truecaller, fraud, money, transaction."
            ),
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 500
            }
        )


        # ---------------------------------
        # Collect transcript
        # ---------------------------------

        transcript_parts = []

        for segment in segments:

            text = segment.text.strip()

            if text:
                transcript_parts.append(text)


        text = " ".join(
            transcript_parts
        ).strip()


        print(
            "LegalBot: Whisper result:",
            repr(text)
        )

        print(
            "LegalBot: Detected language:",
            info.language
        )


        # ---------------------------------
        # Empty result
        # ---------------------------------

        if not text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not understand the audio. "
                    "Please speak clearly and try again."
                )
            )


        # ---------------------------------
        # SUCCESS
        # ---------------------------------

        return {
            "text": text,
            "language": info.language
        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            "Whisper transcription error:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to transcribe audio."
        )


    finally:

        # ---------------------------------
        # Delete temporary file
        # ---------------------------------

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            try:

                os.remove(temp_path)

            except Exception:
                pass