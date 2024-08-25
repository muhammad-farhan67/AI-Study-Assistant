# ThinkQuest 🤖📚

An intelligent study companion powered by AI to help students with various subjects and topics.

## 🚀 Features

- Text-based Q&A
- Image processing and analysis
- PDF text extraction and analysis
- Topic-specific hints (General, Coding, Math, Science)
- Chat history for each input type

## 🛠️ Tech Stack

- Python 3.7+
- Streamlit
- Groq API
- PyTesseract (OCR)
- PyMuPDF (PDF processing)

## 📚 Libraries

- streamlit
- groq
- pytesseract
- Pillow (PIL)
- PyMuPDF (fitz)
- requests

## 🏗️ How to Use the Code

1. Clone the repository:
   ```
   git clone https://github.com/muhammad-farhan67/AI-Study-Assistant.git
   cd AI-Study-Assistant
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Groq API key:
   - Create a `.streamlit/secrets.toml` file in your project directory
   - Add your Groq API key to the file:
     ```
     GROQ_API_KEY = "your-api-key-here"
     ```

4. Install Tesseract OCR:
   - For Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - For macOS: `brew install tesseract`
   - For Linux: `sudo apt-get install tesseract-ocr`

5. Update the Tesseract path in the code if necessary:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'path/to/tesseract'
   ```
6. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## 🚀 How to Deploy on Streamlit

1. Create a Streamlit account at [streamlit.io](https://streamlit.io/)

2. Connect your GitHub repository to Streamlit

3. Create a new app and select your repository

4. Add your Groq API key to the Streamlit secrets:
   - Go to your app settings
   - Navigate to the "Secrets" section
   - Add your Groq API key as `GROQ_API_KEY`

5. Deploy your app

6. Your AI Study Assistant is now live and accessible via the provided Streamlit URL!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/muhammad-farhan67/AI-Study-Assistant/issues).

## 📝 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 🙏 Acknowledgements

- Groq for providing the AI model API
- Streamlit for the awesome web app framework
- PyTesseract and PyMuPDF for image and PDF processing capabilities
```
