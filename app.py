import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Math to LaTeX DZ", layout="centered")

st.sidebar.title("إعدادات الموقع")
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك:", type="password")

st.title("محول التمارين إلى LaTeX 🇩🇿")
st.write("ارفع صورة التمرين وسأقوم بتحويلها لك لملف جاهز لـ Overleaf")

uploaded_file = st.file_uploader("اختر صورة التمرين...", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        image = Image.open(uploaded_file)
        st.image(image, caption='التمرين المرفوع', use_container_width=True)
        
        if st.button('توليد الملف وتحميله'):
            with st.spinner('جاري التحليل...'):
                # استخدام الاسم العام المباشر لحل خطأ 404 نهائياً
                model = genai.GenerativeModel('gemini-pro-vision') 
                # ملاحظة: إذا استمر الخطأ، جرب تغيير السطر أعلاه فقط إلى: model = genai.GenerativeModel('gemini-1.5-flash-8b')
                
                prompt = "Extract math exercise from image. Format as a complete XeLaTeX document using Amiri font. Output ONLY code."
                response = model.generate_content([prompt, image])
                latex_code = response.text
                
                st.code(latex_code, language='latex')
                
                st.download_button(
                    label="📥 تحميل ملف التمرين (.tex)",
                    data=latex_code,
                    file_name="exercise.tex",
                    mime="text/plain"
                )
                st.success("تم التوليد! حمل الملف وارفع في Overleaf.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
elif not api_key:
    st.warning("⚠️ يرجى وضع مفتاح API في القائمة الجانبية (على اليسار).")
    
