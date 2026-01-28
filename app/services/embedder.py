from sentence_transformers import SentenceTransformer
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            cls._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Model loaded successfully")
        return cls._instance

    def encode(self, text: str | list[str]) -> list[float] | list[list[float]]:
        """
        Generate embeddings for a text or list of texts.
        """
        if self._model is None:
            raise RuntimeError("Embedding model not initialized")
        
        embeddings = self._model.encode(text)
        return embeddings.tolist()

    def get_dimension(self) -> int:
        """Return the dimension of the embeddings."""
        if self._model is None:
            raise RuntimeError("Embedding model not initialized")
        return self._model.get_sentence_embedding_dimension()
