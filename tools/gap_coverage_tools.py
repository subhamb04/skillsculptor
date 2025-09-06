from agents import function_tool
import pandas as pd

EMP_PATH = "data/employees.csv"
PROJ_PATH = "data/projects.csv"

def load_employees():
    df = pd.read_csv(EMP_PATH)
    df["skills_list"] = df["skills"].str.split(";").apply(lambda xs: [s.strip().lower() for s in xs])
    return df

def load_projects():
    df = pd.read_csv(PROJ_PATH)
    df["skills_required_list"] = df["skills_required"].str.split(";").apply(lambda xs: [s.strip().lower() for s in xs])
    return df

@function_tool
def compute_skill_coverage():
    """Return % coverage per skill for the whole organization, split by Benched vs Deployed."""
    emps = load_employees()
    total = emps["emp_id"].nunique()

    exploded = emps.explode("skills_list")
    skill_counts = exploded.groupby("skills_list")["emp_id"].nunique()
    status_split = exploded.groupby(["skills_list", "status"])["emp_id"].nunique().unstack(fill_value=0)

    results = []
    for skill, count in skill_counts.items():
        benched = int(status_split.loc[skill].get("Benched", 0)) if skill in status_split.index else 0
        deployed = int(status_split.loc[skill].get("Deployed", 0)) if skill in status_split.index else 0
        pct = round((count / total) * 100, 2) if total else 0
        results.append({
            "skill": skill,
            "employees": int(count),
            "coverage_pct": pct,
            "benched": benched,
            "deployed": deployed
        })
    return {"coverage": sorted(results, key=lambda x: -x["coverage_pct"])}


@function_tool
def analyze_internal_skill_gaps(project_ids: list[str] = []):
    """Compare internal supply vs demand across projects. Identify gaps internal to organizational requirements."""
    emps = load_employees()
    projs = load_projects()

    if project_ids:
        projs = projs[projs["project_id"].isin(project_ids)]

    # demand side
    demand = {}
    for _, row in projs.iterrows():
        for skill in row.skills_required_list:
            demand[skill] = demand.get(skill, 0) + 1

    # supply side
    exploded = emps.explode("skills_list")
    supply = exploded.groupby("skills_list")["emp_id"].nunique().to_dict()

    results = []
    for skill, d in demand.items():
        s = supply.get(skill, 0)
        ratio = round(s / d, 2) if d > 0 else 0
        results.append({"skill": skill, "demand": d, "supply": s, "supply_demand_ratio": ratio})
    return {"gaps": sorted(results, key=lambda x: x["supply_demand_ratio"])}