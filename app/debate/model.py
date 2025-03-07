from typing_extensions import TypedDict
from enum import Enum


class AgentType(Enum):
    LEFT_WING = 1
    RIGHT_WING = 2


class DebateMessage(TypedDict):
    agent_type: AgentType
    message: str


class AgentResult(TypedDict):
    agent: str
    message: str


message_store: list[DebateMessage] = []

__right_wing_leader = {
    "US": "Donald Trump",
    "DE": "Alice Weidel",
    "IN": "BJP",
}
__left_wing_leader = {
    "US": "Joe Biden",
    "DE": "Olaf Scholz",
    "IN": "INC",
}

__country = "US"

system_prompts: dict[str, str] = {
    "right_wing_system_prompt": f"""
You have thoughts like {__right_wing_leader[__country]} and are a participant with right-wing/conservative political views.
Keep your response concise (3-4 sentences maximum) and focused on the topic. Here are the previous messages about the debate {message_store}
Please get more information by calling the right_wing_additional_data function
""",
    "left_wing_system_prompt": f"""
You have thoughts like {__left_wing_leader[__country]} with left-wing/progressive political views. 
Keep your response concise (3-4 sentences maximum) and focused on the topic. Here are the previous messages about the debate {message_store}
Please get more information by calling the left_wing_additional_data function
""",
    "right_wing_researcher_agent_prompt": f"Search DuckDuckGo for the given query about this topic and how it aligns with {__right_wing_leader[__country]} thinking and return 5 sentences that best describe this in a right wing political view.",
    "left_wing_researcher_agent_prompt": f"Search DuckDuckGo for the given query about this topic and how it aligns with {__left_wing_leader[__country]} thinking and return 5 sentences that best describe this in a left wing political view.",
}


def get_right_wing_message(message: str) -> AgentResult:
    return AgentResult(
        agent=__right_wing_leader[__country],
        message=message,
    )


def get_left_wing_message(message: str) -> AgentResult:
    return AgentResult(
        agent=__left_wing_leader[__country],
        message=message,
    )
