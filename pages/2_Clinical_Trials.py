# Lab 3: API data page
# AI-assisted draft: review and adapt the code according to course policy.
# Data analysis uses Python only, not an LLM.
import requests
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Clinical Trial Dashboard", page_icon="🧫", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.main {
    background: linear-gradient(180deg, #fffdf8 0%, #f8fcfa 45%, #f6faf8 100%);
}
.panel {
    background: rgba(255,255,255,0.78);
    border: 1px solid #e1ece5;
    border-radius: 18px;
    padding: 1rem 1.1rem;
    box-shadow: 0 4px 16px rgba(122, 140, 130, 0.08);
}
.hero {
    background: linear-gradient(135deg, rgba(249,241,248,0.95), rgba(241,249,245,0.95));
    border: 1px solid #d9e7df;
    border-radius: 22px;
    padding: 1.3rem 1.5rem;
    box-shadow: 0 6px 20px rgba(100, 120, 110, 0.08);
}
.smallcaps {
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #809286;
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)

API_URL = "https://clinicaltrials.gov/api/v2/studies"
CANCERS = ["Breast cancer", "Lung cancer", "Prostate cancer", "Leukemia"]
STATUSES = {"Recruiting": "RECRUITING", "Completed": "COMPLETED", "Terminated": "TERMINATED"}
COLORS = {"Recruiting": "#a8c9bd", "Completed": "#c8b6d9", "Terminated": "#e8b0b3"}
BAR_COLORS = ["#95b7a9", "#d9c8e8", "#b8d9cf", "#e9c0cf"]

@st.cache_data(ttl=3600)
def get_trial_count(cancer, status):
    """Return the total number of registered studies matching a search."""
    params = {
        "query.cond": cancer,
        "filter.overallStatus": STATUSES[status],
        "countTotal": "true",
        "pageSize": 1,
        "fields": "NCTId",
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data["totalCount"]


def get_counts(cancers, statuses):
    """Organize API counts into a nested dictionary by cancer and status."""
    counts = {}
    for cancer in cancers:
        counts[cancer] = {}
        for status in statuses:
            counts[cancer][status] = get_trial_count(cancer, status)
    return counts


def calculate_totals(counts):
    """Add selected status counts for each cancer type."""
    totals = {}
    for cancer in counts:
        total = 0
        for status in counts[cancer]:
            total += counts[cancer][status]
        totals[cancer] = total
    return totals


def calculate_percentages(counts, totals):
    """Calculate the percentage of each selected status within each cancer."""
    percentages = {}
    for cancer in counts:
        percentages[cancer] = {}
        for status in counts[cancer]:
            if totals[cancer] == 0:
                percentages[cancer][status] = 0
            else:
                percentages[cancer][status] = counts[cancer][status] / totals[cancer] * 100
    return percentages


st.markdown("""
<div class="hero">
    <div class="smallcaps">OncoExplore · Cancer research</div>
    <h1 style="margin-bottom:0.2rem; color:#4e685d;">🧫 Cancer Clinical Trial Dashboard</h1>
    <p style="font-size:1.02rem; color:#5f7369; margin-bottom:0;">
        Explore registered cancer studies by cancer type and study status using public data from ClinicalTrials.gov.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("Source: ClinicalTrials.gov API • counts cached for one hour")

left, right = st.columns(2)
with left:
    selected_cancers = st.multiselect("Cancer types", CANCERS, default=CANCERS)
with right:
    selected_statuses = st.multiselect("Study statuses", list(STATUSES), default=list(STATUSES))

if not selected_cancers or not selected_statuses:
    st.info("Select at least one cancer type and one study status.")
    st.stop()

try:
    with st.spinner("Retrieving clinical study counts..."):
        counts = get_counts(selected_cancers, selected_statuses)
except (requests.RequestException, ValueError, KeyError):
    st.error("ClinicalTrials.gov data could not be loaded. Please try again later.")
    st.stop()

totals = calculate_totals(counts)
percentages = calculate_percentages(counts, totals)

a, b, c = st.columns(3)
a.metric("Cancer types selected", len(selected_cancers))
b.metric("Study statuses selected", len(selected_statuses))
c.metric("Largest category count", format(max(totals.values()), ","))
st.caption("A study can match multiple cancer searches, so counts across cancer types may overlap.")

chart_left, chart_right = st.columns(2)
with chart_left:
    st.subheader("Study counts by cancer type")
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    bars = ax.bar(list(totals), list(totals.values()), color=BAR_COLORS[:len(totals)])
    ax.set_ylabel("Number of matching registered studies")
    ax.tick_params(axis="x", rotation=18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, fmt="%d", padding=3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Counts include only the study statuses selected above.")

with chart_right:
    st.subheader("Study status distribution")
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    bottoms = [0] * len(selected_cancers)
    for status in selected_statuses:
        values = []
        for cancer in selected_cancers:
            values.append(percentages[cancer][status])
        ax.bar(selected_cancers, values, bottom=bottoms, label=status, color=COLORS[status])
        for i in range(len(bottoms)):
            bottoms[i] += values[i]
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percentage of matching studies (%)")
    ax.tick_params(axis="x", rotation=18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=max(1, len(selected_statuses)))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Percentages are calculated within each cancer type using only selected statuses.")

st.subheader("Detailed results")
rows = []
for cancer in selected_cancers:
    row = {"Cancer type": cancer}
    for status in selected_statuses:
        row[status] = counts[cancer][status]
    row["Selected total"] = totals[cancer]
    rows.append(row)
st.dataframe(rows, hide_index=True, use_container_width=True)

st.markdown("""
<div class="panel">
    <h4 style="color:#5b6f65;">🔬 Interpreting the dashboard</h4>
    <p style="color:#697a72; margin-bottom:0.5rem;">
        Recruiting studies are currently seeking participants. Completed studies have finished, and terminated studies stopped early.
        These are not the only statuses in the registry.
    </p>
    <p style="color:#697a72; margin-bottom:0;">
        The registry includes different kinds of studies, and search matches are not exclusive to one cancer type. Study status does not measure treatment success.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("[ClinicalTrials.gov](https://clinicaltrials.gov/) | [API documentation](https://clinicaltrials.gov/data-api/api)")
