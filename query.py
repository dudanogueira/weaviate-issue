import weaviate
import weaviate.classes as wvc
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType, Tokenization, Configure
import os

client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host="127.0.0.1",
        http_port="8080",
        http_secure=False,
        grpc_host="127.0.0.1",
        grpc_port="50051",
        grpc_secure=False,
    ),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get("OPENAI_APIKEY")
    }
)
client.connect()

collection_name = "MyCollection"
collection = client.collections.get(collection_name)

response = collection.query.fetch_objects(
    limit=5,
    include_vector=True
)
for obj in response.objects:
    print(
        f"fetch_objects: {obj.uuid} ({len(obj.vector['default'])}) | Properties: {obj.properties}")

response = collection.query.hybrid(
    query="data",
    alpha=0.75,
    limit=5,
    include_vector=True
)
for obj in response.objects:
    print(
        f"hybrid query: {obj.uuid} ({len(obj.vector['default'])}) | Properties: {obj.properties}")

client.close()
