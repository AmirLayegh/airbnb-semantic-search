import superlinked.framework as sl
from loguru import logger

from superlinked_app import index, query
from superlinked_app import setting


airbnb_source: sl.RestSource = sl.RestSource(index.airbnb)

logger.info("Data loader will load data from: %s", setting.DATA_PATH)

airbnb_data_loader_parser: sl.DataFrameParser = sl.DataFrameParser(
    schema=index.airbnb,
    mapping={index.airbnb.id: "id"}
    )

airbnb_data_loader_config: sl.DataLoaderConfig = sl.DataLoaderConfig(
    str(setting.DATA_PATH),
    sl.DataFormat.CSV,
    pandas_read_kwargs={"chunksize": 100},
)

airbnb_loader_source: sl.DataLoaderSource = sl.DataLoaderSource(
    index.airbnb,
    data_loader_config=airbnb_data_loader_config,
    parser=airbnb_data_loader_parser,
)

if setting.USE_QDRANT_VECTOR_DB:
    logger.info("Using Qdrant vector database")
    vector_database = sl.QdrantVectorDatabase(
        setting.QDRANT_CLUSTER_URL.get_secret_value(),
        setting.QDRANT_API_KEY.get_secret_value(),
        collection_name='airbnb_semantic_search',
    )
    
else:
    logger.info("Using in-memory database")
    vector_database = sl.InMemoryVectorDatabase()
    

executor = sl.RestExecutor(
    sources=[airbnb_source, airbnb_loader_source],
    indices=[index.airbnb_index],
    queries=[
        sl.RestQuery(sl.RestDescriptor("filter_query"), query.filter_query),
        sl.RestQuery(sl.RestDescriptor("base_query"), query.base_query),
        sl.RestQuery(sl.RestDescriptor("semantic_search_query"), query.semantic_query),
    ],
    vector_database=vector_database,
)

sl.SuperlinkedRegistry.register(executor)