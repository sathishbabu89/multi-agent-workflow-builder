
from typing import List, Dict, Any
from crewai import Crew
from .planning import build_tasks_from_plan
from ..agents.factory import manager

def run_dynamic_flow(plan: list) -> List[Dict[str, Any]]:
    """
    Run a given list[dict] of phases (agents) sequentially and collect outputs.
    """
    tasks = build_tasks_from_plan(plan)
    agents_for_crew = [manager] + [t.agent for t in tasks]

    crew = Crew(
        agents=agents_for_crew,
        tasks=tasks,
        process="sequential",
        verbose=False,
    )

    result = crew.kickoff()

    task_outputs = getattr(result, "tasks_output", None) or getattr(result, "outputs", None)
    if not task_outputs:
        try:
            task_outputs = list(result)
        except Exception:
            task_outputs = [result]

    stored_outputs = []
    for idx, t in enumerate(task_outputs, start=1):
        try:
            agent_name = getattr(t, "agent", None) or getattr(t, "agent_name", None) or getattr(t, "role", None) or f"agent_{idx}"
            output_text = getattr(t, "raw", None) or getattr(t, "text", None) or getattr(t, "summary", None) or str(t)
        except Exception:
            agent_name = f"agent_{idx}"
            output_text = str(t)

        stored_outputs.append({"agent": agent_name, "task_id": f"task:{idx}", "output": output_text})

    return stored_outputs
