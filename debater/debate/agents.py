from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool as searcher
from .model import system_prompts

__model = OpenAIChatModel(
    model_name="gemini-3-flash-preview",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

# right wing agents
right_wing_agent = Agent(
    model=__model,
    deps_type=str,
    output_type=str,
    output_retries=2,
    system_prompt=[system_prompts["right_wing_system_prompt"]],
)

right_wing_researcher_agent = Agent(
    model=__model,
    deps_type=str,
    output_type=str,
    output_retries=2,
    tools=[searcher(max_results=3)],
    system_prompt=[system_prompts["right_wing_researcher_agent_prompt"]],
)

# left wing agents
left_wing_agent = Agent(
    model=__model,
    deps_type=str,
    output_type=str,
    output_retries=2,
    system_prompt=system_prompts["left_wing_system_prompt"],
)

left_wing_researcher_agent = Agent(
    model=__model,
    deps_type=str,
    output_type=str,
    output_retries=2,
    tools=[searcher(max_results=3)],
    system_prompt=system_prompts["left_wing_researcher_agent_prompt"],
)


# right wing functions
@right_wing_agent.system_prompt
async def add_right_wing_agent_data(ctx: RunContext[str]) -> str:
    debate_topic = ctx.deps
    return f"This is the debate topic to show your right-wing values: '{debate_topic}'"


@right_wing_agent.tool
async def right_wing_additional_data(ctx: RunContext[str]) -> str:
    result = await right_wing_researcher_agent.run(
        "Here is the data for you search.",
        deps=ctx.deps,
    )
    return result.output


@right_wing_researcher_agent.system_prompt
async def add_right_wing_data(ctx: RunContext[str]) -> str:
    debate_topic = ctx.deps
    return f"There is the search topic: '{debate_topic}'"


# left wing functions
@left_wing_agent.system_prompt
async def add_left_wing_agent_data(ctx: RunContext[str]) -> str:
    debate_topic = ctx.deps
    return f"This is the debate topic to show your left-wing values: '{debate_topic}'"


@left_wing_agent.tool
async def left_wing_additional_data(ctx: RunContext[str]) -> str:
    result = await left_wing_researcher_agent.run(
        "Here is the data for you search.",
        deps=ctx.deps,
    )
    return result.output


@left_wing_researcher_agent.system_prompt
async def add_left_wing_data(ctx: RunContext[str]) -> str:
    debate_topic = ctx.deps
    return f"There is the search topic: '{debate_topic}'"
