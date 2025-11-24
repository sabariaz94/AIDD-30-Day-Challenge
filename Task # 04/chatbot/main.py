import chainlit as cl
import os
from app import on_chat_start, on_message

if __name__ == "__main__":
    # This is a workaround to run the app with `python main.py`
    # The normal `chainlit run app.py` is not working as expected
    from chainlit.cli import run_chainlit
    run_chainlit("app.py")