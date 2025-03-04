from urllib.parse import urlparse, urlunparse
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from superlinked_app import setting


assert (
    setting.QDRANT_CLUSTER_URL
    ), "QDRANT_CLUSTER_URL must be set in the environment variables"
assert (
    setting.QDRANT_COLLECTION_NAME
    ), "QDRANT_COLLECTION_NAME must be set in the environment variables"

logger.info("Connecting to Qdrant cluster: %s", setting.QDRANT_CLUSTER_URL)

client = QdrantClient(
    url=setting.QDRANT_CLUSTER_URL.get_secret_value(),
    api_key=setting.QDRANT_API_KEY.get_secret_value(),
    #vectors_config=VectorParams(size=768, distance=Distance.Cosine),
)

def create_database(collection_name: str, vector_size: int = 768):
    logger.info("Creating collection: %s", collection_name)
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        logger.info("Collection created: %s", collection_name)
        return True
    except Exception as e:
        logger.exception("An exception occurred: %s", e)
        logger.error("Failed to create collection: %s", e)
        return False

if __name__ == "__main__":
    create_database(setting.QDRANT_COLLECTION_NAME)
