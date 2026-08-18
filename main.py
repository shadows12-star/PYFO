from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()




llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.2
)




prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI document assistant.

Use ONLY the provided document context to answer the question.

Do not use outside knowledge.

If the answer is not present in the context,
say exactly:

"I could not find the answer in the document."

Keep the answer clear, concise, and factual.
"""
        ),

        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)




def ask_question(vectorstore, query: str) -> dict:

   
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )



    docs = retriever.invoke(query)


    if not docs:

        return {
            "answer":
                "I could not find the answer in the document.",

            "sources": []
        }


    
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )



    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )



    response = llm.invoke(
        final_prompt
    )


   

    sources = []


    for i, doc in enumerate(docs, 1):

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        chunk_id = doc.metadata.get(
            "chunk_id",
            "Unknown"
        )

        source_name = doc.metadata.get(
            "source",
            "Uploaded document"
        )


        # PyPDFLoader uses zero-based pages
        if isinstance(page, int):

            page = page + 1


        sources.append(
            {
                "source_number": i,
                "source": source_name,
                "page": page,
                "chunk_id": chunk_id,
                "content": doc.page_content
            }
        )


  

    return {
        "answer": response.content,
        "sources": sources
    }