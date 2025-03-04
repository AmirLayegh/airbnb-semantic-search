create-qdrant-database:
	uv run python -m tools.create_qdrant_database

start-superlinked-server:
	uv run python -m superlinked.server

load-data:
	curl -X 'POST' \
	'http://localhost:8080/data-loader/data_schema/run' \
	-H 'accept: application/json' \
	-d ''
	
search-query:
	curl -X 'POST' \
  'http://0.0.0.0:8080/api/v1/search/base_query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"natural_query": "entire apartment in sodermalm with price lower than 1000 and the price not equal to -1 and rating bigger than 4.5."}'