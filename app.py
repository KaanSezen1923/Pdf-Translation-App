import streamlit as st
import os
from dotenv import load_dotenv
from mistralai import Mistral
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
mistral_api_key = os.getenv("OCR_API_KEY")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        api_key=gemini_api_key,
    )
except Exception as e:
    st.error(f"Gemini API başlatılamadı: {e}")
    st.stop()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a professional translator specializing in English to Turkish translation. Translate the provided English text to Turkish accurately, preserving technical terms and context where applicable. Remove any LaTeX or HTML markup (e.g., <br>, $, {{}}, \dagger) and focus on the plain text. For example:
            User: 'I can't remember' -> Assistant: Hatırlamıyorum.
            User: 'I don't like you' -> Assistant: Seni sevmiyorum.
            User: 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks' -> Assistant: Baskın dizge dönüştürme modelleri, karmaşık yinelemeli veya evrişimli sinir ağlarına dayanır.
            User: 'Ashish Vaswani*<br>Google Brain<br>avaswani@google.com' -> Assistant: Ashish Vaswani, Google Brain, avaswani@google.com
            User: 'Aidan N. Gomez* ${{}}^{{\dagger}}$<br>University of Toronto<br>aidan@cs.toronto.edu' -> Assistant: Aidan N. Gomez, Toronto Üniversitesi, aidan@cs.toronto.edu""",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm


try:
    client = Mistral(api_key=mistral_api_key)
except Exception as e:
    st.error(f"Mistral API başlatılamadı: {e}")
    st.stop()


def clean_text(text):
    text = re.sub(r'\${.*?}\$', '', text) 
    text = re.sub(r'\$\{.*?\}\^\{.*?\}', '', text)  
    text = re.sub(r'\\\[.*?\\\]', '', text)  
    text = re.sub(r'[<][^>]+[>]', '', text) 
    text = re.sub(r'\s+', ' ', text)  
    text = text.replace('*', '').replace('`', '').replace('#', '') 
    return text.strip()


st.title("PDF  Çeviri Uygulaması")
st.write("İngilizce PDF dosyanızı yükleyin, Türkçe'ye çevrilsin ve PDF olarak kaydedilsin!")


if 'translated_texts' not in st.session_state:
    st.session_state.translated_texts = None
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False


uploaded_file = st.file_uploader("PDF Dosyası Seçin", type=["pdf"])

if uploaded_file is not None and not st.session_state.file_processed:
   
    try:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
    except Exception as e:
        st.error(f"Dosya kaydedilemedi: {e}")
        st.stop()
    
   
    st.write("Dosya yükleniyor...")
    try:
        mistral_file = client.files.upload(
            file={
                "file_name": uploaded_file.name,
                "content": open("temp.pdf", "rb")
            },
            purpose="ocr"
        )
    except Exception as e:
        st.error(f"Dosya Mistral API'ye yüklenemedi: {e}")
        st.stop()
    
    
    try:
        file_url = client.files.get_signed_url(file_id=mistral_file.id)
    except Exception as e:
        st.error(f"Dosya URL'si alınamadı: {e}")
        st.stop()
    
   
    st.write("OCR işlemi başlatılıyor...")
    try:
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": file_url.url
            },
            include_image_base64=True,
        )
    except Exception as e:
        st.error(f"OCR işlemi başarısız: {e}")
        st.stop()
    
   
    texts = []
    for page in response.pages:
        cleaned_text = clean_text(page.markdown)
        texts.append(cleaned_text)
    
    
    st.write("Metinler çevriliyor...")
    translated_texts = []
    progress_bar = st.progress(0)
    for i, text in enumerate(texts):
        try:
            if not text.strip(): 
                translated_texts.append("[Boş Sayfa]")
                continue
            response = chain.invoke({"input": text})
            cleaned_translation = clean_text(response.content)
            translated_texts.append(cleaned_translation)
        except Exception as e:
            st.warning(f"Sayfa {i+1} çevrilemedi: {e}")
            translated_texts.append(f"[Çeviri Hatası: {e}]")
        progress_bar.progress((i + 1) / len(texts))
    
  
    st.session_state.translated_texts = translated_texts
    st.session_state.file_processed = True
    
    
    pdf_path = "translated_output.pdf"
    try:
        
        font_name = "Helvetica"  
        try:
            if os.path.exists("DejaVuSans.ttf"):
                pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
                font_name = "DejaVuSans"
            else:
                st.warning("DejaVuSans.ttf bulunamadı. Varsayılan font (Helvetica) kullanılacak.")
        except Exception as e:
            st.warning(f"DejaVuSans fontu yüklenemedi: {e}. Varsayılan font (Helvetica) kullanılacak.")
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont(font_name, 12)
        y_position = 750 
        max_width = 500   
        
        for text in translated_texts:
            for line in text.split("\n"):
                
                while len(line) > 0:
                    width = c.stringWidth(line, font_name, 12)
                    if width <= max_width:
                        c.drawString(40, y_position, line)
                        break
                    else:
                        split_point = len(line)
                        while c.stringWidth(line[:split_point], font_name, 12) > max_width and split_point > 0:
                            split_point -= 1
                        c.drawString(40, y_position, line[:split_point])
                        line = line[split_point:]
                    y_position -= 15  
                    if y_position < 50: 
                        c.showPage()
                        c.setFont(font_name, 12)
                        y_position = 750
            y_position -= 15  
            if y_position < 50:
                c.showPage()
                c.setFont(font_name, 12)
                y_position = 750
        
        c.showPage()
        c.save()
        
        
        st.session_state.pdf_path = pdf_path
    
    except Exception as e:
        st.error(f"PDF oluşturulamadı: {e}")
        st.session_state.file_processed = False


if st.session_state.translated_texts is not None:
    st.write("Çeviri tamamlandı!")
    
    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="Çevrilen PDF'yi İndir",
                data=f,
                file_name="translated_output.pdf",
                mime="application/pdf",
                key="download_pdf"
            )