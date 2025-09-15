iimport streamlit as st

st.title("تطبيق تذكير الأدوية البسيط")

# التأكد من وجود قائمة الأدوية في الجلسة
if "meds" not in st.session_state:
    st.session_state.meds = []

# نموذج لإضافة دواء
with st.form("add_medicine"):
    med_name = st.text_input("اسم الدواء")
    doses_per_day = st.number_input("عدد الجرعات في اليوم", min_value=1, max_value=10, step=1)
    submit = st.form_submit_button("أضف الدواء")

    if submit:
        st.session_state.meds.append({"name": med_name, "doses": doses_per_day})
        st.success(f"تم إضافة {med_name} بنجاح!")

# عرض قائمة الأدوية
st.subheader("قائمة الأدوية")
for i, med in enumerate(st.session_state.meds):
    st.write(f"{i+1}. {med['name']} - {med['doses']} جرعات في اليوم")
