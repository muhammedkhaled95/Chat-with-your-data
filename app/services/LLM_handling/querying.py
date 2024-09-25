from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.services.LLM_handling.llm_loader import load_llm

# Setting the custom prompt which has 2 variables as its dynamic content ['context', 'question']
# Context: is the top similar context we got from the vector database.
# Question: is the original user que
def set_custom_prompt():
    custom_prompt_template = """Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    if the user doesn't ask for a link, return the answer from the context and the question, if you did not find the answer in the context, 
    try to answer it from your own knowledge, but make sure to mention that you are answering from your own knowledge.

    Context: {context}
    Question: {question}

    If the user asks for a link, only return the link from the context, and nothing else. and the user will ask it like
    open this or that or get me the link to this or that.

    Helpful answer:
    """

    prompt = PromptTemplate(
        template=custom_prompt_template,
        input_variables=['context', 'question']
    )

    return prompt


def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=False,
        chain_type_kwargs={'prompt': prompt}
    )

    return qa_chain


def qa_bot(db_faiss_path, llm_model):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    db = FAISS.load_local(db_faiss_path, embeddings, allow_dangerous_deserialization=True)
    llm = llm_model
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

# Output function
def get_llm_answer(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})

    return response