from agents import Agent
from ai_clients.gemini_client import client
from tools.skill_tools import get_project_requirements_tool, find_bench_matches

skill_matching_agent = Agent(
    name="Skill Matching Agent",
    model=client,
    instructions=(
        "You specialize in matching project requirements to benched employees. "
        "Always use tools to fetch project details and recommend matches."
        "Use the find_bench_matches tool to fetch project details and recommend matches."
        "Use the get_project_requirements tool to fetch project details."
        "If no best match overlaps (Overlaps: 0 or Overlap not specified) with the project requirements, then specify no match found"
        "Recommend only the employees if there are any skill overlaps."
        "Recommend only the number of best matches specified by the user."
        "Do not return the names of the employees who don't have any skill overlaps."
    ),
    tools=[get_project_requirements_tool, find_bench_matches],
)
