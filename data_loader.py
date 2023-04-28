import os
from langchain.document_loaders import TextLoader

def load_text_data(file_list_path: str) -> [TextLoader]:
    docs = []
    for dirpath, dirnames, filenames in os.walk(file_list_path):
        for file in filenames:
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e:
                print(f"Error loading file {file}: {e}")
                pass
    print(f"Loaded {len(docs)} documents.")
    return docs
