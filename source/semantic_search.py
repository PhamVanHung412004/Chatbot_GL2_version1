from package import np
from package import Path
from package import faiss
from package import SentenceTransformer
from package import Path
from package import Init_Input
def read_model() -> dict:
    index = faiss.read_index("vector_database.faiss")
    return index

class Sematic_search(Init_Input):
    def __init__(self,model : SentenceTransformer, use_query : str, top_k : int) -> None:
        super().__init__(use_query,top_k)
        self.model = model

    def run(self) -> list:
        index = read_model()
        query_embedding = self.model.encode([self.use_query])[0]
        query_embedding = np.array(query_embedding, dtype="float32").reshape(1, -1)
        D, I = index.search(query_embedding,self.top_k)
        return I