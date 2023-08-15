import openai
import tiktoken

pricing = {
    "gpt-4":{
        "prompt":0.03/1000,
        "response":0.06/1000
    },

    "gpt-4-32k":{
        "prompt":0.06/1000,
        "response":0.12/1000
    },

    "gpt-3.5-turbo":{
        "prompt":0.0015/1000,
        "response":0.002/1000
    },

    "gpt-3.5-turbo-16k":{
        "prompt":0.003/1000,
        "response":0.004/1000
    }
}

def get_completion_cost(text, model_id, type):
    enc = tiktoken.get_encoding("cl100k_base")
    enc = tiktoken.encoding_for_model(model_id)
    token_count = len(enc.encode(text))
    if type == 'prompt':
        return pricing[model_id]['prompt'] * token_count
    elif type == 'response':
        return pricing[model_id]['response'] * token_count


class QAGenerator:
    def __init__(self,
                 api_key,
                 model_id
                 ):
        self.api_key = api_key
        self.model_id = model_id
        self.cost = 0

    def get_completion(self, prompt, **kwargs):
        model_id = self.model_id
        prompt_cost = get_completion_cost(prompt, model_id, type = 'prompt')

        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
        model=self.model_id,
        messages=prompt,
        **kwargs
        )

        resp = response.choices[0].message["content"]
        resp_cost = get_completion_cost(prompt, model_id, type = 'prompt')

        completion_cost = prompt_cost + resp_cost
        self.cost += completion_cost

        return resp