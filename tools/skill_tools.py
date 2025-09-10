from agents import function_tool
import pandas as pd

EMP_PATH = "sample_data/employees.csv"
PROJ_PATH = "sample_data/projects.csv"

def load_employees():
    df = pd.read_csv(EMP_PATH)
    df["skills_list"] = df["skills"].str.split(";").apply(lambda xs: [s.strip().lower() for s in xs])
    return df

def load_projects():
    df = pd.read_csv(PROJ_PATH)
    df["skills_required_list"] = df["skills_required"].str.split(";").apply(lambda xs: [s.strip().lower() for s in xs])
    return df

def get_project_requirements(project_id: str):
    """Return project skills + location for a given project_id."""
    proj = load_projects()
    row = proj[proj["project_id"] == project_id]
    if row.empty:
        return {"error": f"Project {project_id} not found"}
    r = row.iloc[0]
    return {"project_id": r.project_id, "location": r.location, "skills_required": r.skills_required_list}

@function_tool
def get_project_requirements_tool(project_id: str):
    return get_project_requirements(project_id)

@function_tool
def find_bench_matches(project_id: str):
    """Find benched employees matching a given project."""
    proj = get_project_requirements(project_id)
    if "error" in proj:
        return proj

    emps = load_employees()
    bench = emps[emps["status"].str.lower() == "benched"]
    matches = []
    for _, row in bench.iterrows():
        overlap = len(set(proj["skills_required"]) & set(row.skills_list))
        matches.append({"emp_id": row.emp_id, "name": row["name"], "overlap": overlap})
    matches.sort(key=lambda x: x["overlap"], reverse=True)
    return {"project_id": project_id, "matches": matches}