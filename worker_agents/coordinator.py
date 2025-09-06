# coordinator.py
from agents import Agent
from ai_clients.gemini_client import client
from worker_agents.skill_matching import skill_matching_agent
from worker_agents.gap_coverage import gap_coverage_agent
from worker_agents.reporter import reporter_agent
from worker_agents.guardian import guardian_agent
from worker_agents.upskill import upskill_agent

# --- Tools setup ---
skill_matching_agent_as_tool = skill_matching_agent.as_tool(
    tool_name="skill_matching_agent",
    tool_description="This agent is specialized in matching project requirements to benched employees."
)

gap_coverage_agent_as_tool = gap_coverage_agent.as_tool(
    tool_name="gap_coverage_agent",
    tool_description="This agent is specialized in detecting organizations's skill gaps (BOTH INTERNAL AND MARKET TRENDS) and computing skill coverages by comparing project demand vs employee supply."
)

guardian_agent_as_tool = guardian_agent.as_tool(
    tool_name="guardian_agent",
    tool_description="This agent examines user input or final response for guardrail violations and logs if necessary"
)

# --- Coordinator Agent ---
coordinator = Agent(
    name="Coordinator",
    model=client,
    instructions=(
        """
        You are a workforce planning agent. Interpret user queries in natural language and route them to the appropriate capability:

        - If the query is about project staffing or requirement details, use your staffing capability.
        - If the query is about identifying missing skills within the organization or comparison to market data, 
            use your skill gap analysis capability.
        - If the query is outside these areas, respond that you are not trained for that topic.

        Always fetch data through your available capabilities rather than inventing answers. 

        Handoffs:
        1. If asked to prepare a report on skill gap analysis, first gather the required data, generate the analysis, 
        and then pass it on for report writing. Do not invoke report writing unless explicitly asked for a report, otherwise, 
        just respond directly with the requested information.

        2. If asked to give suggestions for filling the skill gap, pass it on to the upskill_agent for analysing the report
        and suggest the list of courses. While passing the instruction also explicitly mention whether the user wants suggestion in a
        new file or whether to append in the same gap_report.md

        Note: Do not ask of human approval/intervention before passing the job to handoffs(if you need to do so).

        Guardrail Enforcement:
        - Every user input must first be examined by the guardrail tool for rule violations before taking any action.
        - Every final response must also be examined by the guardrail tool before being delivered to the user.
        - If the guardrail tool flags a violation, do not override or bypass it. Respect the result and log the violation.
        - Only deliver responses that pass guardrail validation. If blocked, inform the user appropriately without exposing internal details.
        """
    ),
    tools=[skill_matching_agent_as_tool, gap_coverage_agent_as_tool, guardian_agent_as_tool],
    handoffs=[reporter_agent, upskill_agent]
)
