import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Math to LaTeX DZ", layout="centered")

# القائمة الجانبية
st.sidebar.title("إعدادات API")
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك:", type="password")

st.title("محول التمارين إلى LaTeX 🇩🇿")

uploaded_file = st.file_uploader("اختر صورة التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        image = Image.open(uploaded_file)
        st.image(image, caption='التمرين المرفوع', use_container_width=True)
        
        if st.button('توليد الملف وتحميله'):
            with st.spinner('جاري التحليل...'):
                # استخدام النموذج المستقر
                model = genai.GenerativeModel('gemini-1.5-flash') 
                
                prompt = "Extract math exercise from image. Format as a complete XeLaTeX document using Amiri font. Output ONLY LaTeX code."
                response = model.generate_content([prompt, image])
                latex_code = response.text
                
                clean_code = latex_code.replace("```latex", "").replace("```", "").strip()
                
                st.code(clean_code, language='latex')
                
                st.download_button(
                    label="📥 تحميل ملف التمرين (.tex)",
                    data=clean_code,
                    file_name="exercise.tex",
                    mime="text/plain"
                )
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
elif not api_key:
    st.warning("⚠️ يرجى وضع مفتاح API في القائمة الجانبية.")
    
