import subprocess

import json

from sagemaker.predictor import retrieve_default
endpoint_name = "jumpstart-dft-llama-codellama-13b-i-20240417-060043"
PREDICTOR = retrieve_default(endpoint_name)

def get_answer(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "top_p": 0.9,
            "temperature": 0.2
        }
    }
    print( "========= PAYLOAD =========")
    print("payload = " + json.dumps(payload, indent=4, sort_keys=True))
    response = PREDICTOR.predict(payload)
    print( "========= ANSWER =========")
    print(response[0]['generated_text'])
    return response
    
def followup_prompt(prev_prompt, prev_respose, new_prompt):
    p = ""
    if not prev_prompt.startswith('<s>'):
        p = '<s>'
    p = p + prev_prompt + '\n' + prev_respose + '</s>'
    p = p + f'<s>[INST]\n{new_prompt}\n[/INST]'
    return p

