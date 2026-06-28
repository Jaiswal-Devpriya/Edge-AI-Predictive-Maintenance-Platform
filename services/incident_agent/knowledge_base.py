import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb


ROOT_DIR = Path(__file__).resolve().parents[2]
HISTORICAL_FAILURES_PATH = ROOT_DIR / "data" / "historical_failures.json"
RUNBOOKS_PATH = ROOT_DIR / "data" / "knowledge_base" / "maintenance_runbooks.txt"
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"


class KnowledgeBase:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))
        self.collection = self.client.get_or_create_collection(
            name="maintenance_knowledge"
        )

    def build_index(self):
        documents = []
        ids = []

        with open(HISTORICAL_FAILURES_PATH, "r") as file:
            failures = json.load(file)

        for failure in failures:
            text = (
                f"Failure ID: {failure['failure_id']}. "
                f"Component: {failure['component']}. "
                f"Symptoms: {failure['symptoms']}. "
                f"Root cause: {failure['root_cause']}. "
                f"Resolution: {failure['resolution']}."
            )
            documents.append(text)
            ids.append(failure["failure_id"])

        with open(RUNBOOKS_PATH, "r") as file:
            runbooks = file.read().split("\n\n")

        for index, runbook in enumerate(runbooks):
            if runbook.strip():
                documents.append(runbook.strip())
                ids.append(f"RUNBOOK-{index + 1}")

        embeddings = self.embedding_model.encode(documents).tolist()

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
        )

        return len(documents)

    def search(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode([query]).tolist()[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results["documents"][0]