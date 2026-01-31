
from typing import Dict
from crewai import Agent
from ..llm import create_llm

dynamic_agents: Dict[str, Agent] = {}

# One LLM instance reused across agents
_llm = create_llm()

def get_or_create_agent(role: str, goal: str = "", backstory: str = "", allow_delegation=False) -> Agent:
    """
    Simple agent factory without any attached memory or loggers.
    """
    if role in dynamic_agents:
        return dynamic_agents[role]

    agent = Agent(
        role=role,
        goal=goal or f"Fulfill the responsibilities of a {role}.",
        backstory=backstory or f"You are a skilled {role}.",
        allow_delegation=allow_delegation,
        llm=_llm,
    )
    dynamic_agents[role] = agent
    return agent

# Project Manager (singleton)
manager = get_or_create_agent(
    role="Project Manager",
    goal="Understand user request, create minimal agent plan.",
    backstory="You orchestrate efficient agent usage."
)