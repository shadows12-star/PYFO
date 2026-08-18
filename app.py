import streamlit as st

from document_processor import process_document
from main import ask_question



st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .hero {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            padding: 2.5rem 2.5rem;
            border-radius: 20px;
            margin-bottom: 1.75rem;
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
        }
        .hero h1 {
            color: white;
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0 0 0.4rem 0;
        }
        .hero p {
            color: rgba(255,255,255,0.85);
            font-size: 1rem;
            margin: 0;
        }

        .section-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #6366F1;
            margin-bottom: 0.4rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .answer-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-left: 4px solid #6366F1;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            margin-bottom: 1.2rem;
        }
        .answer-card p {
            font-size: 1.02rem;
            line-height: 1.65;
            color: #1F2937;
            margin: 0;
        }

        .no-answer-card {
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-left: 4px solid #F59E0B;
            border-radius: 14px;
            padding: 1.2rem 1.5rem;
            color: #92400E;
            font-weight: 500;
        }

        .source-badge {
            display: inline-block;
            background: #EEF2FF;
            color: #4338CA;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.15rem 0.55rem;
            border-radius: 6px;
            margin-right: 0.5rem;
        }

        .sidebar-card {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            border: none;
            padding: 0.55rem 1.2rem;
        }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        }
    </style>
    """,
    unsafe_allow_html=True,
)



if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "history" not in st.session_state:
    st.session_state.history = []  # list of {question, answer, sources}



st.markdown(
    """
    <div class="hero">
        <h1>📄 AI Document Intelligence</h1>
        <p>Upload a document, ask a question in plain English, and get a grounded
        answer with the exact source passages it came from.</p>
    </div>
    """,
    unsafe_allow_html=True,
)



with st.sidebar:
    st.markdown('<div class="section-label">Document</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        process_clicked = st.button(
            "⚡ Process Document",
            type="primary",
            use_container_width=True,
        )

        if process_clicked:
            with st.spinner("Chunking, embedding, and indexing..."):
                vectorstore, chunks = process_document(uploaded_file)

                st.session_state.vectorstore = vectorstore
                st.session_state.file_name = uploaded_file.name
                st.session_state.chunk_count = len(chunks)
                st.session_state.history = []

            st.toast(f"Indexed {len(chunks)} chunks", icon="✅")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.vectorstore:
        st.markdown('<div class="section-label">Status</div>', unsafe_allow_html=True)
        st.markdown(
            '<span class="status-pill">🟢 Ready</span>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-card">
                <b>📎 {st.session_state.file_name}</b><br>
                <span style="color:#6B7280; font-size:0.85rem;">
                    {st.session_state.chunk_count} chunks indexed
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🗑️ Clear session", use_container_width=True):
            st.session_state.vectorstore = None
            st.session_state.file_name = None
            st.session_state.chunk_count = 0
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown(
            '<span class="status-pill" style="background:#F3F4F6; color:#6B7280; '
            'border-color:#E5E7EB;">⚪ No document indexed</span>',
            unsafe_allow_html=True,
        )



if not st.session_state.vectorstore:
    st.markdown(
        """
        <div style="text-align:center; padding: 4rem 1rem; color:#9CA3AF;">
            <div style="font-size: 3rem;">🗂️</div>
            <h3 style="color:#4B5563;">No document indexed yet</h3>
            <p>Upload a PDF or TXT file in the sidebar and click
            <b>Process Document</b> to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown('<div class="section-label">Ask a question</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "Question",
            placeholder="e.g. What are the key findings in this document?",
            label_visibility="collapsed",
        )
    with col2:
        ask_clicked = st.button("Ask →", type="primary", use_container_width=True)

    if ask_clicked and query.strip():
        with st.spinner("Retrieving relevant passages and generating an answer..."):
            result = ask_question(st.session_state.vectorstore, query)

        st.session_state.history.insert(
            0,
            {
                "question": query,
                "answer": result["answer"],
                "sources": result["sources"],
            },
        )

    if st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)

        for turn in st.session_state.history:
            st.markdown(f"**🙋 {turn['question']}**")

            not_found = "could not find the answer" in turn["answer"].lower()

            if not_found:
                st.markdown(
                    f'<div class="no-answer-card">⚠️ {turn["answer"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="answer-card"><p>{turn["answer"]}</p></div>',
                    unsafe_allow_html=True,
                )

                if turn["sources"]:
                    with st.expander(f"📎 View {len(turn['sources'])} source(s)"):
                        for source in turn["sources"]:
                            st.markdown(
                                f'<span class="source-badge">SOURCE {source["source_number"]}</span>'
                                f'<span style="color:#6B7280; font-size:0.85rem;">'
                                f'{source["source"]} · Page {source["page"]} · Chunk {source["chunk_id"]}'
                                f"</span>",
                                unsafe_allow_html=True,
                            )
                            st.write(source["content"])
                            st.markdown("<hr style='margin:0.6rem 0;'>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)