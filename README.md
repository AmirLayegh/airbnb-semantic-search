# Airbnb Semantic Search

A cutting-edge **semantic search system** for Airbnb listings, leveraging **[Superlinked](https://www.superlinked.com/)** for multi-attribute vector indexing and **[Qdrant](https://qdrant.tech/)** for high-performance vector search. This system enables **natural language queries** to retrieve relevant listings by embedding different attributes (e.g., price, location, and descriptions) using specialized embedding models, ensuring highly accurate and context-aware search results.

![Airbnb Search Banner](/sources/airbnb-superlinked-dark.png)

## 🌟 Features

- **Semantic Search for Structured Data**: Enables natural language queries like "cozy apartments with a view under $150 with rating above 4.5" to retrieve relevant Airbnb listings based on multiple attributes.
- **Multi-Attribute Vector Indexing**: Each column in the Airbnb dataset is embedded using a specialized model (e.g., float-specific embeddings for price, text embeddings for descriptions).
- **Vector Database Integration**: Powered by Qdrant for efficient similarity searches.
- **RESTful API Endpoints**:  Built with FastAPI for efficient and scalable backend operations.
- **Interactive UI**: Uses [Streamlit](https://streamlit.io/) to provide an intuitive front-end interface for searching Airbnb listings.

## 🏗️ Project Structure

```
.
├── data/                                          # Directory where dataset files can be found
├── superlinked_app/                               # Main application source code
├── tools/                                         # Utility scripts and helper tools
├── .env.example                                   # Template for environment variables
├── app.py                                         # Python file for in memory development.
├── Makefile                                       # Running commands shortcuts
├── pyproject.toml                                 # Python project dependencies and metadata
└── uv.lock                                        # Lock file for uv package manager
```

## 🔧 Technologies

- **Superlinked Framework**: For semantic search capabilities
- **Qdrant**: Vector database for efficient similarity search
- **OpenAI API**: Natural language understanding
- **Streamlit**: Interactive web interface
- **uv**: Fast Python package installer and resolver

## 📥 Installation

### Prerequisites

- Python 3.11+
- Qdrant Cloud account (or local Qdrant instance)
- OpenAI API key

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/airbnb-semantic-search.git
cd airbnb-semantic-search
```

2. Install dependencies using uv:
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies from pyproject.toml
uv pip install -e .
```

3. Alternatively, use the Makefile:
```bash
# Setup environment, install dependencies, and verify installation
make setup
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
make create-db
```

2. Start the API server:
```bash
superlinked serve
```
   
   Or using the Makefile:
```bash
make serve
```

3. Launch the Streamlit application:
```bash
cd tools
streamlit run st_app.py
```
   
   Or using the Makefile:
```bash
make ui
```

4. Open your browser at `http://localhost:8501` to access the application.

## 🔍 Usage

### Basic Search

Enter natural language queries in the search bar like:
- "Apartments in downtown with a view"
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
├── .env                     # Environment variables (not tracked by git)
├── Makefile                 # Automation for common development tasks
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Project documentation
```

## 🧩 How It Works

1. **Data Indexing**:
   - The system parses Airbnb listings data according to the schema defined in `index.py`
   - Text fields (descriptions, amenities) are embedded using vector embeddings
   - Numerical fields (price, ratings) are stored for filtering

2. **Query Processing**:
   - Natural language queries are processed by OpenAI
   - The system extracts relevant search parameters (description text, price constraints, etc.)
   - A structured query is built combining vector similarity and filter conditions

3. **Result Retrieval**:
   - The vector database performs efficient similarity search
   - Results are filtered based on additional criteria
   - Listings are ranked by relevance and returned to the user

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

## 📈 Future Improvements

- [ ] Add support for geographical search (map-based interface)
- [ ] Implement user authentication and personalized recommendations
- [ ] Add multi-language support
- [ ] Create advanced analytics dashboards
- [ ] Add image-based similarity search

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Superlinked](https://www.superlinked.com/) for the semantic search framework
- [Qdrant](https://qdrant.tech/) for the vector database
- [OpenAI](https://openai.com/) for natural language processing capabilities
- [Streamlit](https://streamlit.io/) for the interactive web interface