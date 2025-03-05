# Airbnb Semantic Search

A cutting-edge **semantic search system** for Airbnb listings, leveraging **[Superlinked](https://www.superlinked.com/)** for multi-attribute vector indexing and **[Qdrant](https://qdrant.tech/)** for high-performance vector search. This system enables **natural language queries** to retrieve relevant listings by embedding different attributes (e.g., price, location, and descriptions) using specialized embedding models, ensuring highly accurate and context-aware search results.

![Airbnb Search Banner](/sources/airbnb-superlinked-dark.png)

## 🌟 Features

- **Semantic Search for Structured Data**: Enables natural language queries like "cozy apartments with a view under $150 with rating above 4.5" to retrieve relevant Airbnb listings based on multiple attributes.
- **Multi-Attribute Vector Indexing**: Each column in the Airbnb dataset is embedded using a specialized model (e.g., float-specific embeddings for price, text embeddings for descriptions).
- **Vector Database Integration**: Powered by Qdrant for efficient similarity searches.
- **RESTful API Endpoints**:  Built with FastAPI for efficient and scalable backend operations.
- **Interactive UI**: Uses [Streamlit](https://streamlit.io/) to provide an intuitive front-end interface for searching Airbnb listings.

## 📁 Project Structure

```
├── superlinked_app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration settings
│   ├── constants.py         # Constants definition
│   ├── index.py             # Data schema definition
│   ├── query.py             # Query configurations
│   └── vdb.py               # Vector database setup
├── tools/
│   ├── create_qdrant_database.py  # Database initialization tool
│   ├── st_app.py                  # Enhanced Streamlit UI
│   └── streamlit_app.py           # Basic Streamlit UI
├── .env.example                   # Environment variables 
├── app.py                   # Python file for in memory development when we trun Qdrant vdb off.
├── Makefile                 # Automation for common development tasks
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Project documentation
```

## 🔧 Technologies
![Airbnb semantic search](/sources/airbnb-semantic-search-ui.png)
- **Superlinked Framework**: For semantic search capabilities
- **Qdrant**: Vector database for efficient similarity search
- **OpenAI API**: Natural language understanding
- **Streamlit**: Interactive web interface
- **uv**: Fast Python package installer and resolver

## 💾 Dataset  
We use a **publicly available dataset** containing **Airbnb listings in Stockholm**, sourced from [Inside Airbnb](http://insideairbnb.com/), which provides detailed metadata about rental properties.  

- The dataset includes key attributes such as **listing descriptions, prices, locations, property types, availability, and ratings**.  
- This structured data enables **multi-attribute semantic search**, allowing users to query Airbnb listings based on various factors like price range, neighborhood, and amenities.  

## 📥 Installation

### Prerequisites

- Python 3.11+
- Qdrant Cloud account (or local Qdrant instance)
- OpenAI API key

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/AmirLayegh/airbnb-semantic-search.git
cd airbnb-semantic-search
```

2. Install dependencies using uv:
```bash
# Create a virtual environment (if not created)
uv venv

# Install dependencies from pyproject.toml in editable mode
uv install -e .

# OR (Preferred for installing all dependencies with version locking)
uv sync

```


3. Create a `.env` file in the root directory with your credentials:
```
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CLUSTER_URL=your_qdrant_cluster_url
OPENAI_API_KEY=your_openai_api_key
```

4. Update the `DATA_PATH` in `superlinked_app/config.py` to point to your Airbnb listings dataset.

## 🚀 Getting Started

1. Create a Qdrant collection (first-time setup):
```bash
python tools/create_qdrant_database.py
```
   
   Or using the Makefile:
```bash
make create-qdrant-database
```

2. Start the Superlinked server:
```bash
python -m superlinked.server
```
   
   Or using the Makefile:
```bash
make start-superlinked-server
```

3. Load the data into Qdrant collection:
```bash
make load-data
```

4. Run the Streamlit UI app:
```bash
make streamlit-run
```

5. Open your browser at `http://localhost:8501` to access the application.

## 🔍 Usage

### Basic Search

Enter natural language queries in the search bar like:
- "Apartments in old town with a view"
- "Affordable homes under $100 per night"
- "Top-rated places with pool and wifi"

### Advanced Filters

Use the sidebar to set additional filters:
- Price range
- Minimum rating
- Room type preferences

### Analytics

Explore search result analytics including:
- Price distribution
- Rating distribution
- Room type breakdown
- Summary statistics

## 🛠️ Customization

### Adding New Fields

To add a new field to the search schema:

1. Add the field to `DataSchema` in `index.py`
2. Create a new similarity space if needed
3. Add the field to the index spaces list
4. Update the query parameters in `query.py`

### Modifying the UI

The Streamlit interface can be customized by editing:
- `tools/st_app.py` (enhanced UI)
- `tools/streamlit_app.py` (basic UI)


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements
This project was **inspired by** the amazing work from **[DECODING ML](https://github.com/decodingml/tabular-semantic-search-tutorial)** on **tabular semantic search**. Their tutorial provided valuable insights into leveraging vector databases and multi-attribute indexing for structured data retrieval.  
