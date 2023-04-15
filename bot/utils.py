from pathlib import Path
import os
from dotenv import load_dotenv

import openai #type:ignore


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))


openai.api_key = os.getenv("API_KEY")

CHATGPT_PROMPT_FILTER = "not fitness related"

CHATGPT_LINKED_FILTER = "YES"


linked_common_prompt = "Type YES if the last prompt is related to the previous two, otherwise type NO."

common_prompt = f'Answer only if following is a fitness related question otherwise just say: {CHATGPT_PROMPT_FILTER}: '


def generate_fitness_response(prompt, common_prompt):
    prompt_with_history = "\n".join([common_prompt] + [prompt] + ["\nStop:"])
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_with_history[:4000],
        max_tokens=1500,
        n=1,
        temperature=0,
        stop="Stop:",
    )
    answer = response.choices[0].text.strip()
    return answer

def checkPrompt(prompt, common_prompt = common_prompt):
    response = generate_fitness_response(prompt, common_prompt)
    if CHATGPT_PROMPT_FILTER in str(response).lower():
        return 0
    else:
        return 1

def checkPromptLinked(prompts):
    prompt = ""
    for i, text in enumerate(prompts):
        prompt = "\n".join([f"Prompt {i}: {text}"])
    response = generate_fitness_response(prompt, common_prompt = linked_common_prompt)

    if str(response).__contains__(f"{CHATGPT_LINKED_FILTER}"):
        return 1
    else:
        return 0


def get_response(prompt):
    response = generate_fitness_response(prompt, common_prompt)
    return response

def get_linked_response(prompt, common_prompt = ''):
    response = generate_fitness_response(prompt, common_prompt)
    return response


