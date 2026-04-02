from .agents import right_wing_agent, left_wing_agent
from .model import (
    message_store,
    DebateMessage,
    AgentType,
    get_left_wing_message,
    get_right_wing_message,
)
from dataclasses import dataclass
import time


@dataclass
class DebateStats:
    """Statistics for a debate response"""

    model_name: str
    total_tokens: int
    input_tokens: int
    output_tokens: int
    response_time: float  # in seconds

    @property
    def tokens_per_second(self) -> float:
        """Calculate tokens generated per second"""
        if self.response_time == 0:
            return 0
        return self.output_tokens / self.response_time


async def make_debate(query: str) -> tuple[list, dict]:
    """Run debate and return results with stats"""
    start_time = time.time()

    right_result = await right_wing_agent.run("Here is the debate topic", deps=query)
    right_time = time.time() - start_time

    message_store.append(
        DebateMessage(
            agent_type=AgentType.RIGHT_WING,
            message=right_result.output,
        )
    )

    start_time = time.time()
    left_result = await left_wing_agent.run("Here is the debate topic", deps=query)
    left_time = time.time() - start_time

    message_store.append(
        DebateMessage(
            agent_type=AgentType.LEFT_WING,
            message=left_result.output,
        )
    )

    # Extract usage stats
    right_usage = right_result.usage()
    left_usage = left_result.usage()

    right_stats = DebateStats(
        model_name="Ollama Model",
        total_tokens=int(right_usage.total_tokens),
        input_tokens=int(right_usage.input_tokens),
        output_tokens=int(right_usage.output_tokens),
        response_time=right_time,
    )

    left_stats = DebateStats(
        model_name="Ollama Model",
        total_tokens=int(left_usage.total_tokens),
        input_tokens=int(left_usage.input_tokens),
        output_tokens=int(left_usage.output_tokens),
        response_time=left_time,
    )

    return [
        get_right_wing_message(right_result.output),
        get_left_wing_message(left_result.output),
    ], {
        "right": right_stats,
        "left": left_stats,
    }
