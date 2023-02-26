"""App to translate from english to spanish, using
Helsinki-NLP/opus-mt-en-es model from Hugging face and
ray serve.
"""


from starlette.requests import Request
from transformers import pipeline

from ray import serve

MODEL_NAME = "Helsinki-NLP/opus-mt-en-es"


# 1: Define a Ray Serve deployment.
@serve.deployment(route_prefix="/")
class SpanglishDeployment:
    def __init__(self):
        # Initialize model state.
        self.pipe = pipeline("translation", model=MODEL_NAME)

    def predict_one(self, text: str) -> str:
        return self.pipe(text)[0]["translation_text"]

    @serve.batch(max_batch_size=4)
    async def predict_batch(self, inputs: list[str]) -> list[str]:
        results = self.pipe(inputs)
        return [r["translation_text"] for r in results]

    async def __call__(self, request: Request) -> dict[str, str]:
        return await self.predict_batch(request.query_params["text"])
        # return {"translated": self._predict(request.query_params["text"])}


translator = SpanglishDeployment.bind()
