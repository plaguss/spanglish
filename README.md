# spanglish
Spanish to english translator service 

This repo contains an app to translate text from english to spanish. Its an api rest intended for personal use, translating the my blog's posts. The final text may not be perfect, but is a good starting point.

It uses :hugs: Transfomers with [Helsinki-NLP/opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) model, and [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) for model serving.

## Deploy with docker

The app is intented to be run from a docker container, take into account the dependencies make it BIG (3GB plus).

### Building the container

```console
docker build -t spanglish .
```

### Running

```console
docker run -p 8000:8000 -it spanglish
```

### Send requests

Once the container is running (it may take a while, the server needs some time to be ready).

From a different console, check it works using python's requests:

```python
>>> import json
>>> import requests
>>> payload = json.dumps(["Hello world one", "hello world two"])
>>> print(requests.get("http://localhost:8000/", params={"text": payload}).json())
['Hola mundo uno', 'Hola mundo dos']
```

## Local deployment

The app can be started without using docker. Its tested with python 3.10.7 (ray currently fails with python 3.11).

Install the requirements (inside a virtual environment):

```console
pip install -r requirements.txt
```

And start the service:

```console
serve run app:translator
```

Once the service is ready listening, just send the requests as in the Docker example.


## Next steps

- Use FastAPI to make it more general.
    - Add two endpoints, one for a single piece of text.
    - a second (the current one) to allow processing a batch of texts.
- Allow passing the model name as argument to the container.

<!-- ## Deploy with docker compose

The final image is **BIG**.

Start the service:

```console
docker compose up --build
```

Stop it:

```console
docker compose down
``` -->
