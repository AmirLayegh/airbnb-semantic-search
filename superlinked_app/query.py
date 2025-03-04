from superlinked import framework as sl
from superlinked_app import index
from superlinked_app.config import setting


assert(
    setting.OPENAI_API_KEY
), "API_KEY must be set in the .env file. Please refer to the README for more information."

openai_config = sl.OpenAIClientConfig(
    api_key=setting.OPENAI_API_KEY.get_secret_value(),
    model=setting.OPENAI_MODEL_ID,
)

text_similar_param = sl.Param(
    "query_description",
    description=(
        "The text in the user's query that is used to search in the listings' descriptions."
        "Extract info that does not apply to other spaces or params."
    ),
    #options=constants.TYPES,
)
price_param = sl.Param(
    "query_price",
    description="The text in the user's query that is used to search in the listings' prices."
    "Extract info that does not apply to other spaces or params.",
)
review_rating_param = sl.Param(
    "query_review_rating",
    description="The text in the user's query that is used to search in the listings' review ratings."
    "Extract info that does not apply to other spaces or params.",
)
amenities_param = sl.Param(
    "query_amenities",
    description="The text in the user's query that is used to search in the listings' amenities."
    "Extract info that does not apply to other spaces or params.",
)

base_query = (
    sl.Query(
        index.airbnb_index,
        weights={
            index.description_space: sl.Param("description_weight"),
            index.review_rating_maximizer_space: sl.Param("review_rating_maximizer_weight"),
            index.price_minimizer_space: sl.Param("price_minimizer_weight"),
            index.amenities_space: sl.Param("amenities_weight")
        },
    )
    .find(index.airbnb)
    .with_natural_query(sl.Param("natural_query"), openai_config)
    .filter(
        index.airbnb.room_type == sl.Param("filter_by_type", options=['Private room', 'Entire home/apt', 'Shared room', 'Hotel room']),
    )
    #.select_all()
    .limit(5)
)

filter_query = (
    base_query.similar(
        index.description_space,
        text_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .similar(
        index.amenities_space,
        amenities_param,
        sl.Param("amenities_similar_clause_weight"),
    )
    .filter(
        index.airbnb.room_type == sl.Param("filter_by_type", options=['Private room', 'Entire home/apt', 'Shared room', 'Hotel room']),
    )
    .filter(
        index.airbnb.review_scores_rating >= sl.Param("review_rating_bigger_than",
                                                      description="Used to find listings with a review rating bigger than the provided number.",)
    )
    .filter(
        index.airbnb.price <= sl.Param("price_smaller_than",
                                       description="Used to find listings with a price smaller than the provided number.",)
    )
    #.select_all()
)

semantic_query = (
    base_query.similar(
        index.description_space,
        text_similar_param,
        sl.Param("description_similar_clause_weight"),
    )
    .similar(
        index.amenities_space,
        amenities_param,
        sl.Param("amenities_similar_clause_weight"),
    )
    # .filter(
    #     index.airbnb.room_type == sl.Param("filter_by_type", options=constants.TYPES),
    # )
    .filter(
        index.airbnb.review_scores_rating >= sl.Param("review_rating_bigger_than",
                                                      description="Used to find listings with a review rating bigger than the provided number.",)
    )
    .filter(
        index.airbnb.price <= sl.Param("price_smaller_than",
                                       description="Used to find listings with a price smaller than the provided number.",)
    )
    #.select_all()
)