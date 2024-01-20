from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA


# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q2_K.gguf'
# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q4_K_M.gguf'
# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q5_K_S.gguf'
MODEL_PATH = 'models/42dot_LLM-SFT-1.3B_Q4_K_M.gguf'
# MODEL_PATH = 'models/42dot_LLM-SFT-1.3B.gguf'

DB_NAME = "faiss_index_st"


def make_db():
    loader = PyPDFLoader("data/개인정보_보호_가이드라인.pdf")
    data_list = loader.load()

    for data in data_list:
        data.page_content = data.page_content.replace("\x07", "")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(data_list)

    for text in texts:
        print(text)

    embedding_model = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        cache_folder="models",
    )

    faiss_index = FAISS.from_documents(texts, embedding_model)
    faiss_index.save_local(DB_NAME)


def load_db():
    embedding_model = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask",
        cache_folder="models",
        )
    return FAISS.load_local(DB_NAME, embedding_model)


if __name__ == "__main__":
    # 벡터DB 생성
    make_db()
    # 벡터DB 로드
    faiss_index = load_db()
    retriever = faiss_index.as_retriever(search_kwargs={"k": 3})

    llm = LlamaCpp(
        model_path=MODEL_PATH,
        temperature=0,
        top_p=0.98,
        top_k=0,
        n_ctx=32768,
        max_tokens=1024,
        repeat_penalty=1.176,
        last_n_tokens_size=128,
        verbose=False,
        stop=["</s>"],
    )

    template = """\
아래는 대답을 위한 문맥 정보입니다.
---------------------
{context}
---------------------
주어진 문맥 정보와 사전 지식을 활용하여, 다음 질문에 대한 답변을 해주세요.
만약 답변을 찾을 수 없다면, '죄송합니다. 잘 모르겠어요.'라고 답변하세요.

질문: {question}
답변: \
"""

    prompt = PromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    retrievalQA = RetrievalQA.from_llm(llm, prompt, retriever=retriever)

    while True:
        query = input("질문: ")

        print(retrievalQA.invoke(query)["result"])
