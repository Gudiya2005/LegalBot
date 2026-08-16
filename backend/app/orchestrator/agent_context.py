from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class AgentContext:

    # -----------------------------------------
    # User / conversation
    # -----------------------------------------

    user_id: int
    message: str
    tool: str = "main"

    language: Optional[str] = None

    chat_history: List[dict] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Cyber Brain
    # -----------------------------------------

    intent: Optional[str] = None

    incident_type: Optional[str] = None

    is_cyber_related: bool = True

    is_new_incident: bool = True

    is_general_query: bool = False

    emergency: bool = False

    # -----------------------------------------
    # Information collection
    # -----------------------------------------

    collected_information: Dict[str, Any] = field(
        default_factory=dict
    )

    missing_information: List[str] = field(
        default_factory=list
    )

    information_complete: bool = False

    # -----------------------------------------
    # Emergency / Golden Hour
    # -----------------------------------------

    golden_hour_actions: List[str] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Evidence
    # -----------------------------------------

    evidence_checklist: List[str] = field(
        default_factory=list
    )

    evidence: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------
    # RAG
    # -----------------------------------------

    retrieved_docs: List[Any] = field(
        default_factory=list
    )

    retrieved_knowledge: str = ""

    knowledge_sources: List[str] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Response planning
    # -----------------------------------------

    response_plan: Dict[str, Any] = field(
        default_factory=dict
    )

    main_response: str = ""

    final_response: str = ""

    # -----------------------------------------
    # Complaint
    # -----------------------------------------

    complaint_requested: bool = False

    complaint_ready: bool = False

    selected_document: str = ""

    generated_document: str = ""