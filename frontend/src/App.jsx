import Login from "./components/Login";
import Register from "./components/Register";

import { useEffect, useRef, useState } from "react";

import {
  sendMessage,
  getChatHistory,
  getConversationHistory,
  transcribeVoice
} from "./services/api";

import {
  ShieldCheck,
  Bot,
  Plus,
  MessageSquare,
  FileText,
  AlertTriangle,
  Search,
  Settings,
  LogOut,
  Send,
  Mic,
  ChevronDown,
  ChevronRight,
  User,
  Bell,
  Palette,
  LockKeyhole,
  Info,
  X,
  Check,
  Eye,
  EyeOff,
  Camera,
  Trash2,
} from "lucide-react";

import "./App.css";


function App() {

  /* =========================
     AUTHENTICATION
  ========================= */

  const [token, setToken] = useState(
    localStorage.getItem("token")
  );

  const [authPage, setAuthPage] = useState("login");

  const [currentUser, setCurrentUser] = useState({
    email: "",
    password: "",
  });


  /* =========================
     USER / SETTINGS
  ========================= */

  const [profile, setProfile] = useState({
    name: "",
    email: "",
  });

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settingsSection, setSettingsSection] = useState("profile");

  const [profileName, setProfileName] = useState("");

  const [profilePhoto, setProfilePhoto] = useState("");

  const [profileSaving, setProfileSaving] = useState(false);
  const [profileMessage, setProfileMessage] = useState("");

  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });

  const [passwordSaving, setPasswordSaving] = useState(false);

  const [passwordVisibility, setPasswordVisibility] = useState({
    current_password: false,
    new_password: false,
    confirm_password: false,
  });

  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("legalbot_theme") === "dark"
  );

  const [language, setLanguage] = useState(
    localStorage.getItem("legalbot_language") || "English"
  );


  /* =========================
     LOAD USER PROFILE
  ========================= */

  const loadProfile = async (authToken) => {

    if (!authToken) {
      return;
    }

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/auth/profile",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Unable to load profile.");
      }

      const data = await response.json();

      const userProfile = {
        name: data.name || "",
        email: data.email || "",
      };

      setProfile(userProfile);
      setProfileName(userProfile.name);

      const photoKey =
        `legalbot_profile_photo_${userProfile.email.toLowerCase()}`;

      setProfilePhoto(
        localStorage.getItem(photoKey) || ""
      );

      // Remove the old global photo key so it can never
      // leak from one account into another.
      localStorage.removeItem("legalbot_profile_photo");


      const passwordKey =
        `legalbot_password_${userProfile.email.toLowerCase()}`;

      const savedPassword =
        localStorage.getItem(passwordKey) || "";

      setPasswordForm((previous) => ({
        ...previous,
        current_password: savedPassword,
      }));

    } catch (error) {

      console.error("LegalBot profile error:", error);

    }
  };


  useEffect(() => {

    if (token) {
      loadProfile(token);
      loadRecentChats(token);
    }

  }, [token]);


  /* =========================
     SETTINGS
  ========================= */

  const openSettings = () => {
    setSettingsSection("profile");
    setProfileMessage("");
    setPasswordMessage("");
    setPasswordError("");

    setPasswordForm((previous) => ({
      current_password: previous.current_password,
      new_password: "",
      confirm_password: "",
    }));

    setSettingsOpen(true);
  };


  const closeSettings = () => {
    setSettingsOpen(false);
  };


  const handleThemeChange = (mode) => {

    const enabled = mode === "dark";

    setDarkMode(enabled);

    localStorage.setItem(
      "legalbot_theme",
      enabled ? "dark" : "light"
    );
  };


  const handleProfilePhotoChange = (event) => {

    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      setProfileMessage("Please select an image file.");
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      setProfileMessage("Profile photo must be 2 MB or smaller.");
      return;
    }

    const reader = new FileReader();

    reader.onload = () => {

      const photo = reader.result;

      setProfilePhoto(photo);

      const photoKey =
        `legalbot_profile_photo_${profile.email.toLowerCase()}`;

      localStorage.setItem(
        photoKey,
        photo
      );

      setProfileMessage(
        "Profile photo updated successfully."
      );
    };

    reader.onerror = () => {
      setProfileMessage("Unable to read the selected photo.");
    };

    reader.readAsDataURL(file);
  };


  const removeProfilePhoto = () => {
    setProfilePhoto("");

    if (profile.email) {
      const photoKey =
        `legalbot_profile_photo_${profile.email.toLowerCase()}`;

      localStorage.removeItem(photoKey);
    }

    localStorage.removeItem("legalbot_profile_photo");

    setProfileMessage(
      "Profile photo removed."
    );
  };


  const handleLanguageChange = (value) => {

    setLanguage(value);

    localStorage.setItem(
      "legalbot_language",
      value
    );
  };


  const handleProfileSave = async () => {

    const trimmedName = profileName.trim();

    if (!trimmedName) {
      setProfileMessage("Name cannot be empty.");
      return;
    }

    setProfileSaving(true);
    setProfileMessage("");

    try {

      const storedToken =
        localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:8000/auth/profile",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${storedToken}`,
          },
          body: JSON.stringify({
            name: trimmedName,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update profile."
        );
      }

      setProfile({
        name: data.name,
        email: data.email,
      });

      setProfileName(data.name);

      setProfileMessage(
        "Profile updated successfully."
      );

    } catch (error) {

      setProfileMessage(
        error.message || "Unable to update profile."
      );

    } finally {

      setProfileSaving(false);

    }
  };


  const handlePasswordSave = async () => {

    setPasswordMessage("");
    setPasswordError("");

    if (
      !passwordForm.current_password ||
      !passwordForm.new_password ||
      !passwordForm.confirm_password
    ) {
      setPasswordError(
        "Please fill in all password fields."
      );
      return;
    }

    if (passwordForm.new_password.length < 6) {
      setPasswordError(
        "New password must be at least 6 characters."
      );
      return;
    }

    if (
      passwordForm.new_password !==
      passwordForm.confirm_password
    ) {
      setPasswordError(
        "New password and confirmation do not match."
      );
      return;
    }

    setPasswordSaving(true);

    try {

      const storedToken =
        localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:8000/auth/password",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${storedToken}`,
          },
          body: JSON.stringify({
            current_password:
              passwordForm.current_password,
            new_password:
              passwordForm.new_password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update password."
        );
      }

      setPasswordForm({
        current_password: passwordForm.new_password,
        new_password: "",
        confirm_password: "",
      });

      setPasswordMessage(
        "Password updated successfully."
      );

    } catch (error) {

      setPasswordError(
        error.message || "Unable to update password."
      );

    } finally {

      setPasswordSaving(false);

    }
  };


  /* =========================
     CHAT STATE
  ========================= */
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTool, setActiveTool] = useState("chat");


  const [recentChats, setRecentChats] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  /* =========================
     CONVERSATION ID
  ========================= */

  const [conversationId, setConversationId] = useState(
    () => crypto.randomUUID()
  );
  
  /* =========================
   LOAD RECENT CHATS
  ========================= */

  const loadRecentChats = async (authToken) => {
    if (!authToken) {
      return;
    }

    try {
      setHistoryLoading(true);

      const data = await getChatHistory(authToken);

      setRecentChats(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (error) {

      console.error(
        "LegalBot history error:",
        error
      );

    } finally {

      setHistoryLoading(false);

    }
  };

  /* =========================
    OPEN PREVIOUS CHAT
  ========================= */

  const openPreviousChat = async (chat) => {

    console.log("========== OPEN HISTORY ==========");
    console.log("Clicked chat:", chat);
    console.log("Conversation ID:", chat?.conversation_id);
    console.log("Tool:", chat?.tool);

    if (!chat?.conversation_id) {
      console.error("No conversation ID found.");
      return;
    }

    const storedToken =
      localStorage.getItem("token");

    if (!storedToken) {
      console.error("No authentication token found.");
      return;
    }

    try {

      setLoading(true);

      /*
        -----------------------------------------
        1. Set conversation ID
        -----------------------------------------
      */

      setConversationId(
        chat.conversation_id
      );


      /*
        -----------------------------------------
        2. Restore the correct agent
        -----------------------------------------
      */

      const tool =
        chat.tool || "main";

      if (tool === "main") {

        setActiveTool("chat");

      } else {

        setActiveTool(tool);

      }


      /*
        -----------------------------------------
        3. Load messages
        -----------------------------------------
      */

      console.log(
        "Loading conversation:",
        chat.conversation_id
      );

      const history =
        await getConversationHistory(
          chat.conversation_id,
          storedToken
        );

      console.log(
        "Conversation history received:",
        history
      );


      /*
        -----------------------------------------
        4. Convert backend messages
          into frontend message format
        -----------------------------------------
      */

      const formattedMessages =
        Array.isArray(history)
          ? history.map((item) => ({

              role: item.role,

              content: item.message,

              emergency: false,

              evidence: [],

              missingInformation: [],

              generatedDocument: "",

              language: "en",

              intent: "general",

              sources: [],

            }))
          : [];


      /*
        -----------------------------------------
        5. Display conversation
        -----------------------------------------
      */

      setMessages(
        formattedMessages
      );

      setMessage("");


      console.log(
        "Conversation opened successfully."
      );


    } catch (error) {

      console.error(
        "ERROR OPENING CONVERSATION:",
        error
      );

      alert(
        error.message ||
        "Unable to open this conversation."
      );

    } finally {

      setLoading(false);

    }
  };


  /* =========================
     SIDEBAR TOOLS
  ========================= */

  const openTool = (tool) => {
    // Open a completely fresh tool session.
    // Do not place an automatic prompt in the input box.
    setActiveTool(tool);
    setMessages([]);
    setMessage("");
    setConversationId(crypto.randomUUID());
  };

  const returnToChat = () => {
    stopVoiceRecording();
    setVoiceError("");
    setActiveTool("chat");
    setMessages([]);
    setMessage("");
    setConversationId(crypto.randomUUID());
  };

  /* =========================
     VOICE ASSISTANT
  ========================= */

  const [isListening, setIsListening] = useState(false);
  const [voiceError, setVoiceError] = useState("");
  const [isVoiceProcessing, setIsVoiceProcessing] = useState(false);

  const recognitionRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const voiceStreamRef = useRef(null);

  const speechCompletedRef = useRef(false);
  const whisperFallbackRef = useRef(false);


  /* =========================
     START VOICE ASSISTANT
  ========================= */

  const startVoiceAssistant = async () => {

  console.log("LegalBot: Starting Whisper voice assistant");

  setVoiceError("");

  audioChunksRef.current = [];


  /* =========================
     MICROPHONE CHECK
  ========================= */

  if (
    !navigator.mediaDevices ||
    !navigator.mediaDevices.getUserMedia
  ) {

    setVoiceError(
      "Microphone access is not supported by this browser."
    );

    return;
  }


  /* =========================
     GET MICROPHONE
  ========================= */

  let stream;

  try {

    stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    });

    voiceStreamRef.current = stream;

    console.log(
      "LegalBot: Microphone access granted."
    );

  } catch (error) {

    console.error(
      "LegalBot: Microphone error:",
      error
    );

    setVoiceError(
      "Microphone permission was denied."
    );

    return;
  }


  /* =========================
     MEDIA RECORDER
     ========================= */

  try {

    if (!window.MediaRecorder) {

      throw new Error(
        "Audio recording is not supported by this browser."
      );
    }


    let mimeType = "";

    if (
      MediaRecorder.isTypeSupported(
        "audio/webm;codecs=opus"
      )
    ) {

      mimeType = "audio/webm;codecs=opus";

    } else if (
      MediaRecorder.isTypeSupported(
        "audio/webm"
      )
    ) {

      mimeType = "audio/webm";

    } else if (
      MediaRecorder.isTypeSupported(
        "audio/mp4"
      )
    ) {

      mimeType = "audio/mp4";
    }


    const recorder = mimeType
      ? new MediaRecorder(
          stream,
          { mimeType }
        )
      : new MediaRecorder(stream);


    mediaRecorderRef.current = recorder;


    /* =========================
       AUDIO DATA
    ========================= */

    recorder.ondataavailable = (event) => {

      console.log(
        "LegalBot: Audio chunk:",
        event.data.size
      );

      if (event.data.size > 0) {

        audioChunksRef.current.push(
          event.data
        );
      }
    };


    /* =========================
       RECORDING START
    ========================= */

    recorder.onstart = () => {

      console.log(
        "LegalBot: Whisper recording STARTED."
      );

      setIsListening(true);
    };


    /* =========================
       RECORDING STOP
    ========================= */

    recorder.onstop = () => {

      console.log(
        "LegalBot: Whisper recording STOPPED."
      );

    };


    /*
       Important:
       timeslice makes MediaRecorder
       continuously produce audio chunks.
    */

    recorder.start(250);


    console.log(
      "LegalBot: MediaRecorder started with:",
      recorder.mimeType
    );


    setIsListening(true);

  } catch (error) {

    console.error(
      "LegalBot: MediaRecorder error:",
      error
    );

    stream
      .getTracks()
      .forEach(
        (track) => track.stop()
      );

    voiceStreamRef.current = null;

    setVoiceError(
      error.message ||
      "Unable to start audio recording."
    );

    return;
  }
};


  /* =========================
     WHISPER TRANSCRIPTION
  ========================= */

  const transcribeWithWhisper = async () => {

  try {

    setIsVoiceProcessing(true);

    console.log(
      "LegalBot: Preparing audio for Whisper..."
    );

    setVoiceError("");

    const recorder =
      mediaRecorderRef.current;


    if (!recorder) {

      throw new Error(
        "Audio recorder is unavailable."
      );
    }


    /* =========================
       STOP RECORDER
    ========================= */

    if (
      recorder.state !== "inactive"
    ) {

      await new Promise((resolve) => {

        recorder.addEventListener(
          "stop",
          resolve,
          { once: true }
        );

        recorder.stop();

      });

    }


    /* =========================
       CREATE AUDIO BLOB
    ========================= */

    const mimeType =
      recorder.mimeType ||
      "audio/webm";

    const audioBlob =
      new Blob(
        audioChunksRef.current,
        {
          type: mimeType
        }
      );


    console.log(
      "LegalBot: Final audio size:",
      audioBlob.size,
      "bytes"
    );

    console.log(
      "LegalBot: Audio type:",
      audioBlob.type
    );


    if (audioBlob.size < 1000) {

      throw new Error(
        "Recording is too short. Please speak for a moment and try again."
      );
    }


    /* =========================
       GET TOKEN
    ========================= */

    const token =
      localStorage.getItem("token");


    if (!token) {

      throw new Error(
        "You are not logged in."
      );
    }


    /* =========================
       SEND TO WHISPER
    ========================= */

    console.log(
      "LegalBot: Sending audio to Whisper..."
    );


    const result =
      await transcribeVoice(
        audioBlob,
        token
      );


    console.log(
      "LegalBot: Whisper result:",
      result
    );


    if (
      !result ||
      !result.text ||
      !result.text.trim()
    ) {

      throw new Error(
        "Whisper could not understand the audio."
      );
    }


    /* =========================
       PUT TEXT INTO CHAT BOX
    ========================= */

    setMessage(
      result.text.trim()
    );


  } catch (error) {

    console.error(
      "LegalBot: Whisper error:",
      error
    );

    setVoiceError(
      error.message ||
      "Unable to understand your voice."
    );

  } finally {

    stopVoiceRecording();

    setIsVoiceProcessing(false);

  }
};


  /* =========================
     STOP VOICE RECORDING
  ========================= */

  const stopVoiceRecording = () => {

  console.log(
    "LegalBot: Cleaning up voice recording."
  );


  /* =========================
     STOP RECOGNITION
     ========================= */

  try {

    if (
      recognitionRef.current
    ) {

      recognitionRef.current.abort();

      recognitionRef.current = null;

    }

  } catch (error) {

    console.warn(
      "LegalBot: Recognition cleanup error:",
      error
    );

  }


  /* =========================
     STOP MEDIA RECORDER
     ========================= */

  try {

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {

      mediaRecorderRef.current.stop();

    }

  } catch (error) {

    console.warn(
      "LegalBot: Recorder cleanup error:",
      error
    );

  }


  /* =========================
     STOP MICROPHONE
     ========================= */

  if (
    voiceStreamRef.current
  ) {

    voiceStreamRef.current
      .getTracks()
      .forEach(
        (track) => track.stop()
      );

    voiceStreamRef.current = null;
  }


  mediaRecorderRef.current = null;

  audioChunksRef.current = [];

  speechCompletedRef.current = false;

  whisperFallbackRef.current = false;

  setIsListening(false);
};


  /* =========================
     MICROPHONE BUTTON
  ========================= */

  const toggleVoiceInput = async () => {

  console.log(
    "LegalBot: Microphone button clicked."
  );


  /* =========================
     IGNORE CLICK WHILE PROCESSING
  ========================= */

  if (isVoiceProcessing) {

    console.log(
      "LegalBot: Whisper is still processing."
    );

    return;
  }


  /* =========================
     STOP RECORDING
  ========================= */

  if (isListening) {

    console.log(
      "LegalBot: Stopping recording immediately..."
    );


    /*
      Update UI immediately.

      This makes the microphone button
      stop showing the recording state
      without waiting for Whisper.
    */

    setIsListening(false);


    /*
      Whisper transcription happens
      after recording stops.
    */

    await transcribeWithWhisper();

    return;
  }


  /* =========================
     START RECORDING
  ========================= */

  await startVoiceAssistant();

};

  /* =========================
     SEND MESSAGE
  ========================= */

  const handleSend = async () => {

    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message.trim();

    /* Add user message immediately */

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");

    setLoading(true);


    try {

      const storedToken =
        localStorage.getItem("token");

      if (!storedToken) {
        throw new Error(
          "Your session has expired. Please log in again."
        );
      }


      /* =========================
         SEND TO BACKEND
      ========================= */

      const response = await sendMessage(
        userMessage,
        storedToken,
        conversationId,
        activeTool === "chat" ? "main" : activeTool
      );

      /* =========================
         ADD ASSISTANT RESPONSE
      ========================= */

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",

          content:
            response.reply ||
            "LegalBot could not generate a response.",

          emergency:
            response.emergency || false,

          evidence:
            response.evidence || [],

          missingInformation:
            response.missing_information || [],

          generatedDocument:
            response.generated_document || "",

          language:
            response.language || "en",

          intent:
            response.intent || "general",

          sources:
            response.sources || [],
        },
      ]);

      /* Refresh recent chats */

      loadRecentChats(storedToken);

    } catch (error) {

      console.error(
        "LegalBot chat error:",
        error
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error.message ||
            "Unable to connect to LegalBot.",
          isError: true,
        },
      ]);

    } finally {

      setLoading(false);

    }
  };


  /* =========================
     NEW CHAT
  ========================= */

  const handleNewChat = () => {

    stopVoiceRecording();
    setVoiceError("");

    setMessages([]);

    setMessage("");

    setActiveTool("chat");

    /*
      Generate a completely new conversation ID.

      This means the new chat will NOT use
      the previous conversation history.
    */

    setConversationId(
      crypto.randomUUID()
    );
  };


  /* =========================
     LOGOUT
  ========================= */

  const handleLogout = () => {

    localStorage.removeItem("token");

    setToken(null);

    setMessages([]);

    setMessage("");

    setActiveTool("chat");

    stopVoiceRecording();

    setConversationId(
      crypto.randomUUID()
    );

    setAuthPage("login");
    setSettingsOpen(false);

    setProfile({
      name: "",
      email: "",
    });
  };


  /* =========================
     QUICK ACTIONS
  ========================= */

  const quickActions = [

    {
      icon: AlertTriangle,
      title: "Emergency Help",
      description:
        "Immediate cyber crime assistance",
    },

    {
      icon: Search,
      title: "Check a Scam",
      description:
        "Analyze a suspicious message or situation",
    },

    {
      icon: FileText,
      title: "Prepare a Complaint",
      description:
        "Create a cyber crime complaint draft",
    },

  ];


  /* =========================
     AUTH PAGE
  ========================= */

  if (!token) {

    if (authPage === "login") {

      return (
        <Login
          onLogin={(newToken, email, password) => {

            localStorage.setItem(
              "token",
              newToken
            );

            setToken(newToken);

            const passwordKey =
              `legalbot_password_${email.toLowerCase()}`;

            localStorage.setItem(
              passwordKey,
              password
            );

            setCurrentUser({
              email: email,
              password: password,
            });

            setConversationId(
              crypto.randomUUID()
            );

            setMessages([]);

            setMessage("");
            setActiveTool("chat");
          }}

          onSwitchToRegister={() => {
            setAuthPage("register");
          }}
        />
      );
    }


    return (
      <Register

        onRegister={() => {
          setAuthPage("login");
        }}

        onSwitchToLogin={() => {
          setAuthPage("login");
        }}

      />
    );
  }


  /* =========================
     MAIN APPLICATION
  ========================= */

  return (

    <div
      className={`app ${darkMode ? "dark-mode" : ""}`}
    >

      {/* ==================================
          SIDEBAR
      ================================== */}

      <aside className="sidebar">


        {/* LOGO */}

        <div className="brand">

          <div className="brand-icon legalbot-brand-mark">
            <ShieldCheck size={25} strokeWidth={2.2} />
            <span className="brand-bot-mark">
              <Bot size={10} strokeWidth={2.4} />
            </span>
          </div>

          <div>
            <h1>LegalBot</h1>

            <span>
              Cyber Crime Assistant
            </span>
          </div>

        </div>


        {/* NEW CHAT */}

        <button
          className="new-chat-btn"
          onClick={handleNewChat}
        >
          <Plus size={18} />

          New Chat
        </button>


        {/* RECENT CHATS */}

      <div className="recent-chats">

        <p className="section-title">
          RECENT CHATS
        </p>

        <div className="recent-chats-list">

          {historyLoading ? (

            <div className="chat-history-empty">
              Loading chats...
            </div>

          ) : recentChats.length === 0 ? (

            <div className="chat-history-empty">
              No recent chats
            </div>

          ) : (

            recentChats
              .slice(0, 20)
              .map((chat) => (

                <button
                  key={chat.conversation_id}
                  type="button"
                  className={`chat-history-item ${
                    chat.conversation_id === conversationId
                      ? "current-chat"
                      : ""
                  }`}
                  onClick={() =>
                    openPreviousChat(chat)
                  }
                  title={chat.title}
                >

                  <MessageSquare size={16} />

                  <span>
                    {chat.title || "New conversation"}
                  </span>

                </button>

              ))

          )}

        </div>

      </div>


        {/* QUICK TOOLS */}

        <div className="sidebar-section">

          <p className="section-title">
            QUICK TOOLS
          </p>

          <button
            type="button"
            className={`tool-item ${activeTool === "emergency" ? "active-tool" : ""}`}
            onClick={() => openTool("emergency")}
          >
            <AlertTriangle size={17} />
            <span>Emergency Help</span>
          </button>

          <button
            type="button"
            className={`tool-item ${activeTool === "evidence" ? "active-tool" : ""}`}
            onClick={() => openTool("evidence")}
          >
            <FileText size={17} />
            <span>Evidence Guide</span>
          </button>

          <button
            type="button"
            className={`tool-item ${activeTool === "complaint" ? "active-tool" : ""}`}
            onClick={() => openTool("complaint")}
          >
            <FileText size={17} />
            <span>Complaint Draft</span>
          </button>

          <button
            type="button"
            className={`tool-item ${activeTool === "scam" ? "active-tool" : ""}`}
            onClick={() => openTool("scam")}
          >
            <Search size={17} />
            <span>Check a Scam</span>
          </button>

        </div>


        {/* SIDEBAR BOTTOM */}

        <div className="sidebar-bottom">

          <button
            type="button"
            className="tool-item"
            onClick={openSettings}
          >
            <Settings size={17} />
            <span>Settings</span>
          </button>


          <div
            className="tool-item"
            onClick={handleLogout}
          >

            <LogOut size={17} />

            <span>
              Logout
            </span>

          </div>

        </div>

      </aside>


      {/* ==================================
          MAIN AREA
      ================================== */}

      <main className="main">


        {/* TOP BAR */}

        <header className="topbar">

          <div>

            <h2>
              {activeTool === "emergency"
                ? "Emergency Cybercrime Help"
                : activeTool === "evidence"
                ? "Cyber Crime Evidence Guide"
                : activeTool === "complaint"
                ? "Cyber Crime Complaint Draft"
                : activeTool === "scam"
                ? "Scam & Phishing Checker"
                : "Cyber Crime & Online Fraud Assistant"}
            </h2>

            <p>
              {activeTool === "emergency"
                ? "Get immediate guidance for urgent cyber incidents"
                : activeTool === "evidence"
                ? "Find out what evidence you should preserve"
                : activeTool === "complaint"
                ? "Describe what happened and prepare a complaint draft"
                : activeTool === "scam"
                ? "Analyze suspicious messages, links, calls, or online offers"
                : "Your AI-powered assistant for cyber crime incidents"}
            </p>

          </div>


          {/* LANGUAGE */}

          <div className="topbar-actions">

            <div className="profile-hover">
              <button
                type="button"
                className="profile-avatar-btn"
                onClick={openSettings}
                title="Open profile settings"
                aria-label="Open profile settings"
              >
                {profilePhoto ? (
                  <img
                    src={profilePhoto}
                    alt="Profile"
                  />
                ) : (
                  profile.name
                    ? profile.name.trim().charAt(0).toUpperCase()
                    : "U"
                )}
              </button>

              <div className="profile-hover-card">
                <div className="profile-hover-avatar">
                  {profilePhoto ? (
                    <img
                      src={profilePhoto}
                      alt="Profile"
                    />
                  ) : (
                    profile.name
                      ? profile.name.trim().charAt(0).toUpperCase()
                      : "U"
                  )}
                </div>
                <strong>{profile.name || "User"}</strong>
                <span>{profile.email || ""}</span>
                <small>Click to open profile</small>
              </div>
            </div>

            <button
              type="button"
              className="language-selector"
              onClick={openSettings}
              title="Change language in Settings"
            >
              🌐 {language}

              <ChevronDown size={16} />

            </button>

          </div>

        </header>


        {/* ==================================
            CHAT AREA
        ================================== */}

        <section className="chat-area">


          {/* EMPTY CHAT */}

          {messages.length === 0 ? (

            <>

              <div className="welcome">

                <div className="welcome-icon">
                  {activeTool === "emergency" ? (
                    <AlertTriangle size={32} />
                  ) : activeTool === "evidence" ? (
                    <FileText size={32} />
                  ) : activeTool === "complaint" ? (
                    <FileText size={32} />
                  ) : activeTool === "scam" ? (
                    <Search size={32} />
                  ) : (
                    <ShieldCheck size={32} />
                  )}
                </div>

                {activeTool === "chat" && profile.name ? (
                  <div className="welcome-user-name">
                    Welcome, {profile.name} 👋
                  </div>
                ) : null}

                <h2 className={activeTool === "chat" ? "welcome-main-question" : ""}>
                  {activeTool === "emergency"
                    ? "Emergency Help"
                    : activeTool === "evidence"
                    ? "Evidence Guide"
                    : activeTool === "complaint"
                    ? "Complaint Draft"
                    : activeTool === "scam"
                    ? "Check a Scam"
                    : "How can LegalBot help you today?"}
                </h2>

                <p>
                  {activeTool === "emergency"
                    ? "Tell me what is happening right now. I'll focus on the immediate actions you should take."
                    : activeTool === "evidence"
                    ? "Describe the incident and I'll give you a focused checklist of evidence you should preserve."
                    : activeTool === "complaint"
                    ? "Describe what happened in your own words. I'll ask only the essential missing questions before preparing the complaint."
                    : activeTool === "scam"
                    ? "Paste the suspicious message, link, email, call details, or offer. I'll help you assess the warning signs and tell you what to do next."
                    : "Describe your cyber crime or online fraud situation. I'll help you understand what happened, what to do next, and what evidence you should preserve."}
                </p>

                {activeTool !== "chat" && (
                  <div className="tool-example">
                    <span>Example</span>
                    <p>
                      {activeTool === "emergency"
                        ? "Someone made an unauthorized UPI transaction from my account."
                        : activeTool === "evidence"
                        ? "Someone called me pretending to be my bank and asked for an OTP."
                        : activeTool === "complaint"
                        ? "My Instagram account was hacked today and I cannot access it."
                        : "Your bank account will be blocked today. Click this link immediately to complete KYC."}
                    </p>
                  </div>
                )}

              </div>




            </>

          ) : (

            /* ==================================
               MESSAGES
            ================================== */

            <div className="messages-container">

              {messages.map(
                (msg, index) => (

                  <div
                    key={index}
                    className={`message-row ${msg.role}`}
                  >

                    <div className="message-bubble">


                      {/* MESSAGE LABEL */}

                      <div className="message-label">

                        {msg.role === "user"
                          ? "You"
                          : "LegalBot"}

                      </div>


                      {/* MESSAGE CONTENT */}

                      <div
                        className={`message-content ${
                          msg.isError
                            ? "error-message"
                            : ""
                        }`}
                      >

                        {msg.content}

                      </div>


                      {/* ERROR */}

                      {msg.isError && (

                        <div className="response-card">

                          <strong>
                            Please try again.
                          </strong>

                        </div>

                      )}


                      {/* EMERGENCY */}

                      {msg.emergency && (

                        <div
                          className="response-card emergency-card"
                        >

                          <strong>
                            🚨 Emergency Guidance
                          </strong>

                          <p>
                            Please follow the
                            immediate safety
                            instructions provided
                            above.
                          </p>

                        </div>

                      )}


                      {/*
                        IMPORTANT:

                        We DO NOT render
                        generatedDocument here.

                        Your backend's
                        ResponseFormatterAgent
                        already puts the generated
                        document inside response.reply.

                        Rendering it again was causing
                        the duplicate document.
                      */}


                    </div>

                  </div>

                )
              )}


              {/* LOADING */}

              {loading && (

                <div
                  className="message-row assistant"
                >

                  <div className="message-bubble">

                    <div className="message-label">
                      LegalBot
                    </div>

                    <div className="typing">
                      LegalBot is thinking...
                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </section>


        {/* ==================================
            INPUT AREA
        ================================== */}

        <div className="input-container">

          {activeTool !== "chat" && (
            <div className="active-tool-bar">
              <button
                type="button"
                onClick={returnToChat}
              >
                ← Back to Chat
              </button>
            </div>
          )}

          <div className="chat-input">


            {/* TEXT INPUT */}

            <input

              type="text"

              placeholder={
                activeTool === "emergency"
                  ? "Describe what is happening right now..."
                  : activeTool === "evidence"
                  ? "Describe the incident to get an evidence checklist..."
                  : activeTool === "complaint"
                  ? "Describe what happened and I will help prepare the complaint..."
                  : activeTool === "scam"
                  ? "Paste the suspicious message or describe the situation..."
                  : "Describe your cyber crime or online fraud..."
              }

              value={message}

              onChange={(e) => {
                setMessage(e.target.value);

                // Hide the microphone error as soon as the user
                // starts typing normally.
                if (voiceError) {
                  setVoiceError("");
                }
              }}

              onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {

                  e.preventDefault();

                  handleSend();

                }

              }}

            />


            {/* MICROPHONE */}

            <button
              className={`input-icon ${
                isListening ? "voice-listening" : ""
              }`}
              type="button"
              onClick={toggleVoiceInput}
              disabled={isVoiceProcessing}
              title={
                isListening
                  ? "Stop listening"
                  : "Voice input"
              }
              disabled={loading}
            >
              <Mic size={19} />
            </button>


            {/* SEND */}

            <button

              className="send-btn"

              onClick={handleSend}

              disabled={
                loading ||
                !message.trim()
              }

            >

              <Send size={18} />

            </button>

          </div>


          {/* VOICE PROCESSING STATUS */}
          {isVoiceProcessing && (
            <div
              style={{
                marginTop: "8px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "8px",
                fontSize: "13px",
                fontWeight: 500,
                color: darkMode ? "#aebdff" : "#4f46e5",
              }}
            >
              <span
                style={{
                  width: "12px",
                  height: "12px",
                  border: `2px solid ${
                    darkMode ? "#303b63" : "#d9ddff"
                  }`,
                  borderTopColor: darkMode
                    ? "#8b9cff"
                    : "#4f46e5",
                  borderRadius: "50%",
                  display: "inline-block",
                  animation: "legalbotSpin 0.8s linear infinite",
                }}
              />

              Processing your voice...
            </div>
          )}

          {/* VOICE ERROR */}
          {voiceError && !isVoiceProcessing && (
            <div
              style={{
                marginTop: "8px",
                fontSize: "12px",
                color: darkMode ? "#ffb4b4" : "#b42318",
              }}
            >
              {voiceError}
            </div>
          )}

          <p className="disclaimer">

            LegalBot provides AI-generated
            assistance and does not replace
            professional legal advice.

          </p>

        </div>

        {/* ==================================
            SETTINGS MODAL
        ================================== */}

        {settingsOpen && (
          <div
            onClick={(event) => {
              if (event.target === event.currentTarget) {
                closeSettings();
              }
            }}
            style={{
              position: "fixed",
              inset: 0,
              zIndex: 1000,
              background: "rgba(0, 0, 0, 0.45)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "24px",
            }}
          >

            <div
              style={{
                width: "min(760px, 100%)",
                maxHeight: "90vh",
                overflow: "hidden",
                borderRadius: "18px",
                background: darkMode ? "#18202b" : "#ffffff",
                color: darkMode ? "#f4f7fb" : "#18202b",
                boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
                display: "flex",
                flexDirection: "column",
              }}
            >

              {/* HEADER */}

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "20px 24px",
                  borderBottom: `1px solid ${
                    darkMode ? "#303a49" : "#e7eaf0"
                  }`,
                }}
              >

                <div>
                  <h2 style={{ margin: 0 }}>
                    Settings
                  </h2>

                  <p
                    style={{
                      margin: "5px 0 0",
                      opacity: 0.65,
                      fontSize: "13px",
                    }}
                  >
                    Manage your LegalBot account and preferences.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={closeSettings}
                  style={{
                    border: 0,
                    background: "transparent",
                    color: "inherit",
                    cursor: "pointer",
                    padding: "6px",
                  }}
                >
                  <X size={21} />
                </button>

              </div>


              {/* BODY */}

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "210px 1fr",
                  minHeight: "430px",
                  overflow: "hidden",
                }}
              >

                {/* NAVIGATION */}

                <div
                  style={{
                    padding: "14px",
                    borderRight: `1px solid ${
                      darkMode ? "#303a49" : "#e7eaf0"
                    }`,
                    background: darkMode ? "#141b24" : "#f8fafc",
                  }}
                >

                  {[
                    ["profile", "Profile", User],
                    ["password", "Security", LockKeyhole],
                    ["appearance", "Appearance", Palette],
                    ["language", "Language", ChevronDown],
                    ["about", "About LegalBot", Info],
                  ].map(([id, label, Icon]) => (

                    <button
                      key={id}
                      type="button"
                      onClick={() =>
                        setSettingsSection(id)
                      }
                      style={{
                        width: "100%",
                        display: "flex",
                        alignItems: "center",
                        gap: "10px",
                        padding: "11px 12px",
                        marginBottom: "4px",
                        border: 0,
                        borderRadius: "9px",
                        cursor: "pointer",
                        textAlign: "left",
                        color: "inherit",
                        background:
                          settingsSection === id
                            ? darkMode
                              ? "#263243"
                              : "#e8f0ff"
                            : "transparent",
                      }}
                    >

                      <Icon size={17} />

                      <span>{label}</span>

                      <ChevronRight
                        size={15}
                        style={{
                          marginLeft: "auto",
                          opacity: 0.45,
                        }}
                      />

                    </button>

                  ))}

                </div>


                {/* CONTENT */}

                <div
                  style={{
                    padding: "26px",
                    overflowY: "auto",
                  }}
                >

                  {/* PROFILE */}

                  {settingsSection === "profile" && (
                    <div>

                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "15px",
                          marginBottom: "28px",
                        }}
                      >

                        <div
                          style={{
                            width: "64px",
                            height: "64px",
                            borderRadius: "50%",
                            overflow: "hidden",
                            display: "grid",
                            placeItems: "center",
                            background: darkMode
                              ? "#29384a"
                              : "#e9f0ff",
                            fontSize: "21px",
                            fontWeight: 700,
                            flexShrink: 0,
                          }}
                        >
                          {profilePhoto ? (
                            <img
                              src={profilePhoto}
                              alt="Profile"
                              style={{
                                width: "100%",
                                height: "100%",
                                objectFit: "cover",
                              }}
                            />
                          ) : (
                            profile.name
                              ? profile.name
                                  .trim()
                                  .charAt(0)
                                  .toUpperCase()
                              : "U"
                          )}
                        </div>

                        <div>

                          <h3 style={{ margin: 0 }}>
                            {profile.name || "User"}
                          </h3>

                          <p
                            style={{
                              margin: "4px 0 0",
                              opacity: 0.65,
                            }}
                          >
                            {profile.email || "Loading profile..."}
                          </p>

                        </div>

                      </div>


                      <div
                        style={{
                          marginBottom: "24px",
                          padding: "14px",
                          borderRadius: "10px",
                          border: `1px solid ${
                            darkMode ? "#3a4656" : "#d8dee8"
                          }`,
                        }}
                      >

                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            gap: "15px",
                          }}
                        >

                          <div>
                            <strong>Profile photo</strong>

                            <p
                              style={{
                                margin: "4px 0 0",
                                fontSize: "12px",
                                opacity: 0.65,
                              }}
                            >
                              JPG, PNG or other image · maximum 2 MB
                            </p>
                          </div>

                          <label
                            style={{
                              display: "inline-flex",
                              alignItems: "center",
                              gap: "7px",
                              padding: "9px 12px",
                              borderRadius: "8px",
                              background: darkMode
                                ? "#263243"
                                : "#eef4ff",
                              cursor: "pointer",
                              fontSize: "13px",
                            }}
                          >
                            <Camera size={16} />
                            {profilePhoto ? "Change" : "Add photo"}

                            <input
                              type="file"
                              accept="image/*"
                              onChange={handleProfilePhotoChange}
                              style={{ display: "none" }}
                            />
                          </label>

                        </div>

                        {profilePhoto && (
                          <button
                            type="button"
                            onClick={removeProfilePhoto}
                            style={{
                              marginTop: "10px",
                              display: "inline-flex",
                              alignItems: "center",
                              gap: "6px",
                              border: 0,
                              background: "transparent",
                              color: "inherit",
                              opacity: 0.7,
                              cursor: "pointer",
                              padding: 0,
                              fontSize: "12px",
                            }}
                          >
                            <Trash2 size={14} />
                            Remove photo
                          </button>
                        )}

                      </div>


                      <label
                        style={{
                          display: "block",
                          marginBottom: "7px",
                          fontWeight: 600,
                        }}
                      >
                        Name
                      </label>

                      <input
                        type="text"
                        value={profileName}
                        onChange={(event) =>
                          setProfileName(event.target.value)
                        }
                        style={{
                          width: "100%",
                          boxSizing: "border-box",
                          padding: "11px 12px",
                          borderRadius: "9px",
                          border: `1px solid ${
                            darkMode ? "#3a4656" : "#d8dee8"
                          }`,
                          background: darkMode
                            ? "#111821"
                            : "#ffffff",
                          color: "inherit",
                        }}
                      />


                      <label
                        style={{
                          display: "block",
                          margin: "20px 0 7px",
                          fontWeight: 600,
                        }}
                      >
                        Email
                      </label>

                      <input
                        type="email"
                        value={profile.email}
                        disabled
                        style={{
                          width: "100%",
                          boxSizing: "border-box",
                          padding: "11px 12px",
                          borderRadius: "9px",
                          border: `1px solid ${
                            darkMode ? "#3a4656" : "#d8dee8"
                          }`,
                          background: darkMode
                            ? "#202936"
                            : "#f3f5f8",
                          color: "inherit",
                          opacity: 0.7,
                        }}
                      />

                      <p
                        style={{
                          margin: "7px 0 0",
                          fontSize: "12px",
                          opacity: 0.6,
                        }}
                      >
                        Email is your account identity and cannot be changed here.
                      </p>


                      <button
                        type="button"
                        onClick={handleProfileSave}
                        disabled={profileSaving}
                        style={{
                          marginTop: "22px",
                          padding: "10px 17px",
                          border: 0,
                          borderRadius: "9px",
                          cursor: profileSaving
                            ? "not-allowed"
                            : "pointer",
                          opacity: profileSaving ? 0.65 : 1,
                        }}
                      >
                        {profileSaving
                          ? "Saving..."
                          : "Save Changes"}
                      </button>


                      {profileMessage && (
                        <p
                          style={{
                            marginTop: "12px",
                            fontSize: "13px",
                          }}
                        >
                          {profileMessage}
                        </p>
                      )}

                    </div>
                  )}


                  {/* SECURITY */}

                  {settingsSection === "password" && (
                    <div>

                      <h3 style={{ marginTop: 0 }}>
                        Security
                      </h3>

                      <p
                        style={{
                          opacity: 0.7,
                          fontSize: "14px",
                        }}
                      >
                        Update the password you use to sign in to LegalBot.
                      </p>


                      {[
                        ["Current password", "current_password", "Enter current password"],
                        ["New password", "new_password", "Enter new password"],
                        ["Confirm new password", "confirm_password", "Confirm new password"],
                      ].map(([label, field, placeholder]) => (

                        <div
                          key={field}
                          style={{ marginTop: "17px" }}
                        >

                          <label
                            style={{
                              display: "block",
                              marginBottom: "7px",
                              fontWeight: 600,
                            }}
                          >
                            {label}
                          </label>

                          <div
                            style={{
                              position: "relative",
                            }}
                          >

                            <input
                              type={
                                passwordVisibility[field]
                                  ? "text"
                                  : "password"
                              }
                              name={field}
                              autoComplete={
                                field === "current_password"
                                  ? "current-password"
                                  : "new-password"
                              }
                              value={passwordForm[field]}
                              placeholder={placeholder}
                              onChange={(event) =>
                                setPasswordForm((previous) => ({
                                  ...previous,
                                  [field]: event.target.value,
                                }))
                              }
                              style={{
                                width: "100%",
                                boxSizing: "border-box",
                                padding: "11px 44px 11px 12px",
                                borderRadius: "9px",
                                border: `1px solid ${
                                  darkMode ? "#3a4656" : "#d8dee8"
                                }`,
                                background: darkMode
                                  ? "#111821"
                                  : "#ffffff",
                                color: "inherit",
                              }}
                            />

                            <button
                              type="button"
                              onClick={() =>
                                setPasswordVisibility((previous) => ({
                                  ...previous,
                                  [field]: !previous[field],
                                }))
                              }
                              title={
                                passwordVisibility[field]
                                  ? "Hide password"
                                  : "Show password"
                              }
                              style={{
                                position: "absolute",
                                right: "10px",
                                top: "50%",
                                transform: "translateY(-50%)",
                                border: 0,
                                background: "transparent",
                                color: "inherit",
                                opacity: 0.65,
                                cursor: "pointer",
                                padding: "4px",
                              }}
                            >
                              {passwordVisibility[field] ? (
                                <EyeOff size={18} />
                              ) : (
                                <Eye size={18} />
                              )}
                            </button>

                          </div>

                        </div>

                      ))}


                      {passwordError && (
                        <p style={{ marginTop: "14px" }}>
                          {passwordError}
                        </p>
                      )}

                      {passwordMessage && (
                        <p style={{ marginTop: "14px" }}>
                          {passwordMessage}
                        </p>
                      )}


                      <button
                        type="button"
                        onClick={handlePasswordSave}
                        disabled={passwordSaving}
                        style={{
                          marginTop: "20px",
                          padding: "10px 17px",
                          border: 0,
                          borderRadius: "9px",
                          cursor: passwordSaving
                            ? "not-allowed"
                            : "pointer",
                          opacity: passwordSaving ? 0.65 : 1,
                        }}
                      >
                        {passwordSaving
                          ? "Updating..."
                          : "Update Password"}
                      </button>

                    </div>
                  )}


                  {/* APPEARANCE */}

                  {settingsSection === "appearance" && (
                    <div>

                      <h3 style={{ marginTop: 0 }}>
                        Appearance
                      </h3>

                      <p
                        style={{
                          opacity: 0.7,
                          fontSize: "14px",
                        }}
                      >
                        Choose how LegalBot looks on this device.
                      </p>


                      {[
                        ["light", "Light"],
                        ["dark", "Dark"],
                      ].map(([value, label]) => (

                        <button
                          key={value}
                          type="button"
                          onClick={() =>
                            handleThemeChange(value)
                          }
                          style={{
                            width: "100%",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            padding: "14px",
                            marginTop: "10px",
                            borderRadius: "10px",
                            border: `1px solid ${
                              darkMode ? "#3a4656" : "#d8dee8"
                            }`,
                            background:
                              (value === "dark") === darkMode
                                ? darkMode
                                  ? "#263243"
                                  : "#eef4ff"
                                : "transparent",
                            color: "inherit",
                            cursor: "pointer",
                            textAlign: "left",
                          }}
                        >

                          <span>{label}</span>

                          {(value === "dark") === darkMode && (
                            <Check size={17} />
                          )}

                        </button>

                      ))}

                      <p
                        style={{
                          marginTop: "16px",
                          fontSize: "12px",
                          opacity: 0.6,
                        }}
                      >
                        Your choice is saved on this device.
                      </p>

                    </div>
                  )}


                  {/* LANGUAGE */}

                  {settingsSection === "language" && (
                    <div>

                      <h3 style={{ marginTop: 0 }}>
                        Language
                      </h3>

                      <p
                        style={{
                          opacity: 0.7,
                          fontSize: "14px",
                        }}
                      >
                        Choose your preferred LegalBot language.
                      </p>

                      <select
                        value={language}
                        onChange={(event) =>
                          handleLanguageChange(
                            event.target.value
                          )
                        }
                        style={{
                          marginTop: "18px",
                          width: "100%",
                          padding: "11px 12px",
                          borderRadius: "9px",
                          border: `1px solid ${
                            darkMode ? "#3a4656" : "#d8dee8"
                          }`,
                          background: darkMode
                            ? "#111821"
                            : "#ffffff",
                          color: "inherit",
                        }}
                      >

                        <option value="English">
                          English
                        </option>

                        <option value="Hindi">
                          Hindi
                        </option>

                      </select>

                      <p
                        style={{
                          marginTop: "10px",
                          fontSize: "12px",
                          opacity: 0.6,
                        }}
                      >
                        This language preference is used for LegalBot responses.
                      </p>

                    </div>
                  )}


                  {/* ABOUT */}

                  {settingsSection === "about" && (
                    <div>

                      <h3 style={{ marginTop: 0 }}>
                        About LegalBot
                      </h3>

                      <p
                        style={{
                          lineHeight: 1.6,
                          opacity: 0.75,
                        }}
                      >
                        LegalBot is an AI-powered cyber crime and online fraud assistant designed to help users understand incidents, take safety steps, preserve evidence, and prepare complaint drafts.
                      </p>

                      <div
                        style={{
                          marginTop: "20px",
                          padding: "15px",
                          borderRadius: "10px",
                          background: darkMode
                            ? "#202936"
                            : "#f5f7fa",
                        }}
                      >

                        <strong>Version</strong>

                        <p
                          style={{
                            margin: "5px 0 0",
                            opacity: 0.7,
                          }}
                        >
                          1.0
                        </p>

                      </div>

                      <p
                        style={{
                          marginTop: "18px",
                          fontSize: "12px",
                          lineHeight: 1.5,
                          opacity: 0.65,
                        }}
                      >
                        LegalBot provides AI-generated assistance and does not replace professional legal advice.
                      </p>

                    </div>
                  )}

                </div>

              </div>

            </div>

          </div>
        )}

      </main>

    </div>

  );
}


export default App;