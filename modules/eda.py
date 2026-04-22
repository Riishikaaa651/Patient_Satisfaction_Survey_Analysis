import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger(__name__)
PLOTLY_PAPER = "rgba(0,0,0,0)"
PLOTLY_FONT  = "#e2e8f0"

def _glass_layout(fig, title: str = ""):
    fig.update_layout(
        paper_bgcolor=PLOTLY_PAPER,
        plot_bgcolor="rgba(255,255,255,0.03)",
        font_color=PLOTLY_FONT,
        title_text=title,
        title_font_size=14,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

def render_eda(df: pd.DataFrame):
    st.markdown('<h2 class="section-title">🔍 Exploratory Data Analysis</h2>', unsafe_allow_html=True)

    # Fix any datetime columns that should be numeric
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]) and ('rating' in col or 'score' in col or 'wait' in col):
            # Convert back to numeric if possible
            try:
                df[col] = pd.to_numeric(df[col].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
            except:
                pass

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric("Total Responses", len(df))

    rating_col = _find_rating_col(df)
    if rating_col:
        with kpi_cols[1]: st.metric("Avg Rating", f"{df[rating_col].mean():.2f}")
        with kpi_cols[2]: st.metric("Median Rating", f"{df[rating_col].median():.1f}")

    if "department" in df.columns:
        with kpi_cols[3]: st.metric("Departments", df["department"].nunique())

    st.divider()

    # Rating distribution
    if rating_col:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x=rating_col, nbins=10,
                               title="Overall Rating Distribution",
                               color_discrete_sequence=["#6366f1"])
            fig.update_layout(bargap=0.1, xaxis_title="Rating", yaxis_title="Count")
            _glass_layout(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if "department" in df.columns:
                avg = df.groupby("department")[rating_col].mean().sort_values().reset_index()
                fig2 = px.bar(avg, y="department", x=rating_col, orientation="h",
                              title="Avg Rating by Department",
                              color=rating_col, color_continuous_scale="RdYlGn",
                              text_auto=".2f")
                fig2.update_layout(xaxis_title="Average Rating", yaxis_title="Department")
                _glass_layout(fig2)
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ No rating column found. Upload a dataset with rating/score columns for better analysis.")

    # Additional rating columns analysis
    rating_cols = [c for c in df.columns if 'rating' in c or 'score' in c]
    numeric_rating_cols = [c for c in rating_cols if pd.api.types.is_numeric_dtype(df[c])]
    
    if len(numeric_rating_cols) > 1:
        st.subheader("📊 Rating Breakdown by Category")
        cols = st.columns(min(len(numeric_rating_cols), 4))
        for idx, col in enumerate(numeric_rating_cols[:4]):
            with cols[idx]:
                avg_val = df[col].mean()
                st.metric(
                    col.replace('_', ' ').title(),
                    f"{avg_val:.2f}",
                    delta=f"{avg_val - 3:.2f} vs neutral" if avg_val != 3 else None
                )
        
        # Radar chart for multiple ratings
        if len(numeric_rating_cols) >= 3:
            avg_ratings = {col.replace('_', ' ').title(): df[col].mean() for col in numeric_rating_cols[:6]}
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=list(avg_ratings.values()),
                theta=list(avg_ratings.keys()),
                fill='toself',
                line_color='#6366f1',
                fillcolor='rgba(99, 102, 241, 0.3)'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 5])
                ),
                title="Rating Categories Comparison",
                paper_bgcolor=PLOTLY_PAPER,
                font_color=PLOTLY_FONT
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # Trend over time
    date_cols = df.select_dtypes(include="datetime64[ns]").columns.tolist()
    if date_cols and rating_col:
        dc = date_cols[0]
        trend = df.groupby(df[dc].dt.to_period("M"))[rating_col].mean().reset_index()
        trend[dc] = trend[dc].astype(str)
        fig3 = px.line(trend, x=dc, y=rating_col, title="Rating Trend Over Time", markers=True,
                       color_discrete_sequence=["#8b5cf6"])
        fig3.update_layout(xaxis_title="Month", yaxis_title="Average Rating")
        _glass_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    # Department comparison with all ratings
    if "department" in df.columns and len(numeric_rating_cols) > 0:
        st.subheader("🏥 Department Performance Comparison")
        dept_ratings = df.groupby("department")[numeric_rating_cols].mean().reset_index()
        
        fig_dept = px.bar(dept_ratings, x="department", y=numeric_rating_cols[:5],
                          title="Department Ratings Comparison",
                          barmode="group",
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig_dept.update_layout(xaxis_title="Department", yaxis_title="Average Rating")
        _glass_layout(fig_dept)
        st.plotly_chart(fig_dept, use_container_width=True)

    # NPS breakdown
    if "nps_category" in df.columns:
        c1, c2 = st.columns(2)
        with c1:
            nps_counts = df["nps_category"].value_counts().reset_index()
            fig4 = px.pie(nps_counts, names="nps_category", values="count",
                          color="nps_category",
                          color_discrete_map={"Promoter":"#2ecc71","Passive":"#f39c12","Detractor":"#e74c3c"},
                          title="NPS Category Breakdown", hole=0.4)
            _glass_layout(fig4)
            st.plotly_chart(fig4, use_container_width=True)
        with c2:
            if "rating_band" in df.columns:
                rb = df["rating_band"].value_counts().reset_index()
                fig_rb = px.bar(rb, x="rating_band", y="count",
                                color="rating_band",
                                color_discrete_map={"Poor":"#e74c3c","Average":"#f39c12",
                                                    "Good":"#2ecc71","Excellent":"#27ae60"},
                                title="Rating Band Distribution")
                _glass_layout(fig_rb)
                st.plotly_chart(fig_rb, use_container_width=True)

    # Word cloud
    if "clean_text" in df.columns:
        st.subheader("💬 Word Cloud — Patient Feedback")
        all_text = " ".join(df["clean_text"].dropna().tolist())
        if all_text.strip():
            wc = WordCloud(width=1000, height=380, background_color="#0d1b2a",
                           colormap="cool", max_words=150).generate(all_text)
            fig_wc, ax = plt.subplots(figsize=(12, 4))
            fig_wc.patch.set_facecolor("#0d1b2a")
            ax.set_facecolor("#0d1b2a")
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig_wc)

    # Correlation heatmap
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 3:
        corr = df[numeric_cols[:12]].corr()
        fig5 = px.imshow(corr, text_auto=".2f", title="Feature Correlation Heatmap",
                         color_continuous_scale="RdBu_r", aspect="auto")
        _glass_layout(fig5)
        st.plotly_chart(fig5, use_container_width=True)

    with st.expander("🗃️ Explore Raw Data"):
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Processed Data", csv,
                           file_name="processed_data.csv", mime="text/csv")

def _find_rating_col(df):
    for c in ["overall_rating","rating","satisfaction_score","score"]:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            return c
    return None
