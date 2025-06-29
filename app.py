import streamlit as st
import asyncio
from core import run_qa_agent, run_comprehensive_disease_analysis, run_market_analysis, run_government_schemes
from translations import translations

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="AgriBharat",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- THE "NATURAL ELEGANCE" UI MAKEOVER ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;700&family=Noto+Serif+Devanagari:wght@400;700&family=Noto+Serif+Telugu:wght@400;700&family=Noto+Serif+Kannada:wght@400;700&family=Noto+Serif+Malayalam:wght@400;700&family=Noto+Serif+Tamil:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* --- CSS Variable Definitions: "Natural Elegance" Theme --- */
        :root {
            --primary-color: #4A6341; /* Deep, Natural Olive Green */
            --secondary-color: #8D6E63; /* Earthy, Warm Brown */
            --accent-color: #D4AF37; /* Muted Gold for Highlights */
            --background-color: #FDFBF5; /* Warm, Creamy Off-White */
            --card-background: #FFFFFF;
            --text-primary: #424242; /* Soft, Dark Brown-Gray */
            --text-secondary: #757575;
            --border-color: #D7CCC8; /* Light Brown-Gray */
            --font-family: 'Noto Serif', 'Noto Serif Devanagari', 'Noto Serif Telugu', 'Noto Serif Kannada', 'Noto Serif Malayalam', 'Noto Serif Tamil', sans-serif;
        }

        /* --- General Body & App Styling --- */
        html, body, .stApp {
            background-color: var(--background-color);
            color: var(--text-primary);
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            font-family: var(--font-family);
        }
        p, label {
            color: var(--text-secondary);
            font-family: var(--font-family);
            line-height: 1.7;
        }

        /* --- Main Title with Leaf Icon --- */
        .main-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 2rem 0 1rem 0;
        }
        .main-title h1 {
            font-size: 3.2rem;
            font-weight: 700;
            color: var(--primary-color);
        }
        .main-title img {
            height: 50px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.15rem;
            color: var(--text-secondary);
            margin-bottom: 2.5rem;
        }

        /* --- Sidebar Styling --- */
        [data-testid="stSidebar"] {
            background-color: var(--background-color);
            border-right: 1px solid var(--border-color);
        }
        [data-testid="stSidebar"] h2 {
            color: var(--primary-color);
            font-size: 1.6rem;
        }

        /* --- Tabs Styling: Underlined & Clean --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            border-bottom: 2px solid var(--border-color);
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 8px;
            font-weight: 600;
            color: var(--text-secondary);
            background-color: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--primary-color);
        }
        .stTabs [aria-selected="true"] {
            color: var(--primary-color) !important;
            font-weight: 700;
            border-bottom: 3px solid var(--primary-color);
        }

        /* --- Form, Inputs & Buttons Styling --- */
        .stForm {
            border: none;
            background-color: transparent;
            padding: 0;
        }
        .stTextInput label, .stFileUploader label, .stTextArea label {
            font-weight: 600;
            color: var(--text-primary);
        }
        .stTextInput input, .stTextArea textarea, .stFileUploader section {
            background-color: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            transition: all 0.2s ease-in-out;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(74, 99, 65, 0.2);
        }
        
        /* THE Primary Button */
        [data-testid="stFormSubmitButton"] button {
            background-color: var(--primary-color);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            width: 100%;
            font-size: 1.1rem;
            font-weight: 700;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px);
            background-color: #3B5034; /* Slightly darker green */
            box-shadow: 0 6px 20px rgba(74, 99, 65, 0.25);
        }
        
        /* Secondary 'Download' button */
        .stButton>button {
            border: 2px solid var(--primary-color);
            background-color: var(--card-background);
            color: var(--primary-color);
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 700;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        /* --- Response Card Styling --- */
        .response-card {
            background-color: var(--card-background);
            border-radius: 12px;
            padding: 2rem;
            margin-top: 2rem;
            border: 1px solid var(--border-color);
            border-left: 5px solid var(--primary-color);
            box-shadow: 0 4px 25px rgba(0,0,0,0.05);
        }
        .response-card h3 {
            color: var(--primary-color);
            font-size: 1.4rem;
            margin-bottom: 1rem;
        }
        .response-card p {
            color: var(--text-primary);
        }

        /* --- Section Headers --- */
        .section-header {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-primary);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.75rem;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }
        .history-header {
             margin-top: 4rem;
             text-align: center;
        }

        /* --- Footer --- */
        .footer { text-align: center; color: var(--text-secondary); margin-top: 4rem; padding: 2rem 0; border-top: 1px solid var(--border-color); }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"
if 'consultation_history' not in st.session_state:
    st.session_state.consultation_history = []

# Language selection in sidebar
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center;'>{translations[st.session_state.selected_language]['settings_header']}</h2>", unsafe_allow_html=True)
    language = st.selectbox(
        label=translations[st.session_state.selected_language]["select_language"],
        options=["English", "Hindi", "Telugu", "Kannada", "Malayalam", "Tamil"],
        key="language_select_unique",
        index=["English", "Hindi", "Telugu", "Kannada", "Malayalam", "Tamil"].index(st.session_state.selected_language),
        label_visibility="collapsed"
    )
    
    if language != st.session_state.selected_language:
        st.session_state.selected_language = language
        st.rerun()

# Get translations
t = translations[st.session_state.selected_language]

