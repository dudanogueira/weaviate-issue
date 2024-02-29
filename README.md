1. Update line 16 of `setup.py` and `query.py` with your OpenAI API key
2. Run the following commands:

```
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

docker run -d \
  --name db \
  --restart unless-stopped \
  -v weaviate-data:/var/lib/weaviate \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e ENABLE_MODULES=text2vec-openai \
  -e DEFAULT_VECTORIZER_MODULE=text2vec-openai \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -p 8080:8080 \
  -p 50051:50051 \
  semitechnologies/weaviate:1.23.10

python setup.py

python query.py

docker restart db

python query.py
```
