import json
import re
from llama_cpp import Llama

def load_local_llm(model_path: str):
    return Llama(model_path=model_path, n_ctx=4096, verbose=False, n_threads=4)

def extract_from_text(text: str, llm):
    clean_text = re.sub(r'(\d[\d,.]*)\s?(?:KGS|LBS|CBM|PCK|Lbs|Kgs|Gross Weight)', r'[WEIGHT]', text)

    prompt = f"""[INST] <<SYS>>
    You are a shipping auditor. Extract data into JSON. 
    If a value is missing, return "".

    ### The B/L Number (Master Bill) ALWAYS includes the 4-letter Carrier Code at the beginning (e.g., 'ONEY', 'ZIMU', 'YMJA'). 
    DO NOT remove these letters.

    ###
    STRICT RULES:
    1. MBL: Can be labeled as 'MBL', 'B/L No', 'Waybill','Bill of Lading, or 'Invoice Number'.
    2. Container: 4 letters + 7 digits (e.g., ABCD1234567).
    3. Total: Only extract currency amounts. Look for words like 'Total Collect', 'Amount', or '$'. 
    <</SYS>>

TEXT:
{clean_text[:2000]}

RESPONSE JSON:
{{"MBL": "", "Container": [], "Total": ""}} [/INST]"""

    try:
        output = llm(prompt, max_tokens=256, temperature=0.1)
        raw_text = output["choices"][0]["text"].strip()
        
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            if isinstance(data.get("Container"), list):
                data["Container"] = ", ".join(data["Container"])
            return data
    except Exception as e: #debug
        print(f"error: {e}")
        
    return {"MBL or Invoice": "", "Container": "", "Total": ""}