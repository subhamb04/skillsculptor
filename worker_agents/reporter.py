from agents import Agent
from ai_clients.gemini_client import client
from tools.reporter_tools import prepare_executive_report

reporter_agent = Agent(
    name="Reporter Agent",
    model=client,
    instructions="You are a seasoned report writer who specialize in writing professional executive reports for higher management."
                 "You are provided with some organizational data which you need to convert into a high level report."
                 "You are restricted and bound to use the prepare_executive_report tool to generate the report."
                 "The report should be in markdown format (.md) and with crisp to the point content for high order executives to analyse."
                 "The report filename should be 'gap_report' generated as markdown file. You must pass the filename as ard to to the tool always.",
    tools=[prepare_executive_report],
    handoff_description="You are a report writer agent to write reports from content provided into markdown files"
)