# from agents import Agent, WebSearchTool, ModelSettings

# INSTRUCTIONS = (
#     "You are a research assistant. Given a search term, you search the web for that term and "
#     "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
#     "words. Capture the main points. Write succintly, no need to have complete sentences or good "
#     "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
#     "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
# )

# search_agent = Agent(
#     name="Search agent",
#     instructions=INSTRUCTIONS,
#     tools=[WebSearchTool(search_context_size="low")],
#     model="gpt-4o-mini",
#     model_settings=ModelSettings(tool_choice="required"),
# )

import os

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query: str) -> str:
    search_results = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    collected_text = []

    for result in search_results.get("results", []):
        collected_text.append(
            f"""
Title: {result.get('title', '')}

URL: {result.get('url', '')}

Content:
{result.get('content', '')}
"""
        )

    raw_content = "\n\n".join(collected_text)

    prompt = f"""
You are a research assistant.

Summarize the following web search results.

Requirements:
- Less than 300 words
- Focus on important facts
- Ignore fluff
- Multiple concise paragraphs

Search Query:
{query}

Web Results:
{raw_content}
"""

    response = groq_client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
