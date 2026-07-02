# from pydantic import BaseModel, Field
# from agents import Agent

# HOW_MANY_SEARCHES = 5

# INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
# to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


# class WebSearchItem(BaseModel):
#     reason: str = Field(description="Your reasoning for why this search is important to the query.")
#     query: str = Field(description="The search term to use for the web search.")


# class WebSearchPlan(BaseModel):
#     searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
# planner_agent = Agent(
#     name="PlannerAgent",
#     instructions=INSTRUCTIONS,
#     model="gpt-4o-mini",
#     output_type=WebSearchPlan,
# )

import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

HOW_MANY_SEARCHES = 5


def create_search_plan(query: str) -> dict:
    prompt = f"""
You are a research planner.

User query:
{query}

Generate exactly {HOW_MANY_SEARCHES} web searches that would help answer this question comprehensively.

Return ONLY valid JSON in this format:

{{
  "searches": [
    {{
      "reason": "why this search matters",
      "query": "search query"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return json.loads(response.choices[0].message.content)