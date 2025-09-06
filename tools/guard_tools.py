from agents import function_tool
from datetime import datetime

@function_tool
def read_rules():
    guardrails = ''
    with open("utils/guardrails.txt", "r", encoding="utf-8") as f:
        guardrails = f.read()
    return guardrails

@function_tool
def log_violation(text):
    print(f"Logging violation: {text}", flush=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"Datetime: {now} | Question: {text}\n"
    with open("reports/violations.txt", "a", encoding="utf-8") as f:
        f.write(line)
    return {"logged": "ok"}