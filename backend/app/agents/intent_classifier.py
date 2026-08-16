def classify_intent(message: str) -> str:

    message = message.lower().strip()

    # =====================================================
    # 1. SOCIAL MEDIA / ACCOUNT HACKING
    # =====================================================

    if any(word in message for word in [
        "instagram",
        "facebook",
        "whatsapp",
        "twitter",
        "telegram",
        "snapchat",
        "social media",
        "account hacked",
        "account was hacked",
        "account has been hacked",
        "my account got hacked",
        "social account hacked",
        "email account hacked",
    ]):
        return "social_media_hacking"


    # =====================================================
    # 2. UPI / PAYMENT FRAUD
    # =====================================================

    if any(word in message for word in [
        "upi",
        "gpay",
        "google pay",
        "phonepe",
        "paytm",
        "upi fraud",
        "unauthorized upi",
        "upi transaction",
    ]):
        return "upi_fraud"


    # =====================================================
    # 3. OTP FRAUD
    # =====================================================

    if any(word in message for word in [
        "otp",
        "one time password",
        "verification code",
        "verification otp",
    ]):
        return "otp_fraud"


    # =====================================================
    # 4. PHISHING
    # =====================================================

    if any(word in message for word in [
        "phishing",
        "phishing link",
        "fake link",
        "suspicious link",
        "fake website",
        "fake login page",
        "phishing email",
        "phishing message",
    ]):
        return "phishing"


    # =====================================================
    # 5. FAKE LOAN APP
    # =====================================================

    if any(word in message for word in [
        "loan app",
        "fake loan",
        "fraudulent loan",
        "loan scam",
        "loan fraud",
    ]):
        return "fake_loan_app"


    # =====================================================
    # 6. DIGITAL ARREST
    # =====================================================
    # Keep this intentionally specific.
    # Words like "police" or "officer" alone should NOT
    # classify something as digital arrest.

    if any(word in message for word in [
        "digital arrest",
        "digital arrest scam",
        "online arrest",
        "fake police call",
        "fake police officer",
        "video call arrest",
        "arrest me on video call",
        "threatened with arrest",
        "threatened to arrest",
        "asked me to stay on video call",
        "cbi officer scam",
        "ed officer scam",
        "cyber crime officer scam",
    ]):
        return "digital_arrest"


    # =====================================================
    # 7. IDENTITY THEFT
    # =====================================================

    if any(word in message for word in [
        "identity theft",
        "identity stolen",
        "someone is using my identity",
        "aadhaar misuse",
        "aadhaar fraud",
        "pan card misuse",
        "pan misuse",
        "identity fraud",
    ]):
        return "identity_theft"


    # =====================================================
    # 8. GENERAL
    # =====================================================

    return "general"