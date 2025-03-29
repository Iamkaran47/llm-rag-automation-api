import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
from src.config.settings import GEMINI_API_KEY
from pathlib import Path
from typing import Dict, List, Optional


class RAGEngine:
    """Retrieval-Augmented Generation (RAG) engine for function execution."""

    def __init__(self, metadata_path: str = "data/function_metadata.json"):
        """Initialize the RAG engine with Gemini Model and embeddings."""
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        genai.configure(api_key=GEMINI_API_KEY)
        self.llm = genai.GenerativeModel("gemini-2.0-flash")
        self.index = None
        self.function_map: Dict[int, Dict] = {}
        self.metadata_path = Path(metadata_path)
        self._load_and_index_functions()

    def _load_and_index_functions(self) -> None:
        """Load function metadata and index with improved embeddings."""
        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata file not found at {self.metadata_path}. Run `python src/core/generate_metadata.py`."
            )

        with open(self.metadata_path, 'r') as f:
            functions = json.load(f)

        # Improve embeddings by including function names and categories
        descriptions = [
            f"{func['name']} - {func['description']} - Category: {func['category']}"
            for func in functions
        ]

        embeddings = self.embedding_model.encode(descriptions, convert_to_numpy=True)

        # Debugging
        # print("\U0001F50D [DEBUG] Generated Embeddings:")
        # for desc, emb in zip(descriptions, embeddings):
        #     print(f"{desc} -> {emb[:5]}...")  # Print first 5 numbers for reference

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        for idx, func in enumerate(functions):
            self.function_map[idx] = func

    def _preprocess_query_with_llm(self, query: str) -> str:
        try:
            prompt = f"""
            You are an AI assistant that maps user queries to known system functions.
            The user asked: "{query}". 
            Your task is to return the closest function from this list:
            {json.dumps([func["name"] for func in self.function_map.values()], indent=2)}
            
            Return ONLY the function name, nothing else.
            """
            response = self.llm.generate_content(prompt)

            if response.candidates:
                mapped_function = response.candidates[0].content.strip()
                print(f"\U0001F50D [DEBUG] Gemini mapped query to function: {mapped_function}")
                return mapped_function

            print("[WARNING] Gemini did not return a valid mapping.")
            return query

        except Exception as e:
            print(f"[ERROR] LLM error: {e}. Using original query.")
            return query  # Fallback in case of API failure

    def retrieve_function(self, query: str) -> Optional[Dict]:
        """Retrieve the best-matching function using Gemini Pro + FAISS."""
        mapped_function = self._preprocess_query_with_llm(query)

        
        for idx, func in self.function_map.items():
            if func["name"] == mapped_function:
                print(f"[DEBUG] Gemini directly matched function: {func['name']}")
                return func

        print("\U0001F50D [DEBUG] No direct match found, using FAISS instead...")
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, k=1)
        best_idx = indices[0][0]

        return self.function_map.get(best_idx)


if __name__ == "__main__":
    rag = RAGEngine()
    func = rag.retrieve_function("Launch Google Chrome")
    print(f"Retrieved function: {func}")
