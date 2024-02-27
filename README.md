import pprint
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from embedding import generate_embeddings
from process_data import scrap_web
import re
from langchain_community.document_loaders import WebBaseLoader

from langchain.chains import (
            StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
        )

from langchain_core.prompts import PromptTemplate
# from langchain_community.llms import G
from langchain_community.vectorstores.chroma import Chroma
from langchain_google_genai import GoogleGenerativeAI

from langchain_community.embeddings import FakeEmbeddings
from langchain.memory import ConversationBufferMemory

embeddings = FakeEmbeddings(size=1352)
from langchain.schema.messages import HumanMessage, SystemMessage,AIMessage

loader = WebBaseLoader("https://python.langchain.com/docs/integrations/vectorstores/chroma")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDVkdoPKIDhyHw0frL6pTY8yvZEwCLrST4",verbose=True)
llm.verbose = True
# combine_docs_chain = StuffDocumentsChain()
vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory="./chroma_db",collection_name="langchain2")
retriever = vectorstore.as_retriever()
import langchain
langchain.debug = True

# This controls how the standalone question is generated.
# Should take `chat_history` and `question` as input variables.


messages = [
    SystemMessage(content="always reply in chinese"),
    HumanMessage(content="hi my name is joe"),
    AIMessage(content="hi joe, how are you?"),
]
memory=ConversationBufferMemory(ai_prefix="AI Assistant")

# prompt = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone 
# question.

# Chat History:
# {chat_history}
# Follow Up Input: {question}
# Standalone question:""")

prompt = PromptTemplate.from_template("""Given the following conversation Context and a follow up question,
rephrase the follow up question to be a standalone question such that it maintain the context of old conversation.
also return the system message as it is

Chat History:
{chat_history}

Follow Up Input: {question}

System Message:

Standalone question:""")


# prompt = PromptTemplate.from_template("""Use the following pieces of context and chat history to answer the 
# question at the end.
# If you don't know the answer, just say that you don't know, 
# don't try to make up an answer.
# Chat history: {chat_history}\n\nQuestion: {question}""")
chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    # rephrase_question=False,
    condense_question_prompt=prompt
    
    # verbose=True
    # memory=memory
)
chat_history=[('hi my name is rahul','hi rahul, how are you?')]
# chat_history.append(('bot','hi joe, how are you?'))

print(chat_history)
res = chain({"question":"what is my name?", "chat_history":messages})
print(res)


# pp = pprint.PrettyPrinter(indent=4)
# client = chromadb.PersistentClient(path="chroma_db")
# collection = client.get_or_create_collection("langchain2")
# recursive_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=30,
#     length_function=len,
#     is_separator_regex=False,
#     )



# def prepare_data(text_splitter, raw_data):
#     texts = text_splitter.create_documents([raw_data])
#     return texts


# def save_to_database( splitted_chunks,metadata, embeddings=None):
#     ids = []
#     metadatas = []
#     documents = []
#     id = 1
#     print(metadata)
#     for chunk in splitted_chunks:
#         ids.append("id_"+str(id))
#         id = id +1 
#         metadatas.append(metadata)
#         documents.append(chunk.page_content)
    
#     if(embeddings):
#         collection.add(
#             embeddings=embeddings,
#             documents=documents,
#             metadatas=metadatas,
#             ids=ids
#         )
#     else:
#         collection.add(
#             documents=documents,
#             metadatas=metadatas,
#             ids=ids
#         )
        
    
 
# def run():
#     urls = [
#         'https://www.hindustantimes.com/education/news/iit-hyderabad-to-host-the-second-edition-of-r-d-innovation-fair-iinventiv-101704460769704.html'
#     ]
#     for url in urls:
#         print(url)
        
#         raw_data =  scrap_web(url)
#         # print(raw_data.page_content)
#         splitted_chunks = prepare_data(recursive_splitter, raw_data.page_content)
#         pp.pprint(splitted_chunks)
#         embeddings = generate_embeddings([splitted_chunks],'UAE-Large-V1')
#         save_to_database(splitted_chunks,raw_data.metadata,embeddings)
#         print('+================================== DATA SAVED =======================================+')
        
        
# run()

# querry = "give me information on Ministry of Education's at flagship event IInvenTiv-2024 "
# print(default_ef([querry]))
# results = collection.query(
#     query_embeddings=default_ef([querry]),
#     n_results=4
# )
# # pp.pprint(results)
# context = ''
# for result in results["documents"][0]:
    
#     context  = context + result + '\n'
#     pp.pprint(re.sub(r'\n+', '\n', result))
#     print('________________________________________________________________________________________________________')
        
# context = re.sub(r'\n+', '\n', context)
# prompt = f"""
#         With the following context 
#         `{context}`
        
#         response to the querry
#         `{querry}`
# """
        
# import requests

# url = 'http://localhost:3000/api/data'



# data = {'message': prompt}
# headers = {'Content-Type': 'application/json'}

# response = requests.post(url, json=data, headers=headers)

# if response.status_code == 200:
#     res = response.json()
#     # print(f'Success! Server response: {response.json()}')
#     print('________________________________________________________________________________________________________')
#     pp.pprint(res["message"])
#     print('________________________________________________________________________________________________________')
#     pp.pprint(res["response"])
    
    
# else:
#     print(f'Error! Server response: {response.status_code} - {response.text}')
