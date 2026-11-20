import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# تنظیمات فایل ذخیره‌سازی
DATA_FILE = 'exam_data.json'

ADMIN_INFO = {
    "first_name": "نيلوفر",
    "last_name": "صفري مقدم",
    "class_number": "702",
    "national_id": "0971041369"
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# لیست سوالات استخراج شده از پیام‌های قبلی تو
questions = [
    {"q": "اگر طول پاندول ساده دو برابر شود، دوره تناوب آن چه تغییری می‌کند؟", "options": ["۲ برابر می‌شود", "۴ برابر می‌شود", "بدون تغییر می‌ماند", "نصف می‌شود"], "a": "۲ برابر می‌شود", "ex": "دوره تناوب با جذر طول رابطه دارد، پس با دو برابر شدن طول، دوره تناوب هم ۲ برابر می‌شود."},
    {"q": "در یک فنر، نیروی بازگرداننده با چه رابطه‌ای دارد؟", "options": ["مستقیم با جابجایی", "معکوس با جابجایی", "مربع جابجایی", "هیچکدام"], "a": "مستقیم با جابجایی", "ex": "طبق قانون هوک، نیرو با جابجایی رابطه مستقیم دارد (F = -kx)."},
    {"q": "کار انجام شده توسط نیروی اصطکاک معمولاً چگونه است؟", "options": ["مثبت", "صفر", "منفی", "بی‌نهایت"], "a": "منفی", "ex": "نیروی اصطکاک در خلاف جهت حرکت است، پس کار آن منفی است."},
    {"q": "انرژی جنبشی یک جسم در صورت دو برابر شدن سرعت، چند برابر می‌شود؟", "options": ["۲ برابر", "۴ برابر", "۸ برابر", "بدون تغییر"], "a": "۴ برابر", "ex": "چون سرعت در توان ۲ است (v²)، با دو برابر شدن سرعت، انرژی ۴ برابر می‌شود."},
    {"q": "واحد اندازه گیری توان چیست؟", "options": ["ژول", "نیوتن", "وات", "پاسکال"], "a": "وات", "ex": "توان یعنی نرخ انجام کار در واحد زمان که با وات اندازه‌گیری می‌شود."},
    {"q": "اگر جابجایی صفر باشد، کار انجام شده چقدر است؟", "options": ["بسیار زیاد", "بیشینه", "صفر", "منفی"], "a": "صفر", "ex": "کار برابر نیرو در جابجایی است؛ اگر جابجایی نباشد، کار صفر است."},
    {"q": "انرژی پتانسیل گرانشی به چه عواملی بستگی دارد؟", "options": ["جرم، شتاب و ارتفاع", "جرم و سرعت", "فقط ارتفاع", "فقط جرم"], "a": "جرم، شتاب و ارتفاع", "ex": "فرمول انرژی پتانسیل gh است."},
    {"q": "در سیستم‌های بدون اصطکاک، انرژی مکانیکی چگونه است؟", "options": ["کاهش می‌یابد", "افزایش می‌یابد", "ثابت می‌ماند", "صفر می‌شود"], "a": "ثابت می‌ماند", "ex": "در نبود اصطکاک، مجموع انرژی جنبشی و پتانسیل همیشه ثابت است."},
    {"q": "واحد نیرو در سیستم SI چیست؟", "options": ["ژول", "وات", "نیوتن", "پاسکال"], "a": "نیوتن", "ex": "نیرو با واحد نیوتن اندازه‌گیری می‌شود."},
    {"q": "اگر یک جسم از ارتفاع ثابت رها شود، انرژی پتانسیل آن چگونه تغییر می‌کند؟", "options": ["افزایش می‌یابد", "کاهش می‌یابد", "ثابت می‌ماند", "صفر می‌شود"], "a": "کاهش می‌یابد", "ex": "با کاهش ارتفاع، انرژی پتانسیل کاهش و انرژی جنبشی افزایش می‌یابد."},
    {"q": "اصطلاح 'کار منفی' به چه معناست؟", "options": ["نیرو در جهت حرکت است", "نیرو در خلاف جهت حرکت است", "جسم حرکت نمی‌کند", "نیرو صفر است"], "a": "نیرو در خلاف جهت حرکت است", "ex": "وقتی زاویه نیرو و جابجایی ۹۰ درجه باشد کار صفر و اگر بیش از ۹۰ باشد کار منفی است."},
    {"q": "واحد جرم در سیستم SI چیست؟", "options": ["گرم", "کیلوگرم", "پوند", "تن"], "a": "کیلوگرم", "ex": "واحد استاندارد جرم در SI کیلوگرم است."},
    {"q": "توان برابر است با:", "options": ["کار تقسیم بر زمان", "نیرو ضرب در جابجایی", "جرم ضرب در شتاب", "کار ضرب در زمان"], "a": "کار تقسیم بر زمان", "ex": "تعریف توان، نرخ انجام کار در واحد زمان است."},
    {"q": "اگر جرم جسم دو برابر شود، انرژی جنبشی (با سرعت ثابت) چه می‌شود؟", "options": ["۲ برابر", "۴ برابر", "نصف می‌شود", "بدون تغییر"], "a": "۲ برابر", "ex": "از آنجا که انرژی جنبشی با جرم رابطه مستقیم دارد، با دو برابر شدن جرم، انرژی هم دو برابر می‌شود."},
    {"q": "کدام یک از موارد زیر یک کمیت نرده‌ای است؟", "options": ["سرعت", "نیرو", "جرم", "جابجایی"], "a": "جرم", "ex": "جرم یک کمیت نرده‌ای است و جهت ندارد."},
]

def main():
    st.set_page_config(page_title="آزمون آنلاین", layout="centered")
    
    # مدیریت وضعیت‌ها
    if 'stage' not in st.session_state:
        st.session_state.stage = 'login'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0

    # --- مرحله ورود ---
    if st.session_state.stage == 'login':
        st.title("ورود به آزمون")
        with st.form("login_form"):
            fname = st.text_input("نام")
            lname = st.text_input("نام خانوادگی")
            cnum = st.text_input("شماره کلاس")
            nid = st.text_input("کد ملی")
            submit = st.form_submit_button("شروع آزمون")

            if submit:
                if not (fname and lname and cnum and nid):
                    st.error("لطفاً تمام فیلدها را پر کنید.")
                else:
                    # ورود مخفی ادمین (بدون نمایش هیچ پیام یا دکمه‌ای)
                    if (fname == ADMIN_INFO["first_name"] and 
                        lname == ADMIN_INFO["last_name"] and 
                        cnum == ADMIN_INFO["class_number"] and 
                        nid == ADMIN_INFO["national_id"]):
                        st.session_state.stage = 'admin_panel'
                        st.rerun()
                    else:
                        all_data = load_data()
                        exists = any(d['national_id'] == nid for d in all_data)
                        if exists:
                            st.error("این کد ملی قبلاً آزمون داده است.")
                        else:
                            st.session_state.user_data = {
                                "first_name": fname, "last_name": lname,
                                "class_number": cnum, "national_id": nid
                            }
                            st.session_state.score = 0
                            st.session_state.current_q = 0
                            st.session_state.stage = 'quiz'
                            st.rerun()

    # --- پنل مدیریت (فقط برای تو باز می‌شود) ---
    elif st.session_state.stage == 'admin_panel':
        st.title("گزارشات ادمین")
        data = load_data()
        if not data:
            st.warning("هنوز هیچ آزمونی ثبت نشده است.")
        else:
            df = pd.DataFrame(data)
            st.subheader("لیست کامل شرکت‌کنندگان")
            st.dataframe(df)
            
            st.subheader("رتبه‌بندی بر اساس درصد موفقیت")
            df['percentage'] = (df['score'] / len(questions)) * 100
            df_sorted = df.sort_values(by='percentage', ascending=False)
            st.table(df_sorted[['first_name', 'last_name', 'class_number', 'score', 'percentage']])
        
        if st.button("خروج از پنل"):
            st.session_state.stage = 'login'
            st.rerun()

    # --- مرحله آزمون ---
    elif st.session_state.stage == 'quiz':
        q_idx = st.session_state.current_q
        
        if q_idx < len(questions):
            st.write(f"### سوال {q_idx + 1} از {len(questions)}")
            q_data = questions[q_idx]
            st.subheader(q_data["q"])
            
            answer = st.radio("گزینه صحیح را انتخاب کنید:", q_data["options"], key=f"q_{q_idx}")
            
            if st.button("ثبت پاسخ"):
                if answer == q_data["a"]:
                    st.success(f"آفرین! درست بود. {q_data['ex']}")
                    st.session_state.score += 1
                else:
                    st.error(f"اشتباه بود. پاسخ صحیح: {q_data['a']}. {q_data['ex']}")
                
                st.session_state.current_q += 1
                st.info("برای رفتن به سوال بعدی روی دکمه زیر کلیک کن.")
                if st.button("سوال بعدی ➔"):
                    st.rerun()
        else:
            # پایان آزمون
            final_score = st.session_state.score
            percentage = (final_score / len(questions)) * 100
            st.balloons()
            st.success(f"آزمون تمام شد! نمره شما: {final_score} از {len(questions)} ({percentage:.1f}%)")
            
            # ذخیره در فایل
            all_data = load_data()
            entry = {
                **st.session_state.user_data,
                "score": final_score,
                "percentage": round(percentage, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            all_data.append(entry)
            save_data(all_data)
            
            if st.button("خروج از آزمون"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()
