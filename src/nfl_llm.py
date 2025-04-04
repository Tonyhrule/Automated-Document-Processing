from helpers.data import read_json
from helpers.tlm import tlm_query_engine, llm_query_engine

data = read_json("data/nfl_tables.json")

query_engine = tlm_query_engine(
    [f"<h1>{table['title']}</h1>\n{table['table']}" for table in data]
)

while True:
    query = input('Enter your query ("exit" to exit): ')
    if query == "exit":
        break

    print(query_engine.query(query))
