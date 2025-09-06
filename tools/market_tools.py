from agents import function_tool
import pandas as pd
import feedparser
from ai_clients.gemini_client import chatllm

MARKET_FALLBACK_PATH = "data/market_trends.csv"

def load_fallback_market_trends():
    df = pd.read_csv(MARKET_FALLBACK_PATH)
    df["skill"] = df["skill"].str.lower()
    return df["skill"].tolist()

def scrape_web_trends():
    url = "https://news.google.com/rss/search?q=top+technology+skills+in+demand&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    articles = [entry.title + " " + entry.summary for entry in feed.entries[:10]]
    return " ".join(articles)

@function_tool
def fetch_job_trends():
    try: 
        raw_text = scrape_web_trends()

        # Prompt Gemini to extract skills
        response = chatllm.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are an expert analyst of job market trends from the data provided to you."},
                {"role": "user", "content": f"""
                        From the following job market news, extract the 5 most in-demand technical skills.
                        Assign each skill a demand index between 0 and 1 (1 = most demand).
                        Format strictly like:
                        1. Skill : <skill name> demand_index : <score>
                        2. Skill : <skill name> demand_index : <score>

                        News Data:
                        {raw_text}
                        """}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[WARN] Scraping failed, using fallback CSV. Error: {e}")
        return load_fallback_market_trends()