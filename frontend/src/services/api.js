const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/* =========================
   REGISTER
========================= */

export async function registerUser(name, email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      name,
      email,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Registration failed."
    );
  }

  return data;
}


/* =========================
   LOGIN
========================= */

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      email,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Invalid email or password."
    );
  }

  return data;
}


/* =========================
   SEND CHAT MESSAGE
========================= */

export async function sendMessage(
  message,
  token,
  conversationId,
  tool = "main"
) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  if (!conversationId) {
    throw new Error("Conversation ID is missing.");
  }

  const response = await fetch(`${API_BASE_URL}/chat/`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },

    body: JSON.stringify({
      message: message,
      conversation_id: conversationId,
      tool: tool,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    let errorMessage = "Unable to process your request.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    } else if (Array.isArray(data.detail)) {
      errorMessage = data.detail
        .map((error) => {
          if (typeof error === "string") {
            return error;
          }

          return error.msg || "Invalid request.";
        })
        .join(", ");
    } else if (data.message) {
      errorMessage = data.message;
    }

    throw new Error(errorMessage);
  }

  return data;
}

/* =========================
   COMPLAINT AGENT
========================= */

export async function sendComplaintMessage(
  message,
  token,
  history = []
) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  const response = await fetch(
    `${API_BASE_URL}/complaint/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({
        message: message,
        history: history,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    let errorMessage = "Unable to process complaint request.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    } else if (Array.isArray(data.detail)) {
      errorMessage = data.detail
        .map((error) =>
          typeof error === "string"
            ? error
            : error.msg || "Invalid request."
        )
        .join(", ");
    }

    throw new Error(errorMessage);
  }

  return data;
}

/* =========================
   EMERGENCY AGENT
========================= */

export async function sendEmergencyMessage(
  message,
  token,
  history = []
) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  const response = await fetch(
    `${API_BASE_URL}/emergency/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({
        message,
        history,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    let errorMessage = "Unable to process emergency request.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    } else if (Array.isArray(data.detail)) {
      errorMessage = data.detail
        .map((error) =>
          typeof error === "string"
            ? error
            : error.msg || "Invalid request."
        )
        .join(", ");
    }

    throw new Error(errorMessage);
  }

  return data;
}

/* =========================
   EVIDENCE AGENT
========================= */

export async function sendEvidenceMessage(
  message,
  token,
  history = []
) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  const response = await fetch(
    `${API_BASE_URL}/evidence/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        message,
        history,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to process evidence request."
    );
  }

  return data;
}

/* =========================
   CHAT HISTORY
========================= */

export async function getChatHistory(token) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  const response = await fetch(
    `${API_BASE_URL}/chat/history`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to load chat history."
    );
  }

  return data;
}


/* =========================
   LOAD ONE CONVERSATION
========================= */

export async function getConversationHistory(
  conversationId,
  token
) {
  if (!token) {
    throw new Error("You are not logged in.");
  }

  if (!conversationId) {
    throw new Error("Conversation ID is missing.");
  }

  const response = await fetch(
    `${API_BASE_URL}/chat/history/${conversationId}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to load conversation."
    );
  }

  return data;
}

/* =========================
   WHISPER VOICE TRANSCRIPTION
========================= */

export async function transcribeVoice(
  audioBlob,
  token
) {

  if (!token) {
    throw new Error("You are not logged in.");
  }

  const formData = new FormData();

  formData.append(
    "audio",
    audioBlob,
    "voice.webm"
  );


  const response = await fetch(
    `${API_BASE_URL}/voice/transcribe`,
    {
      method: "POST",

      headers: {
        Authorization: `Bearer ${token}`,
      },

      body: formData,
    }
  );


  const data = await response.json();


  if (!response.ok) {

    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Unable to transcribe voice."
    );

  }


  return data;
}
