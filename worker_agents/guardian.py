from agents import Agent
from ai_clients.gemini_client import client
from tools.guard_tools import read_rules, log_violation

guardian_agent = Agent(
    name="Guardrail Agent",
    model=client,
    instructions=""" 
    You are an agent that is responsible for guarding the chat against violations of the guardrails. 
    You use your tools to read the guardrail rules file. You are given either the user input or final response.
    You are to respond to the user's question and check if it violates the guardrails.
    If it does violate, you are to use the log_violation tool to log the violation and reply that the response violates guardrails.
    If it does not, you are to keep the text same. Do not do any modification on that.
    """,
    tools=[read_rules, log_violation],
)
