import pandas as pd
from utils.logger import get_logger
import nltk

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

logger = get_logger(__name__)

def _summarize_text(text: str, sentences: int = 3) -> str:
    if not text or len(text.split()) < 20:
        return text or "No feedback available."
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences)
        result = " ".join(str(s) for s in summary)
        return result if result.strip() else text[:400]
    except Exception as e:
        logger.warning("Sumy summarisation failed: %s. Falling back to truncation.", e)
        return text[:400] + "..."

def summarize_feedback(df: pd.DataFrame) -> dict:
    """Return one summary string per department."""
    summaries = {}
    text_col = _find_text_column(df)

    if text_col is None:
        return {"Overall": "No text column found."}

    if "department" not in df.columns:
        all_text = " ".join(df[text_col].dropna().astype(str).tolist())
        summaries["Overall"] = _summarize_text(all_text, 4)
        return summaries

    for dept in df["department"].dropna().unique():
        texts = df[df["department"] == dept][text_col].dropna().astype(str).tolist()
        combined = " ".join(texts)
        summaries[dept] = _summarize_text(combined, 3)

    logger.info("Feedback summarisation complete for %d departments.", len(summaries))
    return summaries

def _find_text_column(df):
    for c in ["feedback_text","comments","feedback","review","text"]:
        if c in df.columns:
            return c
    return None
