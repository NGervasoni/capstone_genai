from sagemaker.predictor import retrieve_default
endpoint_name = "jumpstart-dft-llama-codellama-13b-i-20240417-060043"
PREDICTOR = retrieve_default(endpoint_name)

def get_answer(prompt, verbose=False):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "top_p": 0.9,
            "temperature": 0.2
        }
    }
    if verbose:
        print( "========= PAYLOAD =========")
        print("payload = " + json.dumps(payload, indent=4, sort_keys=True))
        print( "========= ANSWER =========")
    response = PREDICTOR.predict(payload)
    print(response[0]['generated_text'])
    return response