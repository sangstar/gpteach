import openai
import tiktoken
import numpy as np

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

def generate_prompt(section):
    prompt = f"""
You are a helpful assistant that takes sections of text from a Wikipedia article and creates questions and answers based on the article.
Create question and answers in a format where the question is labeled "Q:" and the answer is labeled "A:"
Separate each question and answer pair with a \n\n

#Article Section#:
{section}

#Generated Questions and Answers#:

"""
    return prompt

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
                 model_id,
                 prompt_generator = generate_prompt
                 ):
        self.api_key = api_key
        self.model_id = model_id
        self.cost = 0
        openai.api_key = self.api_key
        self.prompt_generator = prompt_generator
        self.cost_history = []

    def get_completion(self, prompt, **kwargs):
        model_id = self.model_id
        prompt_cost = get_completion_cost(prompt, model_id, type = 'prompt')

        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
        model=self.model_id,
        messages=messages,
        **kwargs
        )

        resp = response.choices[0].message["content"]
        resp_cost = get_completion_cost(prompt, model_id, type = 'prompt')

        completion_cost = prompt_cost + resp_cost
        self.cost += completion_cost
        self.cost_history.append(completion_cost)

        return resp

    def cost_from_sections(self, sections):
        cost = 0
        prompt_generator = self.prompt_generator
        model_id = self.model_id
        for section in sections:
            prompt = prompt_generator(section)
            cost += get_completion_cost(prompt, model_id, type = 'prompt')
        return cost 
        

    def qas_from_sections(self, sections):
        qas = []
        prompt_generator = self.prompt_generator
        for section in sections:
            prompt = prompt_generator(section)
            response = self.get_completion(prompt)
            qas.append(response)
        return qas

    def estimate_cost(self, sections, num_to_test = 5):
        qas = self.qas_from_sections(sections[:num_to_test])
        qa_costs = self.cost_history[-num_to_test:]
        nominal = np.mean(qa_costs)
        uncertainty = np.std(qa_costs)/np.sqrt(num_to_test)
        print(f'{nominal} +- {uncertainty}')
        return nominal, uncertainty


    
