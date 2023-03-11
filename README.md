# spanglish
Spanish to english translator service 

This repo contains an app to translate text from english to spanish. Its an api rest intended for personal use, translating the my blog's posts. The final text may not be perfect, but is a good starting point.

It uses :hugs: Transfomers with [Helsinki-NLP/opus-mt-en-es](https://huggingface.co/Helsinki-NLP/opus-mt-en-es) model, and [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) for model serving.

## Deployment

### Docker

The app is intented to be run from a docker container, take into account the dependencies make it BIG (3GB plus).

It builds from the base ray [docker image](https://hub.docker.com/r/rayproject/ray).

#### Using docker-compose

Build and run the app:

```console
docker compose up --build
```

And stop the app:

```console
docker compose down
```

Or directly from docker, build:

```console
docker build -t spanglish .
```

Run:

```console
docker run -p 8000:8000 -it --env-file=model-name.env spanglish
```

### Local

We can also start the app without docker. Its tested with python 3.10.7 (ray currently fails with python 3.11).

Install the requirements (inside a virtual environment):

```console
pip install -r requirements.txt
```

And start the service:

```console
serve run app:translator
```

Once the service is ready listening (you should see the following message: *Deployed Serve app successfully*), we can start sending requests.

## Send requests

Once the container is running we are ready to test it.

There are two endpoints, one for a single text:

```python
>>> import json
>>> import requests
>>> payload = "hello world"
>>> requests.get("http://localhost:8000/single", params={"text": payload}).json()
'Hola mundo'
```

And one for a batch of texts (see the [ray batching](https://docs.ray.io/en/latest/serve/performance.html#request-batching) docs for more info):

```python
>>> import json
>>> import requests
>>> payload = json.dumps(["hello", "world", "one", "two"])
>>> requests.get("http://localhost:8000/batched", params={"texts": payload}).json()
'["hola", "mundo", "uno", "dos"]'
```

## Notes

Even though the app has been created for translating texts from english to spanish, the 🤗 Transformers API makes it easily interchangeable. For this reason, the model name can be modified via environment variable, updating the [`model-name.env`](model-name.env) file, take a look at the [Helsinki NLP models](https://huggingface.co/Helsinki-NLP) for alternatives!
