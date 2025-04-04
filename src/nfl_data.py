import os
import unstructured_client
from unstructured_client.models import operations, shared
from helpers.data import save_json
import requests

client = unstructured_client.UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY")
)

file_url = "https://storage.googleapis.com/nfl-2024-record/nfl.pdf"

response = requests.get(file_url)
response.raise_for_status()

file_content = response.content

req = operations.PartitionRequest(
    partition_parameters=shared.PartitionParameters(
        files=shared.Files(
            content=file_content,
            file_name="nfl.pdf",
        ),
        strategy=shared.Strategy.VLM,
        vlm_model=shared.PartitionParametersStrategy.GPT_4O,
        vlm_model_provider=shared.PartitionParametersSchemasStrategy.OPENAI,
        languages=["eng"],
        split_pdf_page=True,
        split_pdf_allow_failed=True,
        split_pdf_concurrency_level=15,
    ),
)

result = client.general.partition(request=req)
if result.elements is None:
    raise Exception("No elements found in the response")

rawTables = [item for item in result.elements if item["type"] == "Table"]
titles = [
    item
    for item in result.elements
    if item["text"].startswith("TOP") or "COACHES" in item["text"]
]

tables = [
    {"title": title["text"], "table": table["metadata"]["text_as_html"]}
    for title, table in zip(titles, rawTables)
]

save_json("data/nfl_tables.json", tables)
