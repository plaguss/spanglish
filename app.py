"""App to translate from english to spanish, using
Helsinki-NLP/opus-mt-en-es model from Hugging face and
ray serve.
"""


import os

from fastapi import FastAPI
from ray import serve
from transformers import pipeline

MODEL_NAME = os.environ.get("MODEL_NAME", "Helsinki-NLP/opus-mt-en-es")

app = FastAPI()


@serve.deployment(route_prefix="/")
@serve.ingress(app)
class SpanglishDeployment:
    def __init__(self):
        # Initialize model state.
        self.pipe = pipeline("translation", model=MODEL_NAME)

    @app.get("/single")
    def predict_one(self, text: str) -> str:
        """Takes a single string as input."""
        return self.pipe(text)[0]["translation_text"]

    @serve.batch(max_batch_size=4)
    async def _handle_batch(self, texts: list[str]) -> dict[str, list[str]]:
        results = self.pipe(texts)
        return [r["translation_text"] for r in results]

    @app.get("/batched")
    async def predict_batch(self, texts: str) -> str:
        """Takes a json encoded list of strings as input."""
        return await self._handle_batch(texts)


translator = SpanglishDeployment.bind()
