# Automating Trustworthy Document Processing with Cleanlab and Unstructured

## Overview
This repository illustrates a system that combines Cleanlab's Trustworthy Language Model (TLM) with Unstructured's document processing capabilities to create reliable document processing pipelines for Retrieval-Augmented Generation (RAG) applications. This repository contains the code for a tutorial that demonstrates how to build such a system.

We addresses three key challenges in building reliable AI systems:
- **Document Preprocessing**: Converting diverse document formats into structured, machine-readable text
- **Hallucination Mitigation**: Reducing false information by grounding LLM responses in verified data
- **Trustworthiness Assessment**: Quantifying the reliability of AI-generated responses

## Installation

### Requirements
- Python 3.8+
- API keys for Cleanlab and Unstructured

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Tonyhrule/Automated-Document-Processing.git
cd Automated-Document-Processing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
CLEANLAB_API_KEY=your_cleanlab_api_key
UNSTRUCTURED_API_KEY=your_unstructured_api_key
UNSTRUCTURED_API_URL=https://api.unstructured.io/general/v0/general
```

## Project Structure

```
Automated-Document-Processing/
├── AutoDoc_Notebook.ipynb   # Interactive tutorial notebook
├── README.md                # This file
├── requirements.txt         # Project dependencies
└── src/                     # Source code
    ├── __init__.py          # Exports DocumentProcessor
    ├── config.py            # Environment configuration
    ├── data/                # Sample data
    │   ├── nfl.pdf          # NFL statistics PDF
    │   └── nfl_tables.json  # Extracted tables from PDF
    ├── document_processor.py # Core document processing class
    ├── helpers/             # Utility functions
    │   ├── data.py          # Data utilities (JSON, file operations)
    │   ├── input.py         # CLI utilities
    │   ├── oai.py           # OpenAI integration
    │   ├── progress.py      # Progress tracking
    │   ├── tlm.py           # TLM integration with LlamaIndex
    │   └── variables.py     # Common variables
    ├── nfl_data.py          # NFL data extraction
    ├── nfl_llm.py           # Query engine for NFL data
    └── pipeline_demo.py     # Full pipeline demonstration
```

## Components

### DocumentProcessor
The core class that handles document processing, table detection, and profile extraction:
- `process_documents()`: Processes text files and generates JSON output
- `detect_table_content()`: Detects tabular data in text
- `extract_profile_info()`: Extracts structured profile information

### TLM Integration
Integration with Cleanlab's Trustworthy Language Model:
- Custom wrappers for TLM and LLM
- Query engines for semantic search and RAG
- Trustworthiness assessment of responses

### Unstructured Integration
Document processing with Unstructured:
- PDF partitioning and table extraction
- Structured data extraction from complex documents
- Preservation of document structure

## Tutorial
For a walkthrough of the system, refer to the [AutoDoc_Notebook.ipynb](AutoDoc_Notebook.ipynb) in this repository.

## Links
- [Cleanlab](https://cleanlab.ai/) for the Trustworthy Language Model
- [Unstructured](https://unstructured.io/) for document processing capabilities

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.