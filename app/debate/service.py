from debate.agents import right_wing_agent, left_wing_agent
from debate.model import (
    message_store,
    DebateMessage,
    AgentType,
    get_left_wing_message,
    get_right_wing_message,
)


async def make_debate(query: str) -> tuple[DebateMessage]:
    right_result = await right_wing_agent.run("Here is the debate topic", deps=query)
    left_result = await left_wing_agent.run("Here is the debate topic", deps=query)

    message_store.append(
        DebateMessage(
            agent_type=AgentType.RIGHT_WING,
            message=right_result,
        )
    )
    message_store.append(
        DebateMessage(
            agent_type=AgentType.LEFT_WING,
            message=left_result,
        )
    )

    return (
        get_right_wing_message(right_result),
        get_left_wing_message(left_result),
    )