# --- App Title and Subtitle ---
st.markdown(f"""
    <div class="main-title">
        <span style="font-size: 2.8rem; margin-right: 1rem;">🌾</span>
        <h1>{t['title']}</h1>
        <span style="font-size: 2.8rem; margin-left: 1rem;">🚜</span>
    </div>
    <p class="subtitle">{t['subtitle']}</p>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"🌾 {t['text_query_tab']}",
    f"🌿 {t['image_analysis_tab']}",
    f"💰 {t['market_analysis_tab']}",
    f"📄 {t['government_schemes_tab']}"
])

# --- Crop Queries Tab ---
with tab1:
    st.markdown(f"<h2 class='section-header'>{t['text_query_title']}</h2>", unsafe_allow_html=True)
    with st.form(key="text_query_form"):
        user_question = st.text_area(label=t["text_input_label"], placeholder=t["text_input_placeholder"], key="text_query_input", height=120)
        submit_button = st.form_submit_button(label=t["submit_button"])

    if submit_button:
        if not user_question.strip():
            st.error(f"{t['error_prefix']} {t['no_question_error']}")
        else:
            with st.spinner(t["processing_question"]):
                try:
                    response = asyncio.run(run_qa_agent(user_question, st.session_state.selected_language))
                    st.markdown(f"""<div class="response-card"><h3>{t['response_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    st.session_state.consultation_history.append({"type": "crop_query", "question": user_question, "response": response, "language": st.session_state.selected_language})
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Disease Diagnosis Tab ---
with tab2:
    st.markdown(f"<h2 class='section-header'>{t['image_analysis_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['image_analysis_subtitle']}</p>", unsafe_allow_html=True)
    with st.form(key="image_analysis_form"):
        uploaded_image = st.file_uploader(label=t["image_upload_label"], type=["jpg", "jpeg", "png"], key="image_upload_unique")
        image_question = st.text_input(label=t["image_question_label"], placeholder=t["image_question_placeholder"], key="image_question_input")
        submit_image_button = st.form_submit_button(label=t["analyze_button"])

    if submit_image_button:
        if not uploaded_image:
            st.error(f"{t['error_prefix']} {t['no_image_error']}")
        else:
            with st.spinner(t["processing_image"]):
                try:
                    image_data = uploaded_image.read()
                    response = asyncio.run(run_comprehensive_disease_analysis(image_data=image_data, user_question=image_question if image_question else t["image_question_placeholder"], language=st.session_state.selected_language))
                    st.image(uploaded_image, caption=t["uploaded_image_caption"], use_column_width=True)
                    st.markdown(f"""<div class="response-card"><h3>{t['analysis_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    st.session_state.consultation_history.append({"type": "disease_analysis", "question": image_question if image_question else t["image_question_placeholder"], "response": response, "language": st.session_state.selected_language})
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Market Analysis Tab ---
with tab3:
    st.markdown(f"<h2 class='section-header'>{t['market_analysis_header']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['market_analysis_subtitle']}</p>", unsafe_allow_html=True)
    with st.form(key="market_analysis_form"):
        crop_name = st.text_input(label=t["crop_name_label"], placeholder=t["crop_name_placeholder"], key="crop_name_input")
        submit_market_button = st.form_submit_button(label=t["get_market_trends_button"])

    if submit_market_button:
        if not crop_name.strip():
            st.error(f"{t['error_prefix']} {t['no_crop_name_error']}")
        else:
            with st.spinner(t["processing_market"]):
                try:
                    response = asyncio.run(run_market_analysis(crop_name=crop_name, language=st.session_state.selected_language))
                    st.markdown(f"""<div class="response-card"><h3>{t['market_trends_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    st.session_state.consultation_history.append({"type": "market_analysis", "question": f"Market trends for {crop_name}", "response": response, "language": st.session_state.selected_language})
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Government Schemes Tab ---
with tab4:
    st.markdown(f"<h2 class='section-header'>{t['government_schemes_header']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{t['government_schemes_subtitle']}</p>", unsafe_allow_html=True)
    with st.form(key="schemes_form"):
        scheme_query = st.text_input(label=t["scheme_query_label"], placeholder=t["scheme_query_placeholder"], key="scheme_query_input")
        submit_scheme_button = st.form_submit_button(label=t["get_schemes_button"])

    if submit_scheme_button:
        if not scheme_query.strip():
            st.error(f"{t['error_prefix']} {t['no_scheme_query_error']}")
        else:
            with st.spinner(t["processing_schemes"]):
                try:
                    response = asyncio.run(run_government_schemes(scheme_query=scheme_query, language=st.session_state.selected_language))
                    st.markdown(f"""<div class="response-card"><h3>{t['schemes_title']}</h3><p>{response}</p></div>""", unsafe_allow_html=True)
                    st.session_state.consultation_history.append({"type": "government_schemes", "question": scheme_query, "response": response, "language": st.session_state.selected_language})
                except Exception as e:
                    st.error(f"{t['error_prefix']} {e}")

# --- Consultation History ---
st.markdown(f"<h2 class='section-header history-header'>{t['consultation_history_header']}</h2>", unsafe_allow_html=True)
if st.session_state.consultation_history:
    st.info(f"{t['total_consultations_label']}: {len(st.session_state.consultation_history)}")
    
    history_text = "\n\n".join([f"--- Consultation ---\nType: {h['type']}\nLanguage: {h['language']}\nQuestion: {h['question']}\n\nResponse:\n{h['response']}" for h in reversed(st.session_state.consultation_history)])
    
    st.download_button(
        label=f"💾 {t['download_history_button']}",
        data=history_text.encode('utf-8'),
        file_name="AgriBharat_Consultation_History.txt",
        mime="text/plain",
        key="download_report_button"
    )

else:
    st.info(t["no_history_message"])

# Footer
st.markdown(f"""<div class="footer">{t['footer']}</div>""", unsafe_allow_html=True)