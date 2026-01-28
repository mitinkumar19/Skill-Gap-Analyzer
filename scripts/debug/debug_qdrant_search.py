from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(location=":memory:")
client.create_collection(
    collection_name="test",
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)
client.upsert(
    collection_name="test",
    points=[
        models.PointStruct(id=1, vector=[0.1, 0.1, 0.1, 0.1], payload={"a": 1})
    ]
)

print("Testing query_points...")
try:
    # Try typical search args but with query_points
    res = client.query_points(
        collection_name="test",
        query=[0.1, 0.1, 0.1, 0.1],
        limit=1
    )
    print(f"query_points result type: {type(res)}")
    print(f"query_points result: {res}")
except Exception as e:
    print(f"query_points failed: {e}")

print("\nTesting query...")
try:
    res = client.query(
        collection_name="test",
        query_vector=[0.1, 0.1, 0.1, 0.1],
        limit=1
    )
    print(f"query result type: {type(res)}")
    print(f"query result: {res}")
except Exception as e:
    print(f"query failed: {e}")
