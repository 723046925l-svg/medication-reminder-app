import streamlit as st
from datetime import datetime, time, timedelta
import time as t

st.set_page_config(page_title="تطبيق تذكير الأدوية", layout="centered")

st.title("💊 تطبيق تذكير الأدوية المتكامل")

# --- حالة الجلسة: قائمة الأدوية ---
if "medications" not in st.session_state:
    st.session_state.medications = []

# --- وظيفة لإزالة دواء حسب index ---
def remove_med(index):
    st.session_state.medications.pop(index)
    st.experimental_rerun()

# --- نموذج إضافة دواء جديد ---
with st.form("add_medication_form"):
    st.subheader("➕ أضف دواء جديد")
    name = st.text_input("اسم الدواء")
    doses_per_day = st.number_input("عدد الجرعات في اليوم", min_value=1, max_value=10, step=1)

    dose_times = []
    st.markdown("🕒 أوقات الجرعات:")
    for i in range(doses_per_day):
        dose_time = st.time_input(f"الجرعة رقم {i+1}", value=time(8 + i * 3))
        dose_times.append(dose_time)

    submitted = st.form_submit_button("أضف الدواء")
    if submitted:
        if not name.strip():
            st.error("يرجى إدخال اسم الدواء")
        else:
            st.session_state.medications.append({
                "name": name.strip(),
                "times": dose_times
            })
            st.success(f"تم إضافة الدواء: {name.strip()}")

# --- عرض قائمة الأدوية مع زر حذف ---
st.subheader("📝 قائمة الأدوية")
if not st.session_state.medications:
    st.info("لا توجد أدوية مضافة حالياً.")
else:
    for idx, med in enumerate(st.session_state.medications):
        with st.container():
            cols = st.columns([6,1])
            cols[0].markdown(f"**{idx+1}. {med['name']}**")
            cols[1].button("❌ حذف", key=f"del_{idx}", on_click=remove_med, args=(idx,))
        for t_idx, t_time in enumerate(med['times']):
            st.markdown(f" - الجرعة {t_idx+1}: ⏰ {t_time.strftime('%H:%M')}")

# --- الجرعة القادمة والوقت المتبقي ---
st.subheader("⏳ الجرعة القادمة")
now = datetime.now().time()
next_dose = None
next_med_name = None
next_dose_datetime = None

for med in st.session_state.medications:
    for dose_time in med["times"]:
        if dose_time > now:
            dose_dt = datetime.combine(datetime.today(), dose_time)
            if not next_dose_datetime or dose_dt < next_dose_datetime:
                next_dose_datetime = dose_dt
                next_med_name = med["name"]
                next_dose = dose_time

if next_dose:
    remaining = next_dose_datetime - datetime.now()
    st.success(f"💊 الجرعة القادمة: {next_med_name} الساعة {next_dose.strftime('%H:%M')} - تبقى {str(remaining).split('.')[0]}")
else:
    if st.session_state.medications:
        st.warning("✔️ كل الجرعات لليوم انتهت! 🥳")
    else:
        st.info("لا توجد أدوية حتى الآن.")

# --- عداد تنازلي تجريبي ---
st.subheader("⌛ عداد تنازلي تجريبي للجرعة")
countdown_seconds = st.slider("اختر وقت العد التنازلي (ثواني)", 5, 60, 10)
if st.button("ابدأ العداد"):
    placeholder = st.empty()
    for sec in range(countdown_seconds, 0, -1):
        placeholder.warning(f"⏳ تبقى: {sec} ثانية")
        t.sleep(1)
    placeholder.success("🚨 انتهى الوقت! خذ الجرعة الآن.")
