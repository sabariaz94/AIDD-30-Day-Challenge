from agents import Agent
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel, AsyncOpenAI
from tools import (
    save_summary,
    get_summary,
    save_quiz,
    get_quiz,
    save_pdf,
    extract_text_from_pdf,
)
import os

# Initialize client
client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize chat model with client
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Create the agent
agent = Agent(
    name="StudyNotesAgent",
    instructions=(
        "You are a Study Notes Assistant. "
        "Summarize study material, generate quizzes (MCQs or mixed style), "
        "and store them using tools. PDFs may be uploaded."
    ),
    model=model,
    tools=[
        save_summary,
        get_summary,
        save_quiz,
        get_quiz,
        save_pdf,
        extract_text_from_pdf,
    ],
)

