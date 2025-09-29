from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from backend.models.product import Product
import os

DB_FOLDER = "backend/vector_db"
PICKLE_PATH = os.path.join(DB_FOLDER, "faiss_products.pkl")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_faiss_db(pickle_path=PICKLE_PATH):
    if os.path.exists(pickle_path):
        return FAISS.load_local(pickle_path, embedding_model, allow_dangerous_deserialization=True)
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

def extract_query_category(query, categories=["necklace", "earrings", "ring", "nosering", "bracelet"]):
    query_lower = query.lower()
    for category in categories:
        if category in query_lower:
            return category
    return None

async def semantic_search(query: str, db=None, top_k=4, pickle_path=PICKLE_PATH):
    faiss_db = load_faiss_db(pickle_path)
    if not faiss_db and db is not None:
        faiss_db = await build_faiss_db(db, pickle_path)
        if not faiss_db:
            return []
    elif not faiss_db:
        return []
    docs_and_scores = faiss_db.similarity_search_with_score(query, k=top_k)
    
    target_category = extract_query_category(query)

    results = []
    for doc, score in docs_and_scores:
        cat = doc.metadata.get("category", "").lower().strip()
        # Boost score for explicit category match
        if target_category and cat == target_category:
            score += 0.2
        results.append((doc.metadata, score))

    # Sort by score and limit to top_k
    results.sort(key=lambda x: x[1], reverse=True)
    return [meta for meta, score in results[:top_k] if score > 0.8]
