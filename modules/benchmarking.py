import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure, Scatterpolar
from utils.logger import get_logger

logger = get_logger(__name__)
PLOTLY_PAPER = "rgba(0,0,0,0)"
PLOTLY_FONT  = "#e2e8f0"

def _glass_layout(fig, title=""):
    fig.update_layout(
        paper_bgcolor=PLOTLY_PAPER,
        plot_bgcolor="rgba(255,255,255,0.03)",
        font_color=PLOTLY_FONT,
        title_text=title,
        title_font_size=14,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

def render_benchmarking(df: pd.DataFrame):
    st.markdown('<h2 class="section-title">🏆 Department Performance Benchmarking</h2>',
                unsafe_allow_html=True)

    if "department" not in df.columns:
        st.warning("No 'department' column found.")
        return

    rating_col = _find_rating_col(df)

    # Build scorecard
    agg = {"count": ("department", "count")}
    if rating_col:
        agg["avg_rating"] = (rating_col, "mean")
    if "sentiment_label" in df.columns:
        agg["pct_positive"] = ("sentiment_label", lambda x: (x == "Positive").mean() * 100)
    if "priority_score" in df.columns:
        agg["avg_priority"] = ("priority_score", "mean")
    if "word_count" in df.columns:
        agg["avg_feedback_length"] = ("word_count", "mean")

    scorecard = df.groupby("department").agg(**agg).reset_index()
    scorecard = scorecard.round(2)

    if rating_col and "avg_rating" in scorecard.columns:
        scorecard["rank"] = scorecard["avg_rating"].rank(ascending=False).astype(int)
        scorecard = scorecard.sort_values("rank")

    st.subheader("📋 Department Scorecard")
    style_cols = [c for c in ["avg_rating", "pct_positive"] if c in scorecard.columns]
    if style_cols:
        st.dataframe(
            scorecard.style.background_gradient(cmap="RdYlGn", subset=style_cols),
            use_container_width=True
        )
    else:
        st.dataframe(scorecard, use_container_width=True)

    # Avg Rating bar
    if rating_col and "avg_rating" in scorecard.columns:
        fig = px.bar(scorecard, x="department", y="avg_rating",
                     color="avg_rating", color_continuous_scale="RdYlGn",
                     title="Department Avg Rating", text_auto=".2f")
        fig.add_hline(y=scorecard["avg_rating"].mean(), line_dash="dash",
                      line_color="rgba(255,255,255,0.5)", annotation_text="Overall avg",
                      annotation_font_color=PLOTLY_FONT)
        _glass_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Positive sentiment bar
    if "pct_positive" in scorecard.columns:
        fig2 = px.bar(scorecard, x="department", y="pct_positive",
                      title="% Positive Sentiment by Department",
                      color="pct_positive", color_continuous_scale="Greens",
                      text_auto=".1f")
        _glass_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # Radar chart
    numeric_dims = [c for c in scorecard.columns
                    if scorecard[c].dtype in ["float64", "int64"]
                    and c not in ["count", "rank"]]
    if len(numeric_dims) >= 3:
        st.subheader("🕸️ Radar — Multi-dimension Comparison")
        # Normalise dims for radar
        norm_sc = scorecard.copy()
        for d in numeric_dims:
            mn, mx = norm_sc[d].min(), norm_sc[d].max()
            norm_sc[d] = ((norm_sc[d] - mn) / (mx - mn + 1e-9)) * 10 if mx > mn else 5.0

        fig3 = Figure()
        for _, row in norm_sc.iterrows():
            vals = [row[d] for d in numeric_dims] + [row[numeric_dims[0]]]
            fig3.add_trace(Scatterpolar(
                r=vals,
                theta=numeric_dims + [numeric_dims[0]],
                fill="toself",
                name=row["department"]
            ))
        fig3.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10],
                                       gridcolor="rgba(255,255,255,0.1)",
                                       linecolor="rgba(255,255,255,0.1)"),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")),
            paper_bgcolor=PLOTLY_PAPER,
            font_color=PLOTLY_FONT,
            title="Dept Radar (Normalised 0–10)",
            title_font_size=14,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Download scorecard
    st.download_button("⬇️ Download Scorecard (CSV)", scorecard.to_csv(index=False),
                       file_name="dept_scorecard.csv", mime="text/csv")

def _find_rating_col(df):
    for c in ["overall_rating","rating","satisfaction_score","score"]:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            return c
    return None
