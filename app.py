import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from modules.data_validator import validate_dataframe
from modules.data_cleaner import clean_data
from modules.preprocessor import preprocess_data
from modules.feature_engineer import engineer_features
from modules.eda import render_eda
from modules.sentiment import run_sentiment_analysis
from modules.issue_categorizer import categorize_issues
from modules.benchmarking import render_benchmarking
from modules.priority_scorer import score_priorities
from modules.action_mapper import map_actions
from modules.recommender import generate_recommendations
from modules.summarizer import summarize_feedback
from modules.insight_generator import generate_insights
from utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(
    page_title="Patient Satisfaction Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Glassmorphism CSS ─────────────────────────────────────────────────────────
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header glass-card">
    <div class="header-inner">
        <h1>🏥 Patient Satisfaction Intelligence Platform</h1>
        <p>AI-powered survey analytics · Sentiment · Benchmarking · Actionable Insights</p>
        <div class="header-badges">
            <span class="badge">HCL Internship Project</span>
            <span class="badge">Real-time Analysis</span>
            <span class="badge">NLP Powered</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏥</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", [
        "📤 Upload & Overview",
        "🔍 EDA",
        "💬 Sentiment Analysis",
        "🏷️ Issue Categories",
        "🏆 Dept Benchmarking",
        "⚡ Priority Scoring",
        "🗺️ Action Mapper",
        "💡 Recommendations",
        "📝 Feedback Summary",
        "🧠 AI Insights",
        "📊 Executive Dashboard"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(
        '<div class="sidebar-footer">Built for HCL Internship<br>Patient Satisfaction Analytics</div>',
        unsafe_allow_html=True
    )

# ── Session State ─────────────────────────────────────────────────────────────
for key in ["df_raw", "df", "insights"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Upload & Overview
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📤 Upload & Overview":
    st.markdown('<h2 class="section-title">📤 Upload Survey Data</h2>', unsafe_allow_html=True)

    # ── File uploader (correctly inside the if block) ─────────────────────────
    uploaded_file = st.file_uploader(
        "Drop your CSV or PDF here",
        type=["csv", "pdf"],
        help="CSV is recommended. PDF extraction may vary by layout."
    )

    if uploaded_file:
        logger.info(f"File uploaded: {uploaded_file.name}")

        with st.spinner("📥 Loading data..."):
            df_raw = load_data(uploaded_file)

        if df_raw is not None:
            # ── DATA VALIDATION ───────────────────────────────────────────────
            issues = validate_dataframe(df_raw)

            st.markdown(
                '<div class="validation-section-title">🔍 Validation Report</div>',
                unsafe_allow_html=True
            )
            if issues:
                for issue in issues:
                    st.markdown(
                        f'<div class="validation-warning">⚠️ {issue}</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(
                    '<div class="validation-warning">'
                    'ℹ️ Pipeline will still run — fix warnings above for best results.'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="validation-pass">'
                    '✅ Dataset validated — all 7 checks passed. Ready to analyse.'
                    '</div>',
                    unsafe_allow_html=True
                )
            # ─────────────────────────────────────────────────────────────────

            st.session_state.df_raw = df_raw
            logger.info(f"Data loaded: {df_raw.shape}")

            # ── Pipeline progress bar ─────────────────────────────────────────
            progress_bar = st.progress(0)
            status_text  = st.empty()

            pipeline = [
                ("🧹 Cleaning data...",             clean_data,             10),
                ("⚙️ Preprocessing text...",         preprocess_data,        25),
                ("🔧 Engineering features...",       engineer_features,      40),
                ("💬 Running sentiment analysis...", run_sentiment_analysis, 60),
                ("🏷️ Categorizing issues...",         categorize_issues,      75),
                ("⚡ Scoring priorities...",           score_priorities,       88),
                ("🗺️ Mapping actions...",              map_actions,            95),
            ]

            df_current = df_raw.copy()
            for label, func, pct in pipeline:
                status_text.markdown(
                    f'<div class="pipeline-step">{label}</div>',
                    unsafe_allow_html=True
                )
                progress_bar.progress(pct)
                df_current = func(df_current.copy())

            progress_bar.progress(100)
            status_text.empty()
            st.session_state.df = df_current

            # ── Generate AI insights ──────────────────────────────────────────
            with st.spinner("🧠 Generating AI insights..."):
                st.session_state.insights = generate_insights(df_current)

            logger.info("Full pipeline complete.")
            st.success("✅ Full pipeline complete! Navigate using the sidebar.")

            # ── KPI Cards ─────────────────────────────────────────────────────
            df = st.session_state.df
            kpi_data = [
                ("📋 Total Responses",
                 len(df)),
                ("⭐ Avg Rating",
                 f"{df['overall_rating'].mean():.2f}/5" if "overall_rating" in df.columns else "N/A"),
                ("😊 Positive %",
                 f"{(df['sentiment_label']=='Positive').mean()*100:.1f}%"
                 if "sentiment_label" in df.columns else "N/A"),
                ("🏥 Departments",
                 df["department"].nunique() if "department" in df.columns else "N/A"),
                ("🔴 Critical Issues",
                 int((df["priority_score"] >= 7).sum()) if "priority_score" in df.columns else "N/A"),
            ]
            cols = st.columns(5)
            for i, (label, value) in enumerate(kpi_data):
                with cols[i]:
                    st.markdown(f"""
                    <div class="kpi-card glass-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(50), use_container_width=True)

        else:
            st.error("❌ Could not load the file. Please check the format and try again.")

    else:
        # No file uploaded yet
        st.info("👆 Please upload a CSV or PDF file to begin analysis.")
        st.markdown("""
### 📋 Expected Columns (flexible — the system auto-detects):

| Column | Description |
|---|---|
| `patient_id` | Unique patient identifier |
| `department` | Hospital department |
| `overall_rating` | Rating 1–5 |
| `feedback_text` | Free-text patient feedback |
| `date` | Survey submission date |
| `wait_time_rating` | Wait time rating |
| `staff_rating` | Staff behaviour rating |
| `cleanliness_rating` | Facility cleanliness rating |

> 💡 **Tip**: Use `data/sample_data.csv` to test the full pipeline instantly.
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EDA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 EDA" and st.session_state.df is not None:
    render_eda(st.session_state.df)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Sentiment Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Sentiment Analysis" and st.session_state.df is not None:
    import plotly.express as px
    df = st.session_state.df
    st.markdown('<h2 class="section-title">💬 Sentiment Analysis</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    if "sentiment_label" in df.columns:
        counts  = df["sentiment_label"].value_counts()
        metrics = [
            ("😊 Positive", "Positive", "#2ecc71"),
            ("😐 Neutral",  "Neutral",  "#f39c12"),
            ("😞 Negative", "Negative", "#e74c3c"),
        ]
        for col, (label, key, color) in zip([col1, col2, col3], metrics):
            n = counts.get(key, 0)
            with col:
                st.markdown(f"""
                <div class="sentiment-card glass-card" style="border-left:4px solid {color};">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{n}</div>
                    <div class="kpi-sub">{n/len(df)*100:.1f}% of responses</div>
                </div>
                """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if "sentiment_label" in df.columns:
        with c1:
            fig = px.pie(
                df, names="sentiment_label",
                color="sentiment_label",
                color_discrete_map={"Positive":"#2ecc71","Neutral":"#f39c12","Negative":"#e74c3c"},
                title="Sentiment Distribution", hole=0.4
            )
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            if "department" in df.columns:
                dept_sent = (df.groupby(["department","sentiment_label"])
                               .size().reset_index(name="count"))
                fig2 = px.bar(
                    dept_sent, x="department", y="count", color="sentiment_label",
                    color_discrete_map={"Positive":"#2ecc71","Neutral":"#f39c12","Negative":"#e74c3c"},
                    title="Sentiment by Department", barmode="group"
                )
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color="#e2e8f0")
                st.plotly_chart(fig2, use_container_width=True)

    if "vader_compound" in df.columns:
        fig3 = px.histogram(df, x="vader_compound", nbins=30,
                            title="VADER Compound Score Distribution",
                            color_discrete_sequence=["#6366f1"])
        fig3.add_vline(x=0.05,  line_dash="dash", line_color="#2ecc71",
                       annotation_text="Positive threshold")
        fig3.add_vline(x=-0.05, line_dash="dash", line_color="#e74c3c",
                       annotation_text="Negative threshold")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0")
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📋 Sample Feedback with Sentiment")
    text_col  = ("feedback_text" if "feedback_text" in df.columns
                 else df.select_dtypes(include="object").columns[0])
    cols_show = [c for c in [text_col, "department", "sentiment_label", "vader_compound"]
                 if c in df.columns]
    st.dataframe(df[cols_show].dropna().head(30), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Issue Categories
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏷️ Issue Categories" and st.session_state.df is not None:
    import plotly.express as px
    df = st.session_state.df
    st.markdown('<h2 class="section-title">🏷️ Issue Categorization</h2>', unsafe_allow_html=True)

    if "issue_category" in df.columns:
        c1, c2 = st.columns(2)
        with c1:
            cat_counts = df["issue_category"].value_counts().reset_index()
            fig = px.bar(cat_counts, x="issue_category", y="count",
                         color="issue_category", title="Issue Category Distribution")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig_pie = px.pie(cat_counts, names="issue_category", values="count",
                             title="Issue Share", hole=0.35)
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig_pie, use_container_width=True)

        if "department" in df.columns:
            heat = df.groupby(["department","issue_category"]).size().unstack(fill_value=0)
            fig2 = px.imshow(heat, title="Issues by Department (Heatmap)",
                             color_continuous_scale="Purples", aspect="auto", text_auto=True)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Dept Benchmarking
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Dept Benchmarking" and st.session_state.df is not None:
    render_benchmarking(st.session_state.df)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Priority Scoring
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Priority Scoring" and st.session_state.df is not None:
    import plotly.express as px
    df = st.session_state.df
    st.markdown('<h2 class="section-title">⚡ Priority Scoring</h2>', unsafe_allow_html=True)

    if "priority_score" in df.columns:
        p_labels = ["🟢 Low",  "🟡 Medium", "🟠 High",  "🔴 Critical"]
        p_ranges = [(0, 3),    (3, 5),       (5, 7),     (7, 10.1)]
        p_colors = ["#2ecc71", "#f39c12",    "#e67e22",  "#e74c3c"]
        cols = st.columns(4)
        for i, (label, (lo, hi), color) in enumerate(zip(p_labels, p_ranges, p_colors)):
            n = ((df["priority_score"] >= lo) & (df["priority_score"] < hi)).sum()
            with cols[i]:
                st.markdown(f"""
                <div class="kpi-card glass-card" style="border-left:4px solid {color}">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{n}</div>
                </div>
                """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x="priority_score", nbins=20,
                               title="Priority Score Distribution",
                               color_discrete_sequence=["#e74c3c"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            if "department" in df.columns:
                dept_priority = (df.groupby("department")["priority_score"]
                                   .mean().sort_values(ascending=False).reset_index())
                fig2 = px.bar(dept_priority, x="department", y="priority_score",
                              title="Avg Priority Score by Department",
                              color="priority_score", color_continuous_scale="RdYlGn_r",
                              text_auto=".2f")
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font_color="#e2e8f0")
                st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🔴 Top 20 Critical Cases")
        top_cols = [c for c in ["patient_id","department","feedback_text",
                                "priority_score","priority_label","recommended_action"]
                    if c in df.columns]
        st.dataframe(df.nlargest(20, "priority_score")[top_cols], use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Action Mapper
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Action Mapper" and st.session_state.df is not None:
    df = st.session_state.df
    st.markdown('<h2 class="section-title">🗺️ Complaint-to-Action Mapper</h2>', unsafe_allow_html=True)
    st.info("Each complaint is automatically mapped to a recommended action based on category and severity.")

    if "recommended_action" in df.columns:
        text_col  = ("feedback_text" if "feedback_text" in df.columns
                     else df.select_dtypes(include="object").columns[0])
        show_cols = [c for c in [text_col, "department", "issue_category",
                                 "priority_label", "priority_score", "recommended_action"]
                     if c in df.columns]

        dept_filter = "All"
        if "department" in df.columns:
            dept_filter = st.selectbox(
                "Filter by Department",
                ["All"] + sorted(df["department"].dropna().unique().tolist())
            )

        priority_filter = st.multiselect(
            "Filter by Priority",
            ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"],
            default=["🔴 Critical", "🟠 High"]
        )

        filtered = df.copy()
        if dept_filter != "All":
            filtered = filtered[filtered["department"] == dept_filter]
        if priority_filter and "priority_label" in filtered.columns:
            filtered = filtered[filtered["priority_label"].isin(priority_filter)]

        st.dataframe(filtered[show_cols].dropna().head(50), use_container_width=True)
        st.download_button(
            "⬇️ Download Action Plan (CSV)",
            filtered[show_cols].to_csv(index=False),
            file_name="action_plan.csv",
            mime="text/csv"
        )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Recommendations
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Recommendations" and st.session_state.df is not None:
    df = st.session_state.df
    st.markdown('<h2 class="section-title">💡 Department Recommendations</h2>', unsafe_allow_html=True)
    recs = generate_recommendations(df)
    for dept, items in recs.items():
        with st.expander(f"📌 {dept}", expanded=False):
            for item in items:
                st.markdown(f"- {item}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Feedback Summary
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Feedback Summary" and st.session_state.df is not None:
    df = st.session_state.df
    st.markdown('<h2 class="section-title">📝 AI Feedback Summarizer</h2>',
                unsafe_allow_html=True)

    # ── Existing summaries ──────────────────────────────────────────
    summaries = summarize_feedback(df)
    for dept, summary in summaries.items():
        with st.expander(f"📋 {dept} Summary", expanded=False):
            st.markdown(f'<div class="summary-box glass-card">{summary}</div>',
                        unsafe_allow_html=True)

    # ── NEW: Advanced insights from your notebook Cell 8 ───────────
    st.markdown("---")
    st.subheader("🔑 Key Themes & Feedback Intelligence")

    text_col = "feedback_text" if "feedback_text" in df.columns else None
    if text_col:
        from collections import Counter
        import re

        def clean_for_keywords(text):
            text = str(text).lower()
            return re.sub(r'[^a-zA-Z\s]', '', text)

        stopwords = {'the','is','and','to','of','in','for','on','with','was',
                     'were','it','this','that','very','had','have','has','a',
                     'an','at','by','from','as','but','not','they','their',
                     'them','i','we','you','be','been','are','or'}

        all_words = ' '.join(df[text_col].fillna("").apply(clean_for_keywords)).split()
        filtered  = [w for w in all_words if w not in stopwords and len(w) > 3]
        top_kw    = Counter(filtered).most_common(10)

        # Display keywords as badges
        badges_html = "".join([
            f'<span class="keyword-badge">{w} ({c})</span>'
            for w, c in top_kw
        ])
        st.markdown(f'<div class="notebook-summary-card glass-card">'
                    f'<h4>🔑 Top Keywords</h4>{badges_html}</div>',
                    unsafe_allow_html=True)

        # Best / Worst department
        if "department" in df.columns and "sentiment_label" in df.columns:
            dept_pos = (df.groupby("department")["sentiment_label"]
                          .apply(lambda x: (x=="Positive").mean()*100)
                          .round(1))
            best_dept  = dept_pos.idxmax()
            worst_dept = dept_pos.idxmin()

            st.markdown(f"""
            <div class="dept-insight-row">
                <div class="dept-best glass-card">
                    🏆 <b>Best Department</b><br>{best_dept}
                    <br><small>{dept_pos[best_dept]:.1f}% positive</small>
                </div>
                <div class="dept-worst glass-card">
                    ⚠️ <b>Needs Improvement</b><br>{worst_dept}
                    <br><small>{dept_pos[worst_dept]:.1f}% positive</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI Insights
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 AI Insights" and st.session_state.df is not None:
    df       = st.session_state.df
    insights = st.session_state.insights
    st.markdown('<h2 class="section-title">🧠 AI-Generated Insights</h2>', unsafe_allow_html=True)

    if insights is None:
        with st.spinner("Generating insights..."):
            insights = generate_insights(df)
            st.session_state.insights = insights

    if insights:
        st.subheader("📌 Key Findings")
        for ins in insights.get("key_findings", []):
            st.markdown(f"""
            <div class="insight-card glass-card">
                <span class="insight-icon">{ins['icon']}</span>
                <div class="insight-body">
                    <div class="insight-title">{ins['title']}</div>
                    <div class="insight-desc">{ins['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if insights.get("trends"):
            st.subheader("📈 Trend Analysis")
            for trend in insights.get("trends", []):
                st.markdown(
                    f'<div class="trend-item glass-card">'
                    f'<b>{trend["label"]}</b>: {trend["value"]}</div>',
                    unsafe_allow_html=True
                )

        if insights.get("alerts"):
            st.subheader("🚨 Priority Alerts")
            for alert in insights.get("alerts", []):
                if alert["level"] == "critical":
                    st.error(f"🔴 {alert['message']}")
                elif alert["level"] == "warning":
                    st.warning(f"🟠 {alert['message']}")
                else:
                    st.info(f"🔵 {alert['message']}")

        col1, col2 = st.columns(2)
        with col1:
            if insights.get("top_department"):
                st.success(f"🏆 **Best Department**: {insights['top_department']}")
        with col2:
            if insights.get("worst_department"):
                st.error(f"⚠️ **Needs Attention**: {insights['worst_department']}")

        if insights.get("narrative"):
            st.subheader("📝 Executive Narrative")
            st.markdown(
                f'<div class="narrative-box glass-card">{insights["narrative"]}</div>',
                unsafe_allow_html=True
            )

        report_text = insights.get("report_text", "")
        if report_text:
            st.download_button(
                "⬇️ Download Insight Report (TXT)",
                report_text,
                file_name="insight_report.txt",
                mime="text/plain"
            )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Executive Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Executive Dashboard" and st.session_state.df is not None:
    df = st.session_state.df
    st.markdown('<h2 class="section-title">📊 Executive Dashboard</h2>', unsafe_allow_html=True)
    render_eda(df)
    st.divider()
    render_benchmarking(df)

# ═══════════════════════════════════════════════════════════════════════════════
# Fallback: No data uploaded
# ═══════════════════════════════════════════════════════════════════════════════
else:
    if st.session_state.df is None and page != "📤 Upload & Overview":
        st.markdown("""
        <div class="glass-card warning-box">
            ⚠️ Please upload your survey data first via the
            <b>📤 Upload &amp; Overview</b> page.
        </div>
        """, unsafe_allow_html=True)
