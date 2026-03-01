import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Math to LaTeX DZ", layout="centered")

# خانة وضع المفتاح في القائمة الجانبية
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك:", type="password")

st.title("محول التمارين إلى LaTeX 🇩🇿")
st.write("ارفع صورة التمرين وسأقوم بتحويلها لك بتنسيق LaTeX")

uploaded_file = st.file_uploader("اختر صورة التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_container_width=True)
    
    if st.button('توليد الكود'):
        with st.spinner('جاري التحليل...'):
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Extract the math exercise from this image and format it into professional XeLaTeX code using Amiri font. Use Algerian education style."
            try:
                response = model.generate_content([prompt, image])
                st.code(response.text, language='latex')
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
elif not api_key:
    st.warning("⚠️ من فضلك ضع مفتاح API في القائمة الجانبية (على اليسار) لتتمكن من استخدام الموقع.")
