import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Math to LaTeX DZ", layout="centered")

st.title("محول التمارين إلى ملفات جاهزة 🇩🇿")
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

uploaded_file = st.file_uploader("ارفع صورة التمرين هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption='التمرين المرفوع', use_container_width=True)
    
    if st.button('توليد الملف وتحميله'):
        with st.spinner('جاري التحويل...'):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = """Extract this math exercise and format it as a COMPLETE XeLaTeX document.
            Use: \usepackage[arabic]{babel}, \setmainfont{Amiri}.
            Output ONLY the LaTeX code."""
            
            try:
                response = model.generate_content([prompt, image])
                latex_code = response.text
                
                # زر التحميل المباشر
                st.download_button(
                    label="📥 تحميل ملف التمرين (.tex)",
                    data=latex_code,
                    file_name="exercise.tex",
                    mime="text/plain"
                )
                st.success("تم التوليد! حمل الملف وارفع في Overleaf لتحصل على PDF.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                
