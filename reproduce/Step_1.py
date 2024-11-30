import os
os.environ["OPENAI_API_KEY"]=""

import json
import time

from lightrag import LightRAG
from lightrag.llm import gpt_4o_mini_complete
import time



def insert_text(rag, file_path):
    with open(file_path, mode="r", encoding="utf-8") as f:
        unique_contexts = json.load(f)

    retries = 0
    max_retries = 3
    while retries < max_retries:
        try:
            rag.insert(unique_contexts)
            break
        except Exception as e:
            retries += 1
            print(f"Insertion failed, retrying ({retries}/{max_retries}), error: {e}")
            time.sleep(10)
    if retries == max_retries:
        print("Insertion failed after exceeding the maximum number of retries")


cls = "legal"
WORKING_DIR = f""

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(working_dir=WORKING_DIR, llm_model_func=gpt_4o_mini_complete, embedding_func_max_async=16)

for x in range(146,147):

    insert_text(rag, f"")
    print("X"*200)
    print(f"File {x} Inputted")
    time.sleep(60)

