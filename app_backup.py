
import re
import streamlit as st
from pypdf import PdfReader
from docx import Document
from transformers import pipeline
from history import create_table, save_summary, get_history

create_table()

st.set_page_config(
    page_title="Document Summarization System",
    page_icon="📄",
    layout="wide"
)

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
    st.write("Previously generated document summaries.")

    history_records = get_history()

    if history_records:
        for record in history_records:
            summary_id, filename, original_words, summary_words, summary_text, created_at = record

            with st.expander(f"📄 {filename} — {created_at}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Original Words", original_words)

                with col2:
                    st.metric("Summary Words", summary_words)

                st.write(summary_text)

                st.download_button(
                    "⬇️ Download Summary",
                    data=summary_text,
                    file_name=f"summary_{summary_id}.txt",
                    mime="text/plain",
                    key=f"history_download_{summary_id}"
                )
    else:
        st.info("No saved summaries yet. Generate a summary first.")

    st.stop()


# Main page
st.title("📄 Document Summarization System")
st.write(
    "Upload a document and use AI to generate "
    "a concise summary."
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
    len(final_summary.split()),
    final_summary
)

                        # Display summary
                        st.subheader("📝 Generated Summary")
                        st.write(final_summary)

                        # Summary statistics
                        st.subheader("📊 Summary Statistics")

                        if original_words > 0:
                            reduction = (
                                (original_words - summary_words)
                                / original_words
                            ) * 100
                        else:
                            reduction = 0

                        stat1, stat2, stat3 = st.columns(3)

                        with stat1:
                            st.metric(
                                "Original Words",
                                original_words
                            )

                        with stat2:
                            st.metric(
                                "Summary Words",
                                summary_words
                            )

                        with stat3:
                            st.metric(
                                "Text Reduction",
                                f"{reduction:.1f}%"
                            )

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
