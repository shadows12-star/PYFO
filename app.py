import streamlit as st

from document_processor import process_document
from main import ask_question


st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄"
)


st.title(
    "📄 AI Document Intelligence"
)



if "vectorstore" not in st.session_state:

    st.session_state.vectorstore = None


if "file_name" not in st.session_state:

    st.session_state.file_name = None




uploaded_file = st.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)


if uploaded_file is not None:

    if st.button(
        "Process Document"
    ):

        with st.spinner(
            "Processing document..."
        ):

            vectorstore, chunks = (
                process_document(
                    uploaded_file
                )
            )


            st.session_state.vectorstore = (
                vectorstore
            )

            st.session_state.file_name = (
                uploaded_file.name
            )


        st.success(
            f"Processed {len(chunks)} chunks"
        )




if st.session_state.vectorstore:

    st.subheader(
        "Ask questions"
    )


    query = st.text_input(
        "Question"
    )


    if st.button(
        "Ask"
    ):

        result = ask_question(
            st.session_state.vectorstore,
            query
        )


        st.subheader(
            "Answer"
        )

        st.write(
            result["answer"]
        )


        st.subheader(
            "Sources"
        )


        for source in result["sources"]:

            with st.expander(
                f"Page {source['page']} "
                f"| Chunk {source['chunk_id']}"
            ):

                st.write(
                    source["content"]
                )