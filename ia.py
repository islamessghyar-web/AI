import streamlit as st
import google.generativeai as genai
import os

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="صانع المواقع بالذكاء الاصطناعي",
    page_icon="✨",
    layout="wide"
)

# 2. العنوان والتنسيقات
st.title("✨ صانع المواقع بالذكاء الاصطناعي")
st.write("اكتب وصف الموقع الذي تريده، وسيقوم Gemini بتصميم وبناء الكود لك فوراً!")

# 3. جلب المفتاح من إعدادات البيئة أو إتاحة إدخاله يدوياً في الشريط الجانبي
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")
    st.sidebar.markdown("[🔑 احصل على مفتاح مجاني من Google AI Studio](https://aistudio.google.com/)")

# 4. واجهة إدخال الوصف
prompt = st.text_area(
    "وصف الموقع:", 
    height=120,
    placeholder="مثال: موقع صفحة هبوط لمطعم بيتزا حديث مع قائمة طعام، أزرار طلب متجاوبة، وألوان داكنة..."
)

# 5. زر الإنشاء والتعامل مع الطلب
if st.button("إنشاء الموقع 🚀", use_container_width=True):
    if not api_key:
        st.error("❌ يرجى إدخال مفتاح Gemini API للاستمرار.")
    elif not prompt:
        st.warning("⚠️ يرجى كتابة وصف للموقع أولاً.")
    else:
        with st.spinner("جاري تصميم وبناء كود الموقع بواسطة Gemini AI... ⏳"):
            try:
                # تهيئة نموذج Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-3.1-Pro')
                
                # توجيه النماذج للحصول على كود نقي ومستقل
                full_prompt = (
                    f"أنت مطور مواقع محترف. انشئ كود HTML كامل يحتوي على CSS و JavaScript مدمجين "
                    f"داخله لبناء هذا الموقع: {prompt}. "
                    f"قم بإرجاع كود HTML فقط، بدون أي شرح جانبي وبدون استخدام أوسمة الماركداون (لا تضع ```html)."
                )
                
                response = model.generate_content(full_prompt)
                
                # تنظيف النتيجة
                code = response.text.replace("```html", "").replace("```", "").strip()
                
                st.success("تم إنشاء الموقع بنجاح! 🎉")
                
                # عرض المعاينة الحية للموقع
                st.subheader("🖥️ المعاينة الحية للموقع:")
                st.components.v1.html(code, height=600, scrolling=True)
                
                # زر تنزيل الملف جاهز للفتح في المتصفح
                st.download_button(
                    label="📥 تحميل ملف الموقع (index.html)",
                    data=code,
                    file_name="index.html",
                    mime="text/html",
                    use_container_width=True
                )
                
                # إتاحة نسخ الكود
                with st.expander("📝 عرض كود HTML المصدر"):
                    st.code(code, language="html")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
