import os
import re
import tempfile

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
embedding_model = MistralAIEmbeddings(
    model="mistral-embed"
)


def clean_text(text: str) -> str:

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def load_pdf(uploaded_file):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_path = temp_file.name


    loader = PyPDFLoader(
        temp_path
    )

    docs = loader.load()


    for doc in docs:

        doc.page_content = clean_text(
            doc.page_content
        )

        doc.metadata["source"] = (
            uploaded_file.name
        )


    os.remove(
        temp_path
    )

    return docs


def load_txt(uploaded_file):

    text = uploaded_file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

    text = clean_text(text)


    return [
        Document(
            page_content=text,
            metadata={
                "source": uploaded_file.name,
                "page": 0
            }
        )
    ]


def process_document(uploaded_file):

  

    if uploaded_file.name.lower().endswith(
        ".pdf"
    ):

        docs = load_pdf(
            uploaded_file
        )


    elif uploaded_file.name.lower().endswith(
        ".txt"
    ):

        docs = load_txt(
            uploaded_file
        )


    else:

        raise ValueError(
            "Unsupported file type"
        )


 

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )


    chunks = splitter.split_documents(
        docs
    )


    # Metadata


    for i, chunk in enumerate(chunks):

        chunk.metadata[
            "chunk_id"
        ] = i



    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        
    )


    return vectorstore, chunks