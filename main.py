import os
import subprocess
from ques_genera import generate_specific_questions

def main():
    # Define file paths and role
    resume_path = "C:\\Users\\ASUS\\Desktop\\final_AI\\shoib.cv.pdf"  # Path to your resume PDF
    json_filename = "transcription.json"
    role = "Data Scientist"
    
    # Generate questions and save them to transcription.json
    # print("Generating questions...")
    questions_json = generate_specific_questions(resume_path, role)
    if not questions_json:
        print("Failed to generate questions.")
        return
    print("Questions Generated")
    # print(f"Questions saved to {json_filename}")

    # Run final.py to ask questions, record audio, and video
    print("Starting final.py to ask questions and record responses...")
    result = subprocess.run(["python", "final.py"], capture_output=True, text=True)
    
    # print(result.stdout)
    
    if result.returncode == 0:
        print("Questions asked and recordings completed successfully.")
    else:
        print(f"Error occurred while running final.py:\n{result.stderr}")

if __name__ == "__main__":
    main()

