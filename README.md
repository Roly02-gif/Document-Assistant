# Document Assistant

A document assistant that ingests a PDF, converts it to Markdown, splits the text into chunks, indexes the chunks in Weaviate, and answers user questions using an LLM.

## Features

- Convert PDF to Markdown with `pymupdf` and `pymupdf4llm`
- Split documents into structured chunks
- Index chunks in a Weaviate collection
- Perform hybrid semantic search with query embeddings
- Build an enriched prompt for the LLM from retrieved chunks
- Call an LLM via OpenAI / OpenRouter to generate answers

## Use case

This project is especially suited for documents that are already organized into short sections, such as rules, regulations, laws, policies, or other structured reference texts. The chunking logic groups content by headings so each chunk can represent a single rule, article, or section for better retrieval.

## Prerequisites

- Python 3.14+
- A reachable Weaviate instance
- An OpenRouter-compatible API key

## Installation

1. Clone the repository

```bash
git clone <repo-url>
cd Document-Assistant
```

2. Install dependencies

```bash
uv install -r requirements.txt
```

> If `requirements.txt` does not exist, install from `pyproject.toml`:

```bash
uv install .
```

3. Create a `.env` file at the project root

```env
OPENROUTER_API_KEY=your_openrouter_key
WEAVIATE_URL=https://your-weaviate-endpoint
WEAVIATE_API_KEY=your_weaviate_key
```

## Usage

Run the main script:

```bash
python main.py
```

Then:

1. Enter the path to the PDF document to ingest
2. Wait for conversion and indexing
3. Ask questions to the chatbot
4. Type `quit` to exit

## Project structure

- `main.py`: entry point and user interaction loop
- `proccess_doc.py`: PDF -> Markdown conversion and chunking
- `vector_db.py`: insert chunks into Weaviate
- `retriever.py`: query Weaviate for relevant chunks
- `prompt_builder.py`: build the final prompt for the LLM
- `llm_call.py`: call the LLM API
- `tests/`: unit tests

## Customization

- Change the LLM model in `llm_call.py`
- Adjust the chunking logic in `proccess_doc.py`
- Change the number of results returned by `retrieve_from_vector_db`

## Notes

- The project requires `WEAVIATE_URL` and `WEAVIATE_API_KEY` to store and search embeddings.
- PDFs are converted to Markdown and split by `##` headings.
- The final prompt assembles the best matching chunks before querying the LLM.
