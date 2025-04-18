PDF OCR and Translation Application
This project is a web-based application built with Streamlit that allows users to upload English PDF documents, extract text using Optical Character Recognition (OCR) via the Mistral AI API, translate the extracted text into Turkish using the Google Gemini API, and generate a downloadable PDF with the translated text. The application is designed to handle technical documents, such as academic papers, while preserving context and technical terms.
Features

PDF Upload: Upload English PDF files through a user-friendly Streamlit interface.
OCR Processing: Extract text from PDFs using Mistral AI's OCR API, including support for scanned documents and images.
Text Translation: Translate extracted text from English to Turkish using Google Gemini's language model, with LaTeX and HTML markup removed for clean output.
PDF Generation: Generate a new PDF containing the translated text, with proper formatting and support for Turkish characters.
Session Management: Efficiently handle user sessions to avoid redundant processing when downloading the translated PDF.
Error Handling: Robust error management for file uploads, API calls, and PDF generation.

Technologies Used

Python: Core programming language.
Streamlit: Web application framework for the user interface.
Mistral AI API: For OCR text extraction from PDFs.
Google Gemini API: For English-to-Turkish translation via LangChain.
ReportLab: For generating PDF files with translated text.
LangChain: For managing the translation prompt and API integration.
Regular Expressions (re): For cleaning LaTeX, HTML, and Markdown markup from text.

Installation
Prerequisites

Python 3.8 or higher
A valid Mistral AI API key for OCR
A valid Google Gemini API key for translation
The DejaVuSans.ttf font file for proper Turkish character support in PDFs (optional but recommended)

Steps

Clone the Repository:
git clone https://github.com/KaanSezen1923/pdf-translation-app.git
cd pdf-ocr-translation


Install Dependencies:Install the required Python packages using pip:
pip install streamlit mistralai langchain-google-genai reportlab


Set Up Environment Variables:Create a .env file in the project root and add your API keys:
GEMINI_API_KEY=your_gemini_api_key
OCR_API_KEY=your_mistral_api_key


Download the DejaVuSans Font (Optional):

Download the DejaVuSans.ttf font from DejaVu Fonts.
Place the DejaVuSans.ttf file in the project root directory to ensure proper rendering of Turkish characters in the generated PDF.
If the font is not added, the application will fall back to the Helvetica font, which may not fully support Turkish characters.


Run the Application:Start the Streamlit server:
streamlit run app.py

The application will open in your default web browser.


Usage

Upload a PDF:

Navigate to the application in your browser.
Use the file uploader to select an English PDF document (e.g., an academic paper like "Attention Is All You Need").


Process the PDF:

The application will:
Extract text from the PDF using Mistral AI's OCR API.
Clean the extracted text to remove LaTeX, HTML, and Markdown markup.
Translate the cleaned text into Turkish using Google Gemini.
Generate a new PDF containing the translated text.




Download the Translated PDF:

Once processing is complete, a "Download Translated PDF" button will appear.
Click the button to download the translated_output.pdf file containing the Turkish translation.


View Translated Text:

The translated text for each page is displayed in the Streamlit interface for review.



Project Structure
pdf-ocr-translation/
├── app.py                # Main application script
├── .env                  # Environment variables (API keys)
├── DejaVuSans.ttf        # Font file for Turkish character support (optional)
├── temp.pdf              # Temporary file for uploaded PDFs (generated during runtime)
├── translated_output.pdf # Generated PDF with translated text (generated during runtime)
└── README.md             # Project documentation

Notes

Font Support: For best results, include the DejaVuSans.ttf font to ensure proper rendering of Turkish characters (ş, ğ, ı, etc.). Without it, the application uses Helvetica, which may cause character display issues.
Technical Documents: The application is optimized for technical documents with LaTeX markup (e.g., academic papers). The clean_text function removes LaTeX and HTML artifacts to ensure clean translations.
Session Management: The application uses st.session_state to prevent redundant processing when downloading the PDF.
Error Handling: Comprehensive error handling is implemented for file uploads, API calls, and PDF generation. Check the Streamlit interface for warning or error messages.

Troubleshooting

Font Error: If you see an error like Can't open file "DejaVuSans.ttf", ensure the DejaVuSans.ttf file is in the project root. Alternatively, the application will fall back to Helvetica.
API Errors: Verify that your Mistral AI and Google Gemini API keys are valid and correctly set in the .env file.
Translation Issues: If translations are inaccurate, consider adding more examples to the prompt in app.py or switching to another translation model (e.g., DeepL).
Redundant Processing: If the application reprocesses the PDF when downloading, ensure st.session_state is correctly managing the file_processed flag.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request with a clear description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, please open an issue on GitHub or contact your-email@example.com.
