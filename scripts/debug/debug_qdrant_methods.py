from qdrant_client import QdrantClient

client = QdrantClient(location=":memory:")
methods = [m for m in dir(client) if not m.startswith('_')]
print(f"Methods: {methods}")
print(f"Has query_points: {'query_points' in methods}")
print(f"Has query: {'query' in methods}")
