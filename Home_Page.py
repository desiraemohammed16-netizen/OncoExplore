import streamlit as st

st.set_page_config(page_title="OncoExplore", page_icon="🧬", layout="wide")

# AI-assisted styling and wording. Review and adjust according to course policy.
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.main {
    background: linear-gradient(180deg, #fffdf8 0%, #f7faf7 35%, #f2f8f6 100%);
}
.hero {
    background: linear-gradient(135deg, rgba(255,248,253,0.95), rgba(239,248,244,0.95));
    border: 1px solid #d9e8df;
    border-radius: 22px;
    padding: 1.5rem 1.7rem;
    box-shadow: 0 6px 20px rgba(100, 120, 110, 0.08);
}
.soft-card {
    background: rgba(255,255,255,0.78);
    border: 1px solid #e2ece7;
    border-radius: 18px;
    padding: 1rem 1.1rem;
    box-shadow: 0 4px 16px rgba(120, 140, 132, 0.07);
    min-height: 190px;
}
.note-box {
    background: #f5fbf8;
    border-left: 5px solid #8fae9d;
    border-radius: 10px;
    padding: 0.85rem 1rem;
}
.smallcaps {
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6f8b80;
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="smallcaps">CS 1301 · Web Development Lab 3</div>
    <h1 style="margin-bottom:0.25rem; color:#415d52;">🧬 OncoExplore</h1>
    <h3 style="margin-top:0; color:#6f877b; font-weight:500;">Cancer Clinical Trial Explorer</h3>
    <p style="font-size:1.05rem; color:#54685f;">
        Explore cancer research through interactive clinical trial data and learn about cancer biology with our educational research chatbot.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("**Team:** 70 | **Section:** C")
st.write("**Team members:** Desirae Mohammed and Melissa Thomas")
st.divider()

st.markdown("""
<div class="note-box">
<b>Project purpose:</b> OncoExplore helps students and curious users compare registered cancer studies using public data from ClinicalTrials.gov.
We created it at the intersection of biology, biomedical engineering, and computing.
</div>
""", unsafe_allow_html=True)

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("""
    <div class="soft-card">
        <h3 style="color:#50695e;">🔎 Clinical Trial Dashboard</h3>
        <p style="color:#5a6d65;">
            Explore clinical trial patterns for breast cancer, lung cancer, prostate cancer, and leukemia.
            Filter by cancer type and study status, then compare the changing visuals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Clinical_Trials.py", label="Open the dashboard", icon="📊")
with right:
    st.markdown("""
    <div class="soft-card">
        <h3 style="color:#50695e;">💬 Research Chatbot</h3>
        <p style="color:#5a6d65;">
            Use our themed chatbot to ask general questions about cancer research and clinical trials.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("Open the chatbot from the sidebar.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="soft-card">
        <h4 style="color:#5a6d65;">🧫 Scientific focus</h4>
        <p style="color:#667870;">Cancer biology, research systems, and how study data can be made easier to interpret.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="soft-card">
        <h4 style="color:#5a6d65;">📚 Data source</h4>
        <p style="color:#667870;">ClinicalTrials.gov, a public registry maintained by the U.S. National Library of Medicine.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="soft-card">
        <h4 style="color:#5a6d65;">⚠️ Reminder</h4>
        <p style="color:#667870;">This project is educational and not intended to give medical advice or judge treatment effectiveness.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("[Visit ClinicalTrials.gov](https://clinicaltrials.gov/)")
