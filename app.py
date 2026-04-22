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

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('''
    <div class="sidebar-header">
        <div class="sidebar-logo">🏥</div>
        <div class="sidebar-brand">
            <span class="brand-text">MedInsight</span> <span class="brand-ai">AI</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-title">NAVIGATION</div>', unsafe_allow_html=True)

    options = [
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
    ]

    page = st.radio(
        " ",
        options,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-footer">Built for HCL Internship<br><span class="sidebar-footer-highlight">Patient Satisfaction Analytics</span></div>', unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
for key in ["df_raw", "df", "insights", "current_page"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Default to main upload page
if st.session_state.current_page is None:
    st.session_state.current_page = "upload_overview"

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Upload & Overview
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📤 Upload & Overview":

    # ── Hero Header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="upload-hero">
        <div class="upload-hero-inner">
            <div class="upload-hero-tag">🏥 Patient Satisfaction Intelligence</div>
            <h1 class="upload-hero-title">Survey Data<br><span class="upload-hero-accent">Refined.</span></h1>
            <p class="upload-hero-subtitle">
                Upload your patient survey data and let AI transform raw responses<br>
                into actionable clinical insights.
            </p>
        </div>
        <div class="upload-hero-glow"></div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SUB-PAGE ROUTING
    # ══════════════════════════════════════════════════════════════════════════
    
    # ── MAIN UPLOAD SELECTION PAGE ───────────────────────────────────────────
    if st.session_state.current_page == "upload_overview":
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="upload-mode-card">
                <div class="upload-mode-icon">
                    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="8" y="4" width="36" height="48" rx="4" stroke="currentColor" stroke-width="2.5" fill="none"/>
                        <path d="M36 4L44 12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <rect x="36" y="4" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2" fill="none"/>
                        <line x1="16" y1="24" x2="36" y2="24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <line x1="16" y1="32" x2="36" y2="32" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <line x1="16" y1="40" x2="28" y2="40" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <circle cx="50" cy="50" r="10" fill="rgba(99,102,241,0.15)" stroke="currentColor" stroke-width="2"/>
                        <path d="M47 50l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <h3>Analyze CSV</h3>
                <p>Upload structured patient satisfaction dataset with survey responses and ratings</p>
                <div class="upload-mode-badge">Primary Pipeline</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📊 Select CSV Upload", key="btn_csv", use_container_width=True, type="primary"):
                st.session_state.current_page = "csv_upload"
                st.rerun()

        with col2:
            st.markdown("""
            <div class="upload-mode-card upload-mode-card--pdf">
                <div class="upload-mode-icon">
                    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="8" y="4" width="36" height="48" rx="4" stroke="currentColor" stroke-width="2.5" fill="none"/>
                        <path d="M36 4L44 12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <rect x="36" y="4" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2" fill="none"/>
                        <rect x="13" y="22" width="26" height="16" rx="3" stroke="currentColor" stroke-width="2" fill="rgba(139,92,246,0.1)"/>
                        <text x="16" y="34" font-size="9" fill="currentColor" font-family="monospace" font-weight="bold">PDF</text>
                    </svg>
                </div>
                <h3>Analyze PDF</h3>
                <p>Upload patient survey reports, clinical documents and feedback summaries</p>
                <div class="upload-mode-badge upload-mode-badge--pdf">Survey Reports</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📄 Select PDF Upload", key="btn_pdf", use_container_width=True, type="primary"):
                st.session_state.current_page = "pdf_upload"
                st.rerun()

    # ── CSV UPLOAD PAGE ───────────────────────────────────────────────────────
    elif st.session_state.current_page == "csv_upload":
        
        # Back button
        if st.button("← Back to Upload Options", key="back_from_csv"):
            st.session_state.current_page = "upload_overview"
            st.rerun()
        
        st.markdown('<h2 class="section-title">� Upload CSV Dataset</h2>', unsafe_allow_html=True)
        
        # Centered upload card
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="upload-card glass-card">
                <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">Patient Satisfaction Dataset</h3>
                <p style="color: rgba(226, 232, 240, 0.6); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    Upload your CSV file containing patient survey responses
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            csv_file = st.file_uploader(
                "Drop your CSV file here",
                type=["csv"],
                key="csv_uploader",
                help="Required columns: patient_id, department, feedback_text"
            )
            
            if csv_file:
                # Guardrail Function - Enhanced for Patient Satisfaction Only
                def validate_patient_dataset(df):
                    """Strict validation to ensure only patient satisfaction surveys are accepted."""
                    # Normalize column names
                    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
                    
                    # Check for ID column (flexible naming)
                    id_columns = ['patient_id', 'id', 'respondent_id', 'survey_id', 'record_id', 'patient_no']
                    has_id = any(col in df.columns for col in id_columns)
                    
                    # Check for department/location column
                    dept_columns = ['department', 'dept', 'ward', 'unit', 'location', 'service']
                    has_dept = any(col in df.columns for col in dept_columns)
                    
                    # Check for feedback text column
                    text_columns = ['feedback_text', 'feedback', 'comments', 'comment', 'text', 'response', 'review']
                    text_col = None
                    for col in text_columns:
                        if col in df.columns:
                            text_col = col
                            break
                    
                    # If no exact match, find longest text column
                    if not text_col:
                        obj_cols = df.select_dtypes(include='object').columns.tolist()
                        if obj_cols:
                            # Find column with longest average text
                            avg_lengths = {col: df[col].dropna().astype(str).str.len().mean() for col in obj_cols}
                            text_col = max(avg_lengths, key=avg_lengths.get) if avg_lengths else None
                    
                    has_text = text_col is not None
                    
                    # Check for rating columns
                    rating_columns = ['overall_rating', 'rating', 'satisfaction_score', 'score', 'satisfaction']
                    has_rating = any(col in df.columns for col in rating_columns)
                    
                    # Validation checks
                    if not has_text:
                        return False, "❌ Missing feedback/comment text column. Required for patient satisfaction analysis."
                    
                    if df[text_col].dropna().shape[0] < 5:
                        return False, "❌ Not enough feedback data (minimum 5 responses required)."
                    
                    # Check if content is healthcare-related
                    sample_text = " ".join(df[text_col].dropna().astype(str).head(30)).lower()
                    
                    # Healthcare keywords (must have at least 3 matches)
                    healthcare_keywords = [
                        'patient', 'doctor', 'nurse', 'hospital', 'clinic', 'medical',
                        'treatment', 'care', 'staff', 'appointment', 'wait', 'service',
                        'health', 'physician', 'surgery', 'emergency', 'ward', 'department'
                    ]
                    
                    keyword_matches = sum(1 for keyword in healthcare_keywords if keyword in sample_text)
                    
                    if keyword_matches < 3:
                        return False, f"❌ This doesn't appear to be a patient satisfaction survey. Only {keyword_matches} healthcare-related keywords found. Please upload patient survey data."
                    
                    # Check column names for healthcare context
                    col_text = " ".join(df.columns).lower()
                    col_keywords = ['patient', 'satisfaction', 'rating', 'feedback', 'department', 'staff', 'wait', 'cleanliness', 'hospital', 'care']
                    col_matches = sum(1 for kw in col_keywords if kw in col_text)
                    
                    if col_matches < 2:
                        return False, "❌ Column names don't match patient satisfaction survey format. Expected columns like: patient_id, department, rating, feedback_text."
                    
                    # Success message with details
                    details = []
                    if has_id:
                        details.append("ID column found")
                    if has_dept:
                        details.append("Department column found")
                    if has_rating:
                        details.append("Rating column found")
                    details.append(f"{keyword_matches} healthcare keywords detected")
                    
                    return True, f"✅ Valid patient satisfaction dataset. {', '.join(details)}."

                logger.info(f"CSV uploaded: {csv_file.name}")
                with st.spinner("📥 Loading data..."):
                    df_raw = load_data(csv_file)

                if df_raw is None:
                    st.error("❌ Could not load CSV")
                    st.stop()

                is_valid, message = validate_patient_dataset(df_raw)
                if not is_valid:
                    st.error(message)
                    st.stop()

                st.success(message)

                issues = validate_dataframe(df_raw)
                st.markdown('<div class="validation-section-title">🔍 Validation Report</div>', unsafe_allow_html=True)
                if issues:
                    for issue in issues:
                        st.markdown(f'<div class="validation-warning">⚠️ {issue}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-pass">✅ Dataset validated — all checks passed</div>', unsafe_allow_html=True)

                st.session_state.df_raw = df_raw
                logger.info(f"Data loaded: {df_raw.shape}")

                # ── Pipeline ──────────────────────────────────────────────────
                st.markdown("""
                <div class="pipeline-header">
                    <span class="pipeline-header-title">⚙️ Running Analysis Pipeline</span>
                </div>
                """, unsafe_allow_html=True)

                progress_bar = st.progress(0)
                status_text  = st.empty()

                pipeline = [
                    ("🧹 Cleaning data...", clean_data, 10),
                    ("⚙️ Preprocessing text...", preprocess_data, 25),
                    ("🔧 Engineering features...", engineer_features, 40),
                    ("💬 Running sentiment analysis...", run_sentiment_analysis, 60),
                    ("🏷️ Categorizing issues...", categorize_issues, 75),
                    ("⚡ Scoring priorities...", score_priorities, 88),
                    ("🗺️ Mapping actions...", map_actions, 95),
                ]

                df_current = df_raw.copy()
                for label, func, pct in pipeline:
                    status_text.markdown(f'<div class="pipeline-step">{label}</div>', unsafe_allow_html=True)
                    progress_bar.progress(pct)
                    df_current = func(df_current.copy())

                progress_bar.progress(100)
                status_text.empty()
                st.session_state.df = df_current

                with st.spinner("🧠 Generating AI insights..."):
                    st.session_state.insights = generate_insights(df_current)

                st.success("✅ Full pipeline complete! Navigate using the sidebar →")
                st.session_state.current_page = "data_overview"
                st.rerun()

    # ── PDF UPLOAD PAGE ───────────────────────────────────────────────────────
    elif st.session_state.current_page == "pdf_upload":
        
        # Back button
        if st.button("← Back to Upload Options", key="back_from_pdf"):
            st.session_state.current_page = "upload_overview"
            st.rerun()
        
        st.markdown('<h2 class="section-title">📄 Upload PDF Report</h2>', unsafe_allow_html=True)
        
        # Centered upload card
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="upload-card glass-card">
                <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">Patient Survey Report</h3>
                <p style="color: rgba(226, 232, 240, 0.6); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    Upload PDF containing patient satisfaction survey results
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            pdf_file = st.file_uploader(
                "Drop your PDF file here",
                type=["pdf"],
                key="pdf_uploader"
            )
            
            if pdf_file:
                st.warning("⚠️ Only patient survey PDFs allowed")
                confirm = st.checkbox("✅ Confirm this is a patient satisfaction report")
                if confirm:
                    st.success("✅ PDF accepted — processing can be added later")
                    st.session_state["pdf_file_data"] = pdf_file

    # ── DATA OVERVIEW (After Upload) ──────────────────────────────────────────
    elif st.session_state.current_page == "data_overview":
        df = st.session_state.df
        if df is not None:
            # ── KPI Cards ─────────────────────────────────────────────────
            st.markdown('<h2 class="section-title">📊 Dataset Overview</h2>', unsafe_allow_html=True)

            kpi_data = [
                ("📋 Total Responses", len(df), None),
                ("⭐ Avg Rating", f"{df['overall_rating'].mean():.2f}/5" if "overall_rating" in df.columns else "N/A", None),
                ("😊 Positive %", f"{(df['sentiment_label']=='Positive').mean()*100:.1f}%" if "sentiment_label" in df.columns else "N/A", "#2ecc71"),
                ("🏥 Departments", df["department"].nunique() if "department" in df.columns else "N/A", None),
                ("🔴 Critical Issues", int((df["priority_score"] >= 7).sum()) if "priority_score" in df.columns else "N/A", "#e74c3c"),
            ]

            cols = st.columns(5)
            for i, (label, value, accent) in enumerate(kpi_data):
                border = f"border-left: 4px solid {accent};" if accent else ""
                with cols[i]:
                    st.markdown(f"""
                    <div class="kpi-card glass-card" style="{border}">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(50), use_container_width=True)
            
            if st.button("← Upload New Dataset"):
                st.session_state.current_page = "upload_overview"
                st.session_state.df = None
                st.session_state.df_raw = None
                st.rerun()
        else:
            st.warning("No data loaded. Please upload a dataset.")
            if st.button("← Back to Upload"):
                st.session_state.current_page = "upload_overview"
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EDA
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 EDA":
    if st.session_state.df is not None:
        render_eda(st.session_state.df)
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Sentiment Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Sentiment Analysis":
    if st.session_state.df is not None:
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
                fig = px.pie(df, names="sentiment_label", color="sentiment_label",
                             color_discrete_map={"Positive":"#2ecc71","Neutral":"#f39c12","Negative":"#e74c3c"},
                             title="Sentiment Distribution", hole=0.4)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                if "department" in df.columns:
                    dept_sent = df.groupby(["department","sentiment_label"]).size().reset_index(name="count")
                    fig2 = px.bar(dept_sent, x="department", y="count", color="sentiment_label",
                                  color_discrete_map={"Positive":"#2ecc71","Neutral":"#f39c12","Negative":"#e74c3c"},
                                  title="Sentiment by Department", barmode="group")
                    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                    st.plotly_chart(fig2, use_container_width=True)

        if "vader_compound" in df.columns:
            fig3 = px.histogram(df, x="vader_compound", nbins=30,
                                title="VADER Compound Score Distribution",
                                color_discrete_sequence=["#6366f1"])
            fig3.add_vline(x=0.05, line_dash="dash", line_color="#2ecc71", annotation_text="Positive threshold")
            fig3.add_vline(x=-0.05, line_dash="dash", line_color="#e74c3c", annotation_text="Negative threshold")
            fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig3, use_container_width=True)

        st.subheader("📋 Sample Feedback with Sentiment")
        text_col  = "feedback_text" if "feedback_text" in df.columns else df.select_dtypes(include="object").columns[0]
        cols_show = [c for c in [text_col, "department", "sentiment_label", "vader_compound"] if c in df.columns]
        st.dataframe(df[cols_show].dropna().head(30), use_container_width=True)
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Issue Categories
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏷️ Issue Categories":
    if st.session_state.df is not None:
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
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Dept Benchmarking
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Dept Benchmarking":
    if st.session_state.df is not None:
        render_benchmarking(st.session_state.df)
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Priority Scoring
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Priority Scoring":
    if st.session_state.df is not None:
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
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                if "department" in df.columns:
                    dept_priority = df.groupby("department")["priority_score"].mean().sort_values(ascending=False).reset_index()
                    fig2 = px.bar(dept_priority, x="department", y="priority_score",
                                  title="Avg Priority Score by Department",
                                  color="priority_score", color_continuous_scale="RdYlGn_r", text_auto=".2f")
                    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                    st.plotly_chart(fig2, use_container_width=True)

            st.subheader("🔴 Top 20 Critical Cases")
            top_cols = [c for c in ["patient_id","department","feedback_text","priority_score","priority_label","recommended_action"] if c in df.columns]
            st.dataframe(df.nlargest(20, "priority_score")[top_cols], use_container_width=True)
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Action Mapper
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Action Mapper":
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<h2 class="section-title">🗺️ Complaint-to-Action Mapper</h2>', unsafe_allow_html=True)
        st.info("Each complaint is automatically mapped to a recommended action based on category and severity.")

        if "recommended_action" in df.columns:
            text_col  = "feedback_text" if "feedback_text" in df.columns else df.select_dtypes(include="object").columns[0]
            show_cols = [c for c in [text_col, "department", "issue_category", "priority_label", "priority_score", "recommended_action"] if c in df.columns]

            dept_filter = "All"
            if "department" in df.columns:
                dept_filter = st.selectbox("Filter by Department", ["All"] + sorted(df["department"].dropna().unique().tolist()))

            priority_filter = st.multiselect("Filter by Priority", ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"], default=["🔴 Critical", "🟠 High"])

            filtered = df.copy()
            if dept_filter != "All":
                filtered = filtered[filtered["department"] == dept_filter]
            if priority_filter and "priority_label" in filtered.columns:
                filtered = filtered[filtered["priority_label"].isin(priority_filter)]

            st.dataframe(filtered[show_cols].dropna().head(50), use_container_width=True)
            st.download_button("⬇️ Download Action Plan (CSV)", filtered[show_cols].to_csv(index=False), file_name="action_plan.csv", mime="text/csv")
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Recommendations
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Recommendations":
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<h2 class="section-title">💡 Department Recommendations</h2>', unsafe_allow_html=True)
        recs = generate_recommendations(df)
        for dept, items in recs.items():
            with st.expander(f"📌 {dept}", expanded=False):
                for item in items:
                    st.markdown(f"- {item}")
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Feedback Summary
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Feedback Summary":
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<h2 class="section-title">📝 AI Feedback Summarizer</h2>', unsafe_allow_html=True)

        # Initialize session state for expand/collapse
        if 'expand_all' not in st.session_state:
            st.session_state.expand_all = False

        # ── SEARCH & FILTERS ──────────────────────────────────────────────────
        st.markdown('<div class="filter-section glass-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input(
                "🔍 Search in feedback",
                placeholder="Search keywords in patient feedback...",
                key="feedback_search"
            )
        with col2:
            col_expand, col_collapse = st.columns(2)
            with col_expand:
                if st.button("📂 Expand All", use_container_width=True):
                    st.session_state.expand_all = True
            with col_collapse:
                if st.button("📁 Collapse All", use_container_width=True):
                    st.session_state.expand_all = False

        # Filters row
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            dept_options = ["All Departments"] + sorted(df["department"].dropna().unique().tolist()) if "department" in df.columns else ["All Departments"]
            selected_dept = st.selectbox("🏥 Department", dept_options, key="dept_filter")
        
        with filter_col2:
            sentiment_options = ["All Sentiments", "Positive", "Neutral", "Negative"]
            selected_sentiment = st.selectbox("😊 Sentiment", sentiment_options, key="sentiment_filter")
        
        with filter_col3:
            priority_options = ["All Priorities", "Critical", "High", "Medium", "Low"]
            selected_priority = st.selectbox("⚡ Priority", priority_options, key="priority_filter")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # ── APPLY FILTERS ─────────────────────────────────────────────────────
        filtered_df = df.copy()
        
        # Search filter
        if search_query:
            text_col = "feedback_text" if "feedback_text" in df.columns else df.select_dtypes(include="object").columns[0]
            filtered_df = filtered_df[filtered_df[text_col].str.contains(search_query, case=False, na=False)]
        
        # Department filter
        if selected_dept != "All Departments" and "department" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["department"] == selected_dept]
        
        # Sentiment filter
        if selected_sentiment != "All Sentiments" and "sentiment_label" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sentiment_label"] == selected_sentiment]
        
        # Priority filter
        if selected_priority != "All Priorities" and "priority_label" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["priority_label"] == selected_priority]

        # Show filter results
        if len(filtered_df) < len(df):
            st.info(f"📊 Showing {len(filtered_df)} of {len(df)} responses based on filters")

        # ── GENERATE SUMMARIES ────────────────────────────────────────────────
        if len(filtered_df) > 0:
            summaries = summarize_feedback(filtered_df)
            
            # Calculate department metrics
            dept_metrics = {}
            if "department" in filtered_df.columns and "sentiment_label" in filtered_df.columns:
                for dept in filtered_df["department"].dropna().unique():
                    dept_data = filtered_df[filtered_df["department"] == dept]
                    total = len(dept_data)
                    positive = (dept_data["sentiment_label"] == "Positive").sum() if "sentiment_label" in dept_data.columns else 0
                    negative = (dept_data["sentiment_label"] == "Negative").sum() if "sentiment_label" in dept_data.columns else 0
                    
                    # Get top issue
                    top_issue = "N/A"
                    if "issue_category" in dept_data.columns:
                        issue_counts = dept_data["issue_category"].value_counts()
                        top_issue = issue_counts.index[0] if len(issue_counts) > 0 else "N/A"
                    
                    dept_metrics[dept] = {
                        "positive_pct": (positive / total * 100) if total > 0 else 0,
                        "negative_pct": (negative / total * 100) if total > 0 else 0,
                        "top_issue": top_issue,
                        "total": total
                    }

            # ── DISPLAY SUMMARIES WITH ENHANCED CARDS ─────────────────────────
            for dept, summary in summaries.items():
                metrics = dept_metrics.get(dept, {})
                pos_pct = metrics.get("positive_pct", 0)
                neg_pct = metrics.get("negative_pct", 0)
                top_issue = metrics.get("top_issue", "N/A")
                total = metrics.get("total", 0)
                
                # Determine border color based on sentiment
                if pos_pct >= 70:
                    border_color = "#2ecc71"  # Green
                    border_class = "summary-card-positive"
                elif neg_pct >= 40:
                    border_color = "#e74c3c"  # Red
                    border_class = "summary-card-negative"
                else:
                    border_color = "rgba(99, 102, 241, 0.3)"  # Default
                    border_class = "summary-card-neutral"
                
                # Create expandable card with metrics
                with st.expander(f"📋 {dept} Summary", expanded=st.session_state.expand_all):
                    # Metrics row
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.markdown(f"""
                        <div class="summary-metric">
                            <div class="summary-metric-label">Total Responses</div>
                            <div class="summary-metric-value">{total}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with metric_col2:
                        st.markdown(f"""
                        <div class="summary-metric">
                            <div class="summary-metric-label">😊 Positive</div>
                            <div class="summary-metric-value" style="color: #2ecc71;">{pos_pct:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with metric_col3:
                        st.markdown(f"""
                        <div class="summary-metric">
                            <div class="summary-metric-label">😞 Negative</div>
                            <div class="summary-metric-value" style="color: #e74c3c;">{neg_pct:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with metric_col4:
                        st.markdown(f"""
                        <div class="summary-metric">
                            <div class="summary-metric-label">Top Issue</div>
                            <div class="summary-metric-value" style="font-size: 0.9rem;">{top_issue}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Sentiment distribution bar
                    st.markdown(f"""
                    <div class="sentiment-bar-container">
                        <div class="sentiment-bar-positive" style="width: {pos_pct}%;"></div>
                        <div class="sentiment-bar-negative" style="width: {neg_pct}%;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Summary text
                    st.markdown(f'<div class="summary-box glass-card" style="border-left: 4px solid {border_color};">{summary}</div>', unsafe_allow_html=True)

        else:
            st.warning("⚠️ No feedback matches your filters. Try adjusting the search or filter criteria.")

        st.markdown("---")
        st.subheader("🔑 Key Themes & Feedback Intelligence")

        text_col = "feedback_text" if "feedback_text" in filtered_df.columns else None
        if text_col and len(filtered_df) > 0:
            from collections import Counter
            import re

            def clean_for_keywords(text):
                text = str(text).lower()
                return re.sub(r'[^a-zA-Z\s]', '', text)

            stopwords = {'the','is','and','to','of','in','for','on','with','was',
                         'were','it','this','that','very','had','have','has','a',
                         'an','at','by','from','as','but','not','they','their',
                         'them','i','we','you','be','been','are','or'}

            all_words = ' '.join(filtered_df[text_col].fillna("").apply(clean_for_keywords)).split()
            filtered_words  = [w for w in all_words if w not in stopwords and len(w) > 3]
            top_kw    = Counter(filtered_words).most_common(10)

            badges_html = "".join([f'<span class="keyword-badge">{w} ({c})</span>' for w, c in top_kw])
            st.markdown(f'<div class="notebook-summary-card glass-card"><h4>🔑 Top Keywords</h4>{badges_html}</div>', unsafe_allow_html=True)

            if "department" in filtered_df.columns and "sentiment_label" in filtered_df.columns:
                dept_pos = (filtered_df.groupby("department")["sentiment_label"]
                              .apply(lambda x: (x=="Positive").mean()*100).round(1))
                if len(dept_pos) > 0:
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
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI Insights
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 AI Insights":
    if st.session_state.df is not None:
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
                    st.markdown(f'<div class="trend-item glass-card"><b>{trend["label"]}</b>: {trend["value"]}</div>', unsafe_allow_html=True)

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
                st.markdown(f'<div class="narrative-box glass-card">{insights["narrative"]}</div>', unsafe_allow_html=True)

            report_text = insights.get("report_text", "")
            if report_text:
                st.download_button("⬇️ Download Insight Report (TXT)", report_text, file_name="insight_report.txt", mime="text/plain")
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Executive Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Executive Dashboard":
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<h2 class="section-title">📊 Executive Dashboard</h2>', unsafe_allow_html=True)
        render_eda(df)
        st.divider()
        render_benchmarking(df)
    else:
        st.markdown('<div class="glass-card warning-box">⚠️ Please upload your survey data first via the <b>📤 Upload &amp; Overview</b> page.</div>', unsafe_allow_html=True)