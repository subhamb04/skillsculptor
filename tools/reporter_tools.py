from agents import function_tool

@function_tool
def prepare_executive_report(report_content, filename):
    print(f"Writing report...", flush=True)
    with open("reports/" + filename, "w") as file:
        file.write(report_content)
    return {"report": "report generated successfully"}

@function_tool
def read_report():
    report_content = ''
    with open("reports/gap_report.md", "r", encoding="utf-8") as f:
        report_content = f.read()
    return report_content

@function_tool
def append_executive_report(append_text):
    print(f"Modifying report...", flush=True)
    with open("reports/gap_report.md", "a") as file:
        file.write(append_text)
    return {"report": "report modified successfully"}