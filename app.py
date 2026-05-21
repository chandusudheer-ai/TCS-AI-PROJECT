import streamlit as st
from utils.file_parser import extract_text
from utils.llm_helper import get_llm_response

st.set_page_config(
    page_title="AI Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Basic Chat Agent")
st.caption("Upload documents for Q&A or chat with the model.")

# Sidebar
st.sidebar.header("Settings")

with st.sidebar.expander("Connection", expanded=True):
    api_key = st.text_input("API key", type="password")
    base_url = st.text_input("Base URL", value="https://genailab.tcs.in")
    model_name = st.text_input("Model name", value="azure/genailab-maas-gpt-5-mini")

with st.sidebar.expander("Tips", expanded=False):
    st.markdown(
        """
        - For Document Q&A, upload files first, then ask a focused question.
        - For better results, ask one question at a time.
        - If answers look off, try specifying the section/table name in your question.
        """
    )

# Tabs
tab1, tab2 = st.tabs(["Document Q&A", "Chat"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Document Q&A")
    st.caption("Upload PDFs, Word, or Excel files. The agent answers using only the extracted content.")

    col_left, col_right = st.columns([0.55, 0.45], gap="large")

    with col_left:
        st.markdown("### 1) Upload")
        uploaded_files = st.file_uploader(
            "Upload PDF, Word, or Excel files",
            type=["pdf", "docx", "xlsx", "xls", "xlsm", "xlsb", "ods", "csv", "tsv"],
            accept_multiple_files=True,
        )

        st.divider()

        st.markdown("### 2) Ask")
        user_question = st.text_area(
            "Question",
            placeholder="Example: Summarize the key points from the uploaded document(s).",
            height=120,
        )

        btn = st.button("Get answer", type="primary")

    extracted_text = ""
    file_names = []
    if uploaded_files:
        for file in uploaded_files:
            file_names.append(getattr(file, "name", "(file)"))
            extracted_text += "\n\n" + (extract_text(file) or "")

    with col_right:
        st.markdown("### Preview")
        if not uploaded_files:
            st.info("Upload files to preview extracted text.")
        else:
            st.markdown("**Files**")
            st.write(", ".join(file_names))

            with st.expander("Extracted text", expanded=False):
                st.text_area(
                    "Document content",
                    extracted_text.strip(),
                    height=320,
                )

            st.download_button(
                "Download extracted text",
                data=extracted_text.strip().encode("utf-8"),
                file_name="extracted_text.txt",
                mime="text/plain",
                use_container_width=True,
            )

    if btn:
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        elif not user_question.strip():
            st.warning("Please type a question.")
        elif not api_key:
            st.error("Please enter API key in the sidebar.")
        else:
            prompt = (
                "Answer the question using only the document content below. "
                "If the answer is not present, say you cannot find it in the document.\n\n"
                f"DOCUMENT CONTENT:\n{extracted_text.strip()}\n\n"
                f"QUESTION:\n{user_question.strip()}\n"
            )
            with st.spinner("Generating answer..."):
                response = get_llm_response(api_key, base_url, model_name, prompt)
            st.markdown("### Answer")
            st.write(response)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Chat")
    st.caption("A simple conversation loop using your configured model.")

    top = st.columns([0.75, 0.25])
    with top[0]:
        st.info("Tip: If you want a particular style, say it in your first message.")
    with top[1]:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type a message")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        if not api_key:
            st.session_state.messages.append(
                {"role": "assistant", "content": "Please enter the API key in the sidebar."}
            )
            st.rerun()

        with st.spinner("Thinking..."):
            response = get_llm_response(api_key, base_url, model_name, user_input)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
