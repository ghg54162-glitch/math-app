import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Math to LaTeX DZ", layout="centered")

# القائمة الجانبية
st.sidebar.title("الإعدادات")
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك:", type="password")

st.title("محول التمارين إلى LaTeX 🇩🇿")
st.write("ارفع صورة التمرين وسأقوم بتحويلها لك لملف جاهز")

uploaded_file = st.file_uploader("اختر صورة التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_container_width=True)
    
    if st.button('توليد الملف وتحميله'):
        with st.spinner('جاري التحليل والتحويل...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "Extract math exercise from image. Format as a complete XeLaTeX document using Amiri font and Algerian style. Output ONLY code."
                response = model.generate_content([prompt, image])
                latex_code = response.text
                
                st.subheader("الكود الناتج:")
                st.code(latex_code, language='latex')
                
                # ميزة التحميل التي طلبتها
                st.download_button(
                    label="📥 تحميل ملف التمرين (.tex)",
                    data=latex_code,
                    file_name="exercise.tex",
                    mime="text/plain"
                )
                st.success("تم التوليد! حمل الملف وارفع في Overleaf.")
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
elif not api_key:
    st.warning("⚠️ من فضلك ضع مفتاح API في القائمة الجانبية (على اليسار) لتتمكن من استخدام الموقع.")
