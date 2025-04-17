from langchain_community.vectorstores.faiss import FAISS

import os
import yaml
from PyPDF2 import PdfReader
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.schema import Document
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")  
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")  

os.environ['GOOGLE_API_KEY'] =  GOOGLE_API_KEY
os.environ['LANGCHAIN_API_KEY'] =  LANGCHAIN_API_KEY
os.environ['LANGCHAIN_PROJECT'] =  LANGCHAIN_PROJECT

cwd = os.getcwd()

def get_document_loader():
    loader = DirectoryLoader(f'{cwd}/resources', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
    docs = loader.load()
    return docs

def get_text_chunks(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        
        chunk_size=1000,
        chunk_overlap=200        
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def get_insurance_docs_embedding():
    file_path = f"{cwd}/faiss_index/index.faiss"
    # Check if file exists
    if not os.path.exists(file_path):
        insurance_docs = get_document_loader()
        insurance_docs_chunks = get_text_chunks(insurance_docs)
        embeddings = OllamaEmbeddings(model="llama2") 
        insurance_docs_embedding = FAISS.from_documents(insurance_docs_chunks, embeddings)
        insurance_docs_embedding.save_local(f"{cwd}/faiss_index")
    else:
        print("File already exists. Skipping function.")

def load_insurance_context():
    vector_store = (FAISS.load_local(f"{cwd}/faiss_index", 
                                     OllamaEmbeddings(), 
                                     allow_dangerous_deserialization=True))
    return vector_store

def load_yaml(path):
    with open(path, "r") as f:
        prompt_data = yaml.safe_load(f)
    return prompt_data

def get_claim_approval_context():
    db = load_insurance_context()
    context = db.similarity_search("What are the documents required for claim approval?")
    claim_approval_context = ""
    for x in context:
        claim_approval_context += x.page_content

    return claim_approval_context

def get_general_exclusion_context():
    db = load_insurance_context()
    context = db.similarity_search("Give a list of all general exclusions")
    general_exclusion_context = ""
    for x in context:
        general_exclusion_context += x.page_content

    return general_exclusion_context

def get_file_content(file):
    text = ""
    pdf = PdfReader(file)
    for page in pdf.pages:
        text = text+page.extract_text()
    return text

def check_claim_rejection(claim_reason, general_exclusion_list, config):
    disease_in_list = any(claim_reason.lower() in disease.lower() for disease in general_exclusion_list)
    if disease_in_list:
        claim_template = config["claim_rejection_template"]
    else :
        claim_template = config["claim_accepting_template"]

    return claim_template



        
