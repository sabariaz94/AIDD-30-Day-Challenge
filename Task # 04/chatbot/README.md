Role: Senior Python AI Engineer

Objective: Build a "Study Notes Summarizer & Quiz Generator Agent" using Chainlit and the openai-agents SDK.

1. Project Overview

The goal is to develop an intelligent web-based assistant that can summarize study materials and generate quizzes for learners.

UI: Chainlit (Modern, responsive web interface).

Model: Google Gemini model named gemini-2.0-flash (via OpenAI Agents SDK).

Memory: Local JSON file storage for storing summaries and user-generated quizzes.

Extra Functionality: PDF upload for automated summarization and quiz generation.

2. Critical Technical Constraints

Strict configuration rules:

Zero-Bloat Protocol (CRITICAL):

Do NOT write extra code. No unnecessary features, only core functionality.

API Configuration:

OpenAI Agents SDK configured for Gemini.

Base URL: https://generativelanguage.googleapis.com/v1beta/openai/

API Key: Load from GEMINI_API_KEY environment variable.

Model: OpenaiChatCompletionModel with gemini-2.0-flash.

SDK Specificity: Use openai-agents SDK syntax, not the standard openai library.

Error Recovery Protocol: Same as previous spec.

Dependency Management: Use uv for package management.

3. Architecture & File Structure
.
├── .env                  # Environment variables
├── tools.py              # Summary & Quiz memory functions
├── agent.py              # Agent configuration & tool binding
├── app.py                # Chainlit UI & Event Handlers
├── study_data.json       # JSON Storage (auto-created if missing)
├── pyproject.toml        # UV Config
└── uploads/              # Folder to store uploaded PDFs temporarily

4. Implementation Steps
Step 1: Documentation & Pattern Analysis

Verify SDK syntax for defining tools, initializing agents, and calling OpenaiChatCompletionModel.

Step 2: Tool Implementation (tools.py)

Create memory and PDF handling tools:

save_summary(topic: str, summary: str) → Stores summary under topic.

get_summary(topic: str) → Retrieves summary.

save_quiz(topic: str, quiz: dict) → Stores generated quizzes.

get_quiz(topic: str) → Retrieves stored quizzes.

save_pdf(file_path: str) → Saves uploaded PDF temporarily.

extract_text_from_pdf(file_path: str) → Uses PyPDF to extract text for summarization.

Format: Use correct tool decorator or FunctionTool from SDK.

Step 3: Agent Configuration (agent.py)

Initialize Gemini client with Base URL.

Initialize OpenaiChatCompletionModel with gemini-2.0-flash.

Bind the tools from tools.py.

System Prompt:
"You are a Study Notes Assistant. Summarize study material clearly, generate quizzes (MCQs or mixed style), and store them using tools. PDFs may be uploaded for processing."

Step 4: UI & Application Logic (app.py)

Integrate with Chainlit:

@cl.on_chat_start:

Initialize the agent.

Display static welcome message: "Welcome to Study Assistant! Upload your notes or PDF, or request a quiz."

@cl.on_message:

Pass user message to agent.

Await full response (non-streaming).

Send final text to UI with cl.Message().send().

Print/debug tool outputs to verify correct invocation.

PDF Summarizer Flow:

User uploads a PDF.

Tool extracts text using PyPDF.

Agent generates a clean, meaningful summary.

Summary can be displayed in any UI style (card, block, container, etc.).

Quiz Generator Flow:

After summarization, user clicks "Create Quiz".

Agent reads original PDF (not the summary).

Generates quizzes:

MCQs

Or mixed-style questions

Step 5: Environment & Dependencies

.env template with GEMINI_API_KEY.

List dependencies in pyproject.toml: openai-agents, chainlit, PyPDF2.

Check installed packages; do not reinstall if already present.

5. Testing Scenarios

New PDF Summary: User uploads "Biology.pdf" → Agent extracts text → Generates and stores summary.

Quiz Generation: User requests quiz → Agent reads PDF → Generates MCQs/mixed quizzes → Stores quiz.

Persistence: Restart server → Retrieve previous summary or quiz → Agent returns correct data.

Context Update: User uploads updated PDF → Agent regenerates summary → Quiz updates accordingly.