from inference import InferenceModel

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q2_K.gguf'
# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q4_K_M.gguf'
# MODEL_PATH = 'models/mistral-7b-instruct-v0.2.Q5_K_S.gguf'
MODEL_PATH = 'models/42dot_LLM-SFT-1.3B_Q4_K_M.gguf'
# MODEL_PATH = 'models/42dot_LLM-SFT-1.3B.gguf'

inference_model = InferenceModel(
    model_path=MODEL_PATH,
    # template_path="template2.txt",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@app.post("/")
def run_model(question: str):
    return StreamingResponse(
        inference_model(question),
        media_type="text/plain",
    )
