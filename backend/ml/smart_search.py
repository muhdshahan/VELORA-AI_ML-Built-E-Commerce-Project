from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from backend.models.product import Product
import os

DB_FOLDER = "backend/vector_db"
PICKLE_PATH = os.path.join(DB_FOLDER, "faiss_products.pkl")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_faiss_db(pickle_path=PICKLE_PATH):
    if os.path.exists(pickle_path):
        return FAISS.load_local(pickle_path, embedding_model)
    return None

async def build_faiss_db(db, pickle_path):
    q = await db.execute(Product.__table__.select())
    products = q.fetchall()
    if not products:
        return None
    product_texts = [f"{row.name} {row.category} {row.description or ''}" for row in products]
    metadatas = [{
        "id": row.id,
        "name": row.name,
        "category": row.category,
        "price": row.price,
        "description": row.description
    } for row in products]
    faiss_db = FAISS.from_texts(product_texts, embedding_model, metadatas=metadatas)
    faiss_db.save_local(pickle_path)
    return faiss_db

async def semantic_search(query: str, db=None, top_k=10, pickle_path=PICKLE_PATH):
    faiss_db = load_faiss_db(pickle_path)
    if not faiss_db and db is not None:
        faiss_db = await build_faiss_db(db, pickle_path)
        if not faiss_db:
            return []
    elif not faiss_db:
        return []
    docs_and_scores = faiss_db.similarity_search_with_score(query, k=top_k)
    return [doc.metadata for doc, score in docs_and_scores if score > 0.2]
