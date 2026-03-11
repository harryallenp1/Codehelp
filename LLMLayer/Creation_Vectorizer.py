'''
By: Tejas Kumar
Created on : 2025-12-27
Last Modified: 2025-12-27
Description: This script processes PDF documents, extracts text and table data, and vectorizes the content using Sentence Transformers.

'''



import json
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from tqdm import tqdm
import os
import pdfplumber
import pandas as pd


PDF_FOLDER = 'PDFs'
META_DATA_FILE = os.path.join(PDF_FOLDER, 'Meta_Data.json')

DB_PATH = "./chroma_db"
COLLECTION_NAME = "Eduction_Planning_Documents"


#Declaring the Embedding Model
print("Loading embedding model...")
model = SentenceTransformer('intfloat/e5-large')
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='intfloat/e5-large')

with open(META_DATA_FILE, 'r') as f:
    meta_data = json.load(f)

#Declaring the chuncking size to 3000 token with an overlap of 200 tokens to make sure context is maintained between chunks.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200
)

# Function to append meta data such as the page number and weather or not the chunck is from a table or paragraph
def append_metadata(base_meta: dict, page_number: int, content_type: str) -> dict:
    meta = base_meta.copy()
    meta["page"] = page_number
    meta["content_type"] = content_type
    return meta


# Process text per page by chunking
def process_page_text(page_text: str, base_meta: dict, page_number: int):
    chunks = text_splitter.split_text(page_text)
    docs = []

    for chunk in chunks:
        docs.append({
            "id": str(uuid4()),
            "text": chunk,
            "metadata": append_metadata(base_meta, page_number, "paragraph_chunk")
        })

    return docs

# Process PDFs and extracting text and page numbers
def Process_PDFs():
    print("Starting PDF processing...")
    all_docs = []

    for ID in tqdm(meta_data.keys(), desc="Processing PDFs"):
        sub_dict = meta_data[ID]
        file_path = os.path.join(PDF_FOLDER, sub_dict['fileName'])
        print(f"Processing file: {file_path}")

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    all_docs.extend(process_page_text(page_text, sub_dict, i))

    return all_docs


#Vectorizing the pre-processed documents and storing them in ChromaDB
def Vectorize_Documents(documents):
    print("Starting vectorization and storage in ChromaDB...")

    #Saving all metadata to a JSON file for future reference.
    all_meta_data = [doc['metadata'] for doc in documents]
    with open('All_Metadata.json', 'w') as f:
        json.dump(all_meta_data, f, indent=4)

    #Instantiating ChromaDB client and creating/ getting the collection
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=ef
    )

    if COLLECTION_NAME in [col.name for col in client.list_collections()]:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )
    else:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )


    print("Adding documents to ChromaDB...")
    #Adding the document chuncking with the according meta data to the collection.
    collection.add(
        documents=[doc['text'] for doc in documents],
        metadatas=[doc['metadata'] for doc in documents],
        ids=[doc['id'] for doc in documents]
    )

    print("Vectorization and storage complete.")

#Consolidated main function to run the processing and vectorization steps.
def main():
    try:
        documents = Process_PDFs()
        Vectorize_Documents(documents)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()