import pickle, os
from database import get_products, get_orders, get_faqs
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

VECTOR_FILE = "vector.pkl"
embeddings = OllamaEmbeddings(model="llama3.2:3b")

def create_vector():
    docs = []
    splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)

    # Products
    for product_name, product_desc in get_products():
        content = f"{product_name}: {product_desc}"
        chunks = splitter.split_text(content)
        for chunk in chunks:
            docs.append(Document(page_content=chunk, metadata={"type":"product","name":product_name}))

    # # Orders
    # for order_id, status, product_name in get_orders():
    #     content = f"Pesanan {order_id} untuk {product_name} berstatus {status}"
    #     docs.append(Document(page_content=content, metadata={"type":"order","order_id":order_id}))

    # FAQ
    for q, a in get_faqs():
        content = f"Q: {q}\nA: {a}"
        docs.append(Document(page_content=content, metadata={"type":"faqs","name":q}))

    vector = FAISS.from_documents(docs, embeddings)

    with open(VECTOR_FILE, "wb") as f:
        pickle.dump(vector, f)

def load_vector():
    if not os.path.exists(VECTOR_FILE):
        create_vector()
    with open(VECTOR_FILE, "rb") as f:
        return pickle.load(f)

def rag_query(query, k=6):
    vector = load_vector()
    docs = vector.similarity_search(query, k=k)
    return "\n".join([d.page_content for d in docs])
