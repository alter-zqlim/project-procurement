import streamlit as st
import numpy as np
from helper_functions import llm

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

from openai import OpenAI
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

__import__('pysqlite3')
import sys
import pysqlite3
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def loader(filepath):
    loader = PyPDFLoader(filepath)
    return loader.load()

def text_splitter(pages):
    text_chunking = RecursiveCharacterTextSplitter(
        separators = ["\n\n", "\n", " ", ""],
        chunk_size = 500,
        chunk_overlap = 50,
        length_function = llm.count_tokens
    )
    return text_chunking.split_documents(pages)

def write_vector_store(splitted_documents):
    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    return Chroma.from_documents(
        splitted_documents,
        OpenAIEmbeddings(model = 'text-embedding-3-small', openai_api_key = st.secrets["KEY_OPENAI_API"]),
        persist_directory = "./chroma_db"
    )

template = "Use the following pieces of context to answer the question at the end. If you don't know the answer, do not try to make up an answer. Just say that you don't know. Use three sentences maximum. Keep the answer as concise as possible. {context} Question: {question} Helpful Answer:"
prompt = PromptTemplate.from_template(template)
