import json
from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from utils import is_valid_json_format

def generate_single_conversation(user_input_json, system_message: str, max_retries=3) -> str:

    conversation_prompt = f"{user_input_json}"

    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local("faiss_index", embeddings)

    query = conversation_prompt
    embedding_vector = embeddings.embed_query(query)
    docs_and_scores = db.similarity_search_by_vector(embedding_vector)

    chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff")

    retries = 0
    response_str = ""

    while retries < max_retries:
        response = chain({"input_documents": docs_and_scores, "question": f"{system_message} {query}"}, return_only_outputs=True)

        try:
            if isinstance(response, dict):
                response_dict = response
            else:
                response_dict = json.loads(response)
        except json.JSONDecodeError:
            retries += 1
            continue

        if is_valid_json_format(response_dict):
            break

        retries += 1

    return response_dict

def generate_multiple_conversations(user_input_json, system_message: str, max_retries=3) -> str:

    conversation_prompt = f"{user_input_json}"

    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local("faiss_index", embeddings)

    query = conversation_prompt
    embedding_vector = embeddings.embed_query(query)
    docs_and_scores = db.similarity_search_by_vector(embedding_vector)

    chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff")

    retries = 0
    response_str = ""

    while retries < max_retries:
        response = chain({"input_documents": docs_and_scores, "question": f"{system_message} {query}"}, return_only_outputs=True)

        try:
            if isinstance(response, dict):
                response_dict = response
            else:
                response_dict = json.loads(response)
        except json.JSONDecodeError:
            retries += 1
            continue

        if is_valid_json_format(response_dict):
            break

        retries += 1

    return response_dict
