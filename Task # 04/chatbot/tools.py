# tools.py
import json
import os
from typing import Dict, Any
import PyPDF2

def_file = "study_data.json"
upload_folder = "uploads"

def read_data() -> Dict[str, Any]:
    try:
        with open(def_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"summaries": {}, "quizzes": {}}

def write_data(data: Dict[str, Any]) -> None:
    with open(def_file, 'w') as f:
        json.dump(data, f, indent=4)

def save_summary(topic: str, summary: str) -> str:
    data = read_data()
    data["summaries"][topic] = summary
    write_data(data)
    return f"Summary for '{topic}' saved successfully."

def get_summary(topic: str) -> str:
    data = read_data()
    return data.get("summaries", {}).get(topic, f"No summary found for '{topic}'.")

def save_quiz(topic: str, quiz: Dict[str, Any]) -> str:
    data = read_data()
    data["quizzes"][topic] = quiz
    write_data(data)
    return f"Quiz for '{topic}' saved successfully."

def get_quiz(topic: str) -> Dict[str, Any]:
    data = read_data()
    return data.get("quizzes", {}).get(topic, {"error": f"No quiz found for '{topic}'."})

def save_pdf(file_path: str) -> str:
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(upload_folder, file_name)
    
    try:
        with open(file_path, 'rb') as f_in:
            with open(destination_path, 'wb') as f_out:
                f_out.write(f_in.read())
        return f"PDF '{file_name}' saved successfully to '{upload_folder}'."
    except Exception as e:
        return f"Error saving PDF: {e}"

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"
