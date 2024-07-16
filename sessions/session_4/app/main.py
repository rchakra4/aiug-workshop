from typing import Dict
from fastapi import FastAPI
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent

import re
from dotenv import load_dotenv

load_dotenv()


###########################
### ReAct Search Agent ####
###########################

# Create the agent with memory and search tool
memory = SqliteSaver.from_conn_string(":memory:")
model = ChatOpenAI(model='gpt-4o')
search = TavilySearchResults(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

###########################
###   Nutrition Agent  ####
###########################

# load docs
from langchain_community.document_loaders import PyPDFLoader
import os

file_path = "../pdfs"
docs = []
for file in os.listdir(file_path):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(file_path, file)
        loader = PyPDFLoader(pdf_path)
        docs.extend(loader.load())

# split and index
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=0)

chunked_docs = splitter.split_documents(docs)

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

db = FAISS.from_documents(chunked_docs, HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5"))

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# model_name = "HuggingFaceH4/zephyr-7b-beta"
model_name ="TinyLlama/TinyLlama-1.1B-Chat-v1.0"

save_directory = "../notebooks/model_directory"

# Get the list of files and directories in 'save_directory'
directory_contents = os.listdir(save_directory)

# Check if the directory is empty
if not directory_contents:
    print(f"The directory {save_directory} is empty.")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    tokenizer.save_pretrained(save_directory)
    model.save_pretrained(save_directory)

else:
    print(f"The directory {save_directory} contains {len(directory_contents)} items.")
    model = AutoModelForCausalLM.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)


from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    do_sample=True,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=400,
)

llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

prompt_template = """
<|system|>
Answer the question based on your knowledge. Use the following context to help:

{context}

</s>
<|user|>
{question}
</s>
<|assistant|>

 """

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

llm_chain = prompt | llm | StrOutputParser()

from langchain_core.runnables import RunnablePassthrough

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | llm_chain


###########################
###    App Endpoint    ####
###########################

app = FastAPI()

@app.post("/nutrition")
def generate_nutrition(data: Dict):
    question = data['question']
    response = rag_chain.invoke(question)
    print(response)
    
    # Regular expression to match everything after <|assistant|>
    pattern = r"(?<=<\|assistant\|>)[\s\S]*$"
    
    # Perform the regex search
    match = re.search(pattern, response, re.DOTALL)

    # Check if a match is found and print the result
    if match:
        result = match.group().strip()
        print(result)
    else:
        result = "Try again"
        
    return {"response": result}

@app.post("/event")
@app.post("/event")
def generate_events(data: Dict):
    print(data)
    event_type = data["event_type"]
    location = data["location"]
    time_frame = data["time_frame"]
    user_input = f"Find me {event_type} events in {location} around {time_frame} time frame in 2024. Return back specific events."

    # Set memory for a specific user
    config = {"configurable": {"thread_id": "rc45"}}

    response = agent_executor.invoke({"messages": [("user", user_input)]}, config)

    response = response["messages"][-1].content
    return {"response": response}