# Automating Trustworthy Document Processing with Cleanlab and Unstructured

## Proposed Sample Pipeline

- Unstructured documents (e.g., PDFs/images) enter [unstructured.io](https://unstructured.io) to make them much easier to process.
- CleanLab TLM is used to extract necessary information.
- Example: Profiles from tables of different types and formats in different documents (first name, last name, gender).
  - CleanLab would be asked: *"From this table/row, provide the user's first name, last name, and gender."*

## Purpose

This project advertises CleanLab by demonstrating that the TLM is a superior drop-in replacement for LLMs in data processing.

- In the unstructured documentation and videos, OpenAI GPT is used to extract data from unstructured.io outputs.
- TLMs are a drop-in replacement for the LLMs but also provide a truthfulness score that can validate data accuracy and detect potentially problematic sources.
- Demonstrates the ease of implementation.

### Repo Structure

- `notebooks/`: Jupyter notebooks for data analysis and visualization
  - `data_validation.ipynb`: Main notebook demonstrating the validation pipeline
- `src/`: Source code for the validation system
  - `data_validation.py`: Core validation logic
  - `document_processor.py`: Document processing utilities
  - `config.py`: Configuration settings

### Setup Process

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   CLEANLAB_API_KEY=your_api_key
   ```

3. Run the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/data_validation.ipynb
   ```

### Analysis Pipeline

1. **Data Loading**: Load medical records from CSV file
2. **Record Analysis**: Process each record using Cleanlab TLM
3. **Trustworthiness Scoring**: Calculate trustworthiness scores
4. **Visualization**: Generate distribution and scatter plots
5. **Results Display**: Show detailed analysis with color-coded trustworthiness

### Visualization Features

- **Distribution Plot**: KDE plot showing trustworthiness score distribution
- **Scatter Plot**: Record-by-record visualization with color gradient
- **Statistics Display**: Comprehensive analysis summary
- **Threshold Line**: Clear indication of review threshold (0.85)
