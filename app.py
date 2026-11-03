
import re
import streamlit as st
from pypdf import PdfReader
from docx import Document
from transformers import pipeline
from history import create_table, save_summary, get_history, delete_summary
import history

create_table()

st.set_page_config(
    page_title="Document Summarization System",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📄 DocuSummarizer")
    st.write("AI-Powered Document Analysis")
    st.divider()

    st.subheader("Features")
    st.write("📂 PDF, DOCX and TXT Upload")
    st.write("🤖 AI Text Summarization")
    st.write("📏 Adjustable Summary Length")
    st.write("📊 Summary Statistics")
    st.write("⬇️ Download Summary")

    st.divider()
    st.caption("Mini Project")
    st.caption("Developed using Python and Streamlit")

st.sidebar.divider()
page = st.sidebar.radio(
    "Navigation",
    ["Document Summarizer", "Summary History"]
)

if page == "Summary History":
    st.title("📚 Summary History")
    st.write("Search, view, download, and delete saved summaries.")

    history_records = get_history()

    if history_records:
        search_query = st.text_input(
            "🔍 Search by document filename",
            placeholder="Enter filename..."
        )

        filtered_records = [
            record for record in history_records
            if search_query.lower() in record[1].lower()
        ]

        if filtered_records:
            for record in filtered_records:
                (
                    summary_id,
                    filename,
                    original_words,
                    summary_words,
                    summary_text,
                    created_at
                ) = record

                with st.expander(f"📄 {filename} — {created_at}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Original Words", original_words)

                    with col2:
                        st.metric("Summary Words", summary_words)

                    st.text_area(
                        "Saved summary",
                        value=summary_text,
                        height=180,
                        disabled=True,
                        key=f"history_text_{summary_id}"
                    )

                    st.download_button(
                        "⬇️ Download Summary",
                        data=summary_text,
                        file_name=f"summary_{summary_id}.txt",
                        mime="text/plain",
                        key=f"history_download_{summary_id}"
                    )

                    if st.button(
                        "🗑️ Delete Summary",
                        key=f"delete_summary_{summary_id}"
                    ):
                        delete_summary(summary_id)
                        st.success("Summary deleted successfully!")
                        st.rerun()
        else:
            st.info("No summaries match your search.")

    else:
        st.info("No saved summaries yet. Generate a summary first.")

    st.stop()


# Main page
st.markdown(
    '<div class="main-title">📄 Document Summarization System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform lengthy documents into clear, concise summaries using AI.'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "📂 Upload a PDF, DOCX, or TXT file to get started "
    "with AI-powered summarization."
)


# Load AI model
@st.cache_resource(show_spinner="Loading AI model...")
def load_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

# Extract text from supported documents
def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    elif filename.endswith(".docx"):
        document = Document(uploaded_file)
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

    elif filename.endswith(".txt"):
        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace"
        )

    return ""

# Clean extracted text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Split long documents into chunks
def split_text(text, max_words=450):
    words = text.split()
    chunks = []

    for start in range(0, len(words), max_words):
        chunks.append(
            " ".join(words[start:start + max_words])
        )

    return chunks

# Upload document
uploaded_file = st.file_uploader(
    "Upload your document",
    type=["pdf", "docx", "txt"]
)

summary_length = st.selectbox(
    "Choose summary length",
    ["Short", "Medium", "Long"]
)

if uploaded_file is not None:
    try:
        text = clean_text(extract_text(uploaded_file))

        if not text:
            st.warning(
                "No readable text found. "
                "Scanned PDFs may require OCR."
            )

        else:
            original_words = len(text.split())

            st.success("Document uploaded successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Original Word Count",
                    original_words
                )

            with col2:
                reading_time = max(
                    1, round(original_words / 200)
                )
                st.metric(
                    "Estimated Reading Time",
                    f"{reading_time} min"
                )

            with st.expander("View extracted text"):
                st.text_area(
                    "Document content",
                    text,
                    height=250
                )

            if st.button("Generate AI Summary"):
                if original_words < 40:
                    st.warning(
                        "Please upload a document containing "
                        "at least 40 words."
                    )

                else:
                    try:
                        summarizer = load_summarizer()
                        chunks = split_text(text)

                        if summary_length == "Short":
                            max_len, min_len = 60, 20
                        elif summary_length == "Medium":
                            max_len, min_len = 100, 35
                        else:
                            max_len, min_len = 150, 50

                        summaries = []
                        progress = st.progress(0)

                        for i, chunk in enumerate(chunks):
                            result = summarizer(
                                chunk,
                                max_length=max_len,
                                min_length=min_len,
                                do_sample=False,
                                truncation=True
                            )

                            summaries.append(
                                result[0]["summary_text"]
                            )

                            progress.progress(
                                (i + 1) / len(chunks)
                            )

                        final_summary = " ".join(summaries)
                        summary_words = len(
                            final_summary.split()
                        )

                        save_summary(
                            uploaded_file.name,
                            original_words,
                            summary_words,
                            final_summary
                        )

                        # Original Text vs AI Summary
                        st.subheader("📝 Original Text vs AI Summary")

                        original_col, summary_col = st.columns(2)

                        with original_col:
                            st.markdown("### 📄 Original Document")
                            st.text_area(
                                "Original text",
                                value=text,
                                height=300,
                                disabled=True,
                                key="original_comparison"
                            )

                        with summary_col:
                            st.markdown("### 🤖 AI-Generated Summary")
                            st.text_area(
                                "Generated summary",
                                value=final_summary,
                                height=300,
                                disabled=True,
                                key="summary_comparison"
                            )

                        # Summary statistics
                        st.subheader("📊 Summary Statistics")

                        reduction = (
                            (original_words - summary_words)
                            / original_words
                        ) * 100

                        stat1, stat2, stat3 = st.columns(3)

                        with stat1:
                            st.metric("Original Words", original_words)

                        with stat2:
                            st.metric("Summary Words", summary_words)

                        with stat3:
                            st.metric("Text Reduction", f"{reduction:.1f}%")

                        # Download summary
                        st.download_button(
                            "⬇️ Download Summary",
                            data=final_summary,
                            file_name="document_summary.txt",
                            mime="text/plain"
                        )

                    except Exception as error:
                        st.error(
                            "Could not generate summary. "
                            "Check your internet connection "
                            "and installed AI libraries."
                        )
                        st.caption(str(error))

    except Exception as error:
        st.error(
            f"Could not read the document: {error}"
        )
