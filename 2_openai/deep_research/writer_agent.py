# from pydantic import BaseModel, Field
# from agents import Agent

# INSTRUCTIONS = (
#     "You are a senior researcher tasked with writing a cohesive report for a research query. "
#     "You will be provided with the original query, and some initial research done by a research assistant.\n"
#     "You should first come up with an outline for the report that describes the structure and "
#     "flow of the report. Then, generate the report and return that as your final output.\n"
#     "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
#     "for 5-10 pages of content, at least 1000 words."
# )


# class ReportData(BaseModel):
#     short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

#     markdown_report: str = Field(description="The final report")

#     follow_up_questions: list[str] = Field(description="Suggested topics to research further")


# writer_agent = Agent(
#     name="WriterAgent",
#     instructions=INSTRUCTIONS,
#     model="gpt-4o-mini",
#     output_type=ReportData,
# )

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def write_report(
    query: str,
    search_results: list[str],
) -> str:
    research_notes = "\n\n".join(search_results)

    prompt = f"""
You are a senior research analyst.

Original Query:
{query}

Research Notes:
{research_notes}

Instructions:

1. Create a logical report structure.
2. Write a detailed markdown report.
3. Use headings and subheadings.
4. Include key findings.
5. Include conclusions.
6. Be thorough and detailed.

Target length:
1000+ words.

Return ONLY markdown.
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content