import chainlit as cl
from agent import agent

@cl.on_chat_start
async def start():
    cl.user_session.set("agent", agent)
    await cl.Message("Welcome! Upload a PDF or ask for a quiz.").send()

@cl.on_message
async def on_message(message: cl.Message):
    ag = cl.user_session.get("agent")

    # Handle PDF upload
    if message.elements:
        for element in message.elements:
            if "pdf" in element.mime:
                file_path = element.path

                # Save the PDF
                save_status = await ag.run(f"save_pdf('{file_path}')")
                await cl.Message(f"PDF saved: {save_status}").send()

                # Extract text from PDF
                try:
                    text = await ag.run(f"extract_text_from_pdf('{file_path}')")
                    if not text:
                        await cl.Message("Failed to extract text from PDF.").send()
                        return
                except Exception as e:
                    await cl.Message(f"Error extracting PDF text: {e}").send()
                    return

                # Summarize the extracted text
                try:
                    summary = await ag.run(f"Summarize this:\n{text}")
                    await cl.Message(f"Summary of {element.name}:\n{summary}").send()
                except Exception as e:
                    await cl.Message(f"Error summarizing PDF: {e}").send()
                    return

                # Save the summary
                await ag.run(f"save_summary(topic='{element.name}', summary='{summary}')")
                return

    # Handle normal text messages
    try:
        response = await ag.run(message.content)
        await cl.Message(response).send()
    except Exception as e:
        await cl.Message(f"Error in agent response: {e}").send()


