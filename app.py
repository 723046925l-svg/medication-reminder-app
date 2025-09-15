import streamlit as st

# تخزين الأدوية في جلسة العمل
if "drugs" not in st.session_state:
    st.session_state.drugs = []

st.title("💊 تطبيق تذكير الأدوية المتكامل")

with st.form("add_drug_form"):
    st.header("➕ أضف دواء جديد")
    drug_name = st.text_input("اسم الدواء")
    doses_per_day = st.number_input("عدد الجرعات في اليوم", min_value=1, max_value=10, value=1)
    
    dose_times = []
    for i in range(doses_per_day):
        time = st.time_input(f"الجرعة رقم {i+1}", key=f"time_{i}")
        dose_times.append(time)
    
    submitted = st.form_submit_button("أضف الدواء")
    if submitted:
        if drug_name.strip() == "":
            st.error("يرجى إدخال اسم الدواء")
        else:
            st.session_state.drugs.append({
                "name": drug_name,
                "doses": doses_per_day,
                "times": dose_times
            })
            st.success(f"تم إضافة الدواء {drug_name} بنجاح!")

st.markdown("---")
st.header("📋 قائمة الأدوية")

if len(st.session_state.drugs) == 0:
    st.info("لا توجد أدوية مضافة حالياً.")
else:
    for i, drug in enumerate(st.session_state.drugs):
        times_str = ", ".join([t.strftime("%H:%M") for t in drug["times"]])
        st.write(f"**{i+1}. {drug['name']}** - {drug['doses']} جرعات في اليوم - أوقات الجرعات: {times_str}")
        if st.button(f"حذف {drug['name']}", key=f"delete_{i}"):
            st.session_state.drugs.pop(i)
            st.experimental_rerun()
