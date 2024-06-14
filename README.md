# LAWS OF NATURE

This is a project that uses retrieval assisted generation to respond to questions about laws.   

The project utilizes [LlamaIndex](https://www.llamaindex.ai/) and [FastAPI](https://fastapi.tiangolo.com/). 

## Project parts

### Lawscaper
Tool used to scrape laws from finlex and to prepare the data for the RAG implementation.    

### Backend
Backend that uses the llama-index framework and fastapi to serve RAG responses to users.   

### Frontend
Currently basic frontend provided by llama-index

## Get started

1. Scrape laws.
2. First, startup the backend. 
3. Second, run the development server of the frontend. 
4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.    