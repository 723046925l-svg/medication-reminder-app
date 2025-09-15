import streamlit as st
from datetime import datetime, time, timedelta
import time as t

st.set_page_config(page_title="تطبيق تذكير الأدوية", layout="centered")

st.title("💊 تطبيق تذكير الأدوية المتكامل")

# حالة الجلسة: قائمة الأدوية
if "medications" not in st.session_state:
    st.session_state.medications = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# وظيفة إزالة دواء
def remove_med(index):
    st.session_state.medications.pop(index)
    st.experimental_rerun()

# وظيفة تعديل دواء
def start_edit_med(index):
    st.session_state.edit_index = index
    st.experimental_rerun()

def save_edit_med(name, dose_times):
    idx = st.session_state.edit_index
    st.session_state.medications[idx] = {
        "name": name.strip(),
        "times": dose_times
    }
    st.session_state.edit_index = None
    st.experimental_rerun()

# --- نموذج إضافة / تعديل دواء ---
if st.session_state.edit_index is not None:
    med = st.session_state.medications[st.session_state.edit_index]
    st.subheader(f"✏️ تعديل الدواء: {med['name']}")
    with st.form("edit_med_form"):
        name = st.text_input("اسم الدواء", value=med["name"])
        doses_per_day = len(med["times"])
        dose_times = []
        st.markdown("🕒 أوقات الجرعات:")
        for i in range(doses_per_day):
            dose_time = st.time_input(f"الجرعة رقم {i+1}", value=med["times"][i])
            dose_times.append(dose_time)

        if st.form_submit_button("حفظ التعديل"):
            if not name.strip():
                st.error("يرجى إدخال اسم الدواء")
            else:
                save_edit_med(name, dose_times)
    if st.button("إلغاء التعديل"):
        st.session_state.edit_index = None
        st.experimental_rerun()

else:
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

# --- عرض قائمة الأدوية مع أزرار حذف وتعديل ---
st.subheader("📝 قائمة الأدوية")
if not st.session_state.medications:
    st.info("لا توجد أدوية مضافة حالياً.")
else:
    for idx, med in enumerate(st.session_state.medications):
        with st.container():
            cols = st.columns([6,1,1])
            cols[0].markdown(f"**{idx+1}. {med['name']}**")
            if cols[1].button("✏️ تعديل", key=f"edit_{idx}"):
                start_edit_med(idx)
            if cols[2].button("❌ حذف", key=f"del_{idx}"):
                remove_med(idx)
        for t_idx, t_time in enumerate(med['times']):
            st.markdown(f" - الجرعة {t_idx+1}: ⏰ {t_time.strftime('%H:%M')}")

# --- الجرعة القادمة والوقت المتبقي ---
st.subheader("⏳ الجرعة القادمة")
now = datetime.now()
next_dose_datetime = None
next_med_name = None
next_dose_time = None

for med in st.session_state.medications:
    for dose_time in med["times"]:
        dose_dt = datetime.combine(now.date(), dose_time)
        if dose_dt < now:
            dose_dt += timedelta(days=1)
        if (next_dose_datetime is None) or (dose_dt < next_dose_datetime):
            next_dose_datetime = dose_dt
            next_med_name = med["name"]
            next_dose_time = dose_time

if next_dose_datetime:
    remaining = next_dose_datetime - now
    st.success(f"💊 الجرعة القادمة: {next_med_name} الساعة {next_dose_time.strftime('%H:%M')} - تبقى {str(remaining).split('.')[0]}")

    # عداد تنازلي تلقائي للجرعة القادمة
    countdown_placeholder = st.empty()
    seconds_left = int(remaining.total_seconds())
    if seconds_left > 0:
        for sec in range(seconds_left, -1, -1):
            mins, secs = divmod(sec, 60)
            countdown_placeholder.info(f"⏳ تبقى: {mins:02d}:{secs:02d} دقيقة")
            t.sleep(1)
        countdown_placeholder.success("🚨 انتهى الوقت! خذ الجرعة الآن.")
else:
    if st.session_state.medications:
        st.warning("✔️ كل الجرعات لليوم انتهت! 🥳")
    else:
        st.info("لا توجد أدوية حتى الآن.")

# --- ملخص يومي لجميع الجرعات ---
st.subheader("📋 ملخص يومي للأدوية والجرعات")
if st.session_state.medications:
    for med in st.session_state.medications:
        st.markdown(f"**{med['name']}**")
        for t_idx, t_time in enumerate(med['times']):
            st.markdown(f" - الجرعة {t_idx+1}: ⏰ {t_time.strftime('%H:%M')}")
else:
    st.info("لا توجد أدوية حتى الآن.")

# --- تنبيه صوتي عند الجرعة القادمة ---
st.subheader("🔔 تنبيه صوتي عند وقت الجرعة")
if next_dose_datetime:
    alert_html = """
    <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
        Your browser does not support the audio element.
    </audio>
    """
    if remaining.total_seconds() <= 10:
        st.markdown(alert_html, unsafe_allow_html=True)

