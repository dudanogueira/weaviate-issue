import weaviate
import os
import weaviate.classes as wvc
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType, Tokenization, Configure

client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host="localhost",
        http_port="8080",
        http_secure=False,
        grpc_host="localhost",
        grpc_port="50051",
        grpc_secure=False,
    ),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ.get("OPENAI_APIKEY")
    }
)
client.connect()

collection_name = "MyCollection"
client.collections.delete(collection_name)

collection = client.collections.create(
    name=collection_name,
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-large",
        dimensions=1024,
        type_="text",
        vectorize_collection_name=False
    ),
    properties=[
        Property(
            name="text",
            data_type=DataType.TEXT,
            tokenization=Tokenization.WORD
        )
    ]
)

# Create a single object
response = collection.data.insert(
    properties={
        "text": "Some data"
    }
)
print(f"UUID for new object created: {response}")

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
