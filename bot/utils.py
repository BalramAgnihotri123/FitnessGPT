from pathlib import Path
import os
from dotenv import load_dotenv

import openai #type:ignore


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))


openai.api_key = os.getenv("API_KEY")

CHATGPT_PROMPT_FILTER = "no"

CHATGPT_LINKED_FILTER = "yes"


linked_common_prompt = "I am giving you prompts for a conversation with gpt-3.5, below. Reply with YES, if the context of the Last Prompt can be a follow-up to the response of any of the previous prompts, otherwise say NO"

common_prompt = f'Answer "yes" only if following is a fitness related question otherwise just say: {CHATGPT_PROMPT_FILTER}: '


def generate_fitness_response(prompt, common_prompt, with_stop = True):
    if with_stop:
        prompt_with_history = "\n".join([common_prompt] + [prompt] + ["\nStop:"])
    else:
        prompt_with_history = "\n".join([common_prompt] + [prompt])

    print("prompt send to gpt: ",prompt_with_history)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_with_history[:3000],
        max_tokens=150,
        n=1,
        temperature=0,
        stop="Stop:",
    )
    answer = response.choices[0].text.strip()
    print("answer by gpt: ",answer)

    return answer

def checkPrompt(prompt, common_prompt = common_prompt, with_stop = False):
    response = generate_fitness_response(prompt, common_prompt, with_stop = with_stop)
    if CHATGPT_PROMPT_FILTER in str(response).lower():
        return 0
    else:
        return 1

def checkPromptLinked(prompts):
    prompt = ""
    for i, text in enumerate(prompts):
        prompt += "\n".join([f"Prompt {i+1}: {text}\n"])
    response = generate_fitness_response(prompt, common_prompt = linked_common_prompt)

    if CHATGPT_LINKED_FILTER in str(response).lower():
        print("linked")
        return 1
    else:
        return 0


def get_response(prompt):
    response = generate_fitness_response(prompt, common_prompt = '')
    return response

def get_linked_response(prompt, common_prompt = ''):
    response = generate_fitness_response(prompt, common_prompt)
    return response


