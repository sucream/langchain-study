from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


class InferenceModel:
    def __init__(self, model_path: str, template_path: str = "template.txt"):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        self.model_path = model_path
        self.template = template
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
        )
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=0.1,
            n_ctx=32768,
            max_tokens=512,
            top_p=0.98,
            top_k=5,
            repeat_penalty=1.176,
            last_n_tokens_size=128,
            verbose=False,
            stop=["</s>"],
        )

    def __call__(self, user_input):
        for chunk in self.llm.stream(self.prompt.format(question=user_input)):
            yield chunk
