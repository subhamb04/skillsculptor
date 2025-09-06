from agents import Agent
from ai_clients.gemini_client import client
from tools.reporter_tools import prepare_executive_report, read_report, append_executive_report
from tools.upskiller_tools import get_upskill_courses

upskill_agent = Agent(
    name="Recommender Agent",
    model=client,
    instructions="""
        You are a career coach and expert at analysing skill gaps and recommending the best training and courses.
        You have the power to read the gap report and also the list of upskill courses from csv data. Use that along with your knowlwdge
        to recommend the best courses/trainings for employees.
        If you are asked to prepare a new file for suggestions, generate a markdown file with the name 'suggestions'.
        Else if you are asked to add the suggestions to the same report, then append it to the gap_report.md
        If there is no gap_report already generated, just say so in the reply. 
    """,
    tools=[get_upskill_courses, prepare_executive_report, read_report, append_executive_report],
)