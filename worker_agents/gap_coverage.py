from agents import Agent
from ai_clients.gemini_client import client
from tools.gap_coverage_tools import compute_skill_coverage, analyze_internal_skill_gaps
from tools.market_tools import fetch_job_trends

gap_coverage_agent = Agent(
    name="Gap and Coverage Agent",
    model=client,
    instructions=""" 
    Your task is to analyze workforce skills and identify gaps. You have two core capabilities: 
    (1) compute skillwise coverage within the organization based on employee skills, project requirements, or skill supply; and 
    (2) identify external market skill trends by scraping the web and listing the top 5 most in-demand skills in technology. 
    When required, you can also compare external skill trends with internal skill coverage to highlight gaps. 
    Always use only the tools provided to you, and only invoke the relevant tool depending on whether the task concerns internal analysis,
    external market analysis, or both. Do not invent information beyond what is available through the tools.
    """,
    tools=[compute_skill_coverage, analyze_internal_skill_gaps, fetch_job_trends],
)
