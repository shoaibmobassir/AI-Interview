# AI-Powered Interview Assistant  

The AI-Powered Interview Assistant is a versatile tool designed to simulate and analyze interview interactions. It integrates modern AI models and Python libraries to automate tasks like generating questions, recording responses, and evaluating answers.  

## Features  
- **Resume Parsing**: Extracts data from PDF resumes.  
- **Tailored Question Generation**: Creates specific questions based on resumes.  
- **Audio/Video Recording**: Captures candidate responses.  
- **Transcription**: Converts audio to text using Whisper AI.  
- **Text-to-Speech**: Reads questions aloud with Google TTS.  
- **Interactive Workflow**: Offers dynamic control via keyboard inputs.  

## Installation  
1. Clone the repository:  
   ```bash  
   git clone <repository_url>  
   cd <repository_folder>  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
3. Configure environment variables:  
   - Create a `.env` file and add:  
     ```  
     GROQ_API_KEY=your_groq_api_key  
     ```  

## Usage  
1. Save your resume as a PDF file.  
2. Run the application:  
   ```bash  
   python main.py  
   ```  
3. Interact with the system:  
   - Listen to generated questions.  
   - Record audio and video responses.  
   - View transcriptions in the `output/` folder.  

## Dependencies  
- **Audio/Video**: `sounddevice`, `opencv-python`  
- **NLP**: `transformers`, `faster-whisper`, `groq`  
- **Utilities**: `python-dotenv`, `pdfplumber`, `gtts`  

## File Structure  
```  
project/  
├── transcription_module.py    # Handles recording and transcription  
├── speech_module.py           # Converts text to speech  
├── ques_genera.py             # Generates questions  
├── final.py                   # Manages workflow  
├── main.py                    # Entry point  
├── requirements.txt           # Dependencies  
├── .env.example               # Environment variable example  
└── output/                    # Stores results  
```  

## Contributing  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature-name`.  
3. Commit changes: `git commit -m "Add feature description"`.  
4. Push changes: `git push origin feature-name`.  
5. Open a pull request.  
