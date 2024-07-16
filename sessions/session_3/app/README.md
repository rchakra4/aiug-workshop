# Streamlit AI Agents Application

This Streamlit application serves as an interface for interacting with three distinct AI agents, each designed to perform specific tasks. The application is structured with a main entry point (Home.py) and additional pages for each agent, facilitating user interaction and showcasing the capabilities of each AI model. The streamlit application also uses a fastapi backend for a agent #1 (ReAct) and agent #3 (RAG) endpoints.

## Installation

To run this application, you need to have Python installed on your system.

Once Python is installed, you can install Streamlit and other required packages using pip:

Add any other packages your application depends on in the same way.

You also need OpenAI, Langchain, and Tavily API keys.

## Running the Application

To start the application, navigate to the application's root directory in your terminal and run:

streamlit run Home.py

This command launches the Streamlit web server and opens the application in your default web browser.

To run the fastapi backend for the LLM endpoints:

fastapi dev main.py

Application Structure
Home.py: The main entry point of the application. It provides an overview of the different AI agents.

/pages:

Each page within this folder is connected to a different AI agent, designed to showcase a specific functionality or use case. The pages include:
Page 1: Connected to AI Agent 1. ReAct agent with web search tools.
Page 2: Connected to AI Agent 2. Basic agent built on OpenAI API with memory and Chain of Thought
Page 3: Connected to AI Agent 3. Retrieval Augmented Generation Pipeline

Usage
After launching the application, use the sidebar to navigate between the home page and the different AI agents. Each page provides an interface to interact with the respective AI agent, allowing you to input data or queries and receive responses.
