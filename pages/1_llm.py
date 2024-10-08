import streamlit as st
from helper_functions.utility import check_password
from helper_functions import llm

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("https://www.developer.tech.gov.sg/products/collections/data-science-and-artificial-intelligence/playbooks/prompt-engineering-playbook-beta-v3.pdf")
pages = loader.load()
