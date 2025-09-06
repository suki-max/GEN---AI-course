# dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json, os

# 🛠️ Setup
st.set_page_config(page_title="Chatbot Analytics", layout="wide")
APP_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(APP_DIR, 'analytics_data.json')

# 📁 Load data
if not os.path.exists(json_file):
    st.error(f"analytics_data.json not found at {json_file}")
    st.stop()
analytics = json.load(open(json_file))

# 🎨 Custom CSS
st.markdown(
    """
    <style>
    .metric-label { font-size: 0.95rem; color: #555; }
    .metric-value { font-size: 1.8rem; font-weight: bold; }
    .stButton>button { background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 🏷️ Header and metrics
st.header("🤖 Chatbot Analytics Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Queries", analytics['total_queries'])
col2.metric("Avg Satisfaction", f"{analytics['avg_satisfaction']:.2f} / 5")
most_topic = max(analytics['topic_distribution'], key=lambda k: analytics['topic_distribution'][k])
col3.metric("Top Topic", f"Topic {most_topic}", delta=f"{analytics['topic_distribution'][most_topic]}")

st.divider()

# 📊 Charts in two columns
c1, c2 = st.columns(2)
with c1:
    st.subheader("Topic Distribution")
    fig_topics = px.pie(
        values=list(analytics['topic_distribution'].values()),
        names=[f"Topic {k}" for k in analytics['topic_distribution']],
        color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_topics, use_container_width=True)

with c2:
    st.subheader("Satisfaction Ratings")
    sc = analytics['satisfaction_counts']
    fig_sat = px.bar(
        x=list(sc.keys()), y=list(sc.values()), 
        labels={'x':'Rating','y':'Count'},
        color=list(sc.keys()), color_continuous_scale='Viridis')
    st.plotly_chart(fig_sat, use_container_width=True)

# 🔍 Topic details area with expander
exp = st.expander("Show Topic Keywords")
with exp:
    for t in analytics['topics']:
        st.write(f"**Topic {t['topic']}:** {', '.join(t['words'])}")

# ⚙️ Footer & About
st.sidebar.title("About Dashboard")
st.sidebar.info(
    "This dashboard was built with Streamlit using best UI practices: "
    "wide layout, metrics, charts, expanders, and a sidebar for info."
)
