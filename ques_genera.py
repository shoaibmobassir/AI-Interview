# -*- coding: utf-8 -*-
"""ques_gen

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kdC4Jhcc157hVdMYzZGCiog34qHndKQ4
"""

import pdfplumber
from transformers import pipeline
import os
from dotenv import load_dotenv
from groq import Groq
import json


# Load environment variables from .env file
load_dotenv()

file_path = "E:\\ML DL\\AI_Interview\\Resume.pdf"


def generate_specific_questions(file_path, role):
    """
    Generates specific interview questions from the given resume.

    Parameters:
    file_path (str): The path to the resume PDF file.
    role (str): The role for which the questions are being generated. Default is "Data Scientist".

    Returns:
    str: JSON string of generated questions and answers.
    """
    # Load environment variables from .env file
    load_dotenv()
    role =role

    # Function to extract text from PDF
    def parse_pdf(file_path):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        return text.strip()

    resume = parse_pdf(file_path)

    # Determine the number of questions based on sections
    personal_count = 2
    project_count = 4
    skills_count = 2
    internship_count = 3

    # Create a dynamic prompt
    prompt_prefix = f"""{resume}
    --------------------------
    Generate {personal_count} personal questions, {project_count} project questions, {skills_count} skill questions, and {internship_count} internship questions for the role of {role}. 
    If internships are not available, add 2 more questions in the project section and 1 more question in the skills section.
    Generate questions and corresponding answers in medium to hard difficulty level.
    Strictly output in JSON format. The JSON should have the following format:"""

    # TypeScript interface
    sample_interface = """interface Response {
         data: Array<{ question: string, answer: string }>;
    }"""
    prompt = prompt_prefix + sample_interface

    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    client = Groq(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an experienced Interviewer."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )

    text = chat_completion.choices[0].message.content

    # Debugging: Print the raw response
    # print("Raw response from Groq API:")
    # print(text)

    # Extract the JSON string part from the text
    json_start = text.find("{")
    json_end = text.rfind("}") + 1
    json_str = text[json_start:json_end]

    # Debugging: Print the extracted JSON string
    # print("Extracted JSON string:")
    # print(json_str)

    # Validate the JSON string
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None

    simplified_data = [{"question": item["question"], "answer": item["answer"]} for item in data["data"]]
    simplified_json_str = json.dumps(simplified_data, indent=4)

    # Save to a JSON file
    with open('questions.json', 'w') as file:
        json.dump(simplified_data, file, indent=4)

    return simplified_json_str

if __name__ == "__main__":
    file_path = "shoib.cv.pdf"
    questions_json = generate_specific_questions(file_path,"Data Scientist")
    if questions_json:
        print("Generated Questions successfully")
        # print(questions_json)
