
import json
from textwrap import dedent
from crewai import Task, Crew
from typing import List, Dict, Any

from ..agents.factory import manager, get_or_create_agent
from ..utils.parsing import parse_json_response, enforce_plan_structure

def manager_suggests_plan(user_request: str) -> List[Dict[str, Any]]:
    """
    Ask the manager to generate a lean JSON plan.
    """
    suggestion_task = Task(
        description=dedent(f"""
            Analyze the following user request: {user_request}

            Create a minimal plan with as few agents as possible:
            - If the work is focused on one domain (e.g., only frontend), use ONE agent.
            - If multiple domains are explicitly required (frontend + backend), create one agent per domain.
            - Avoid micro-agents.

            Respond strictly as a JSON list where each item has:
              - agent
              - task
              - tools (list)
              - plan
        """),
        expected_output="JSON plan",
        agent=manager,
    )

    crew = Crew(agents=[manager], tasks=[suggestion_task], process="sequential", verbose=False)
    raw_result = crew.kickoff()
    raw_text = getattr(raw_result, "raw", None) or getattr(raw_result, "text", None) or str(raw_result)
    plan = enforce_plan_structure(parse_json_response(raw_text))
    return plan

def manager_refine_plan(existing_plan, feedback, user_request):
    """
    Ask the manager to refine the JSON plan based on feedback.
    """
    refine_task = Task(
        description=dedent(f"""
            You are provided a previously generated plan (JSON). The user wants the plan refined.

            Existing plan:
            {json.dumps(existing_plan, indent=2)}

            User feedback:
            {feedback}

            Original request:
            {user_request}

            Return a refined plan in JSON list format with fields:
            - agent
            - task
            - tools
            - plan
        """),
        expected_output="Refined JSON plan",
        agent=manager,
    )

    crew = Crew(agents=[manager], tasks=[refine_task], process="sequential", verbose=False)
    raw_result = crew.kickoff()
    raw_text = getattr(raw_result, "raw", None) or getattr(raw_result, "text", None) or str(raw_result)
    plan = enforce_plan_structure(parse_json_response(raw_text))
    return plan

def build_tasks_from_plan(plan: list):
    """
    Create CrewAI tasks for each phase in the plan.
    """
    from crewai import Task
    tasks = []
    for item in plan:
        role = item["agent"]
        task_desc = item["task"]
        tools = item.get("tools", [])
        plan_notes = item.get("plan", "")

        if isinstance(tools, str):
            tools = [tools]

        agent = get_or_create_agent(
            role=role,
            goal=(f"Use {', '.join(tools)} to {task_desc}" if tools else task_desc),
            backstory=f"You are the {role}. You specialize in {', '.join(tools)}.",
            allow_delegation=(role == "Project Manager"),
        )

        tasks.append(
            Task(
                description=f"""{task_desc}

                Tools to use: {', '.join(tools) if tools else 'any suitable tools'}.
                Plan notes: {plan_notes}
                """,
                expected_output=f"Deliverables for: {role}",
                agent=agent,
            )
        )

    return tasks
