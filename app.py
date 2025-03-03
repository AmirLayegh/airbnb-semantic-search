from datetime import datetime, timedelta
import os

import altair as alt
import pandas as pd
from torch import float16
from transformers import AutoTokenizer, pipeline
from superlinked import framework as sl

alt.renderers.enable(sl.get_altair_renderer())
alt.data_transformers.disable_max_rows()
pd.set_option("display.max_colwidth", 1000)
START_OF_2024_TS = int(datetime(2024, 1, 2).timestamp())
EXECUTOR_DATA = {sl.CONTEXT_COMMON: {sl.CONTEXT_COMMON_NOW: START_OF_2024_TS}}
TOP_N = 8


from superlinked import framework as sl
from superlinked_app import constants, index


from datetime import datetime, timedelta

class DataSchema(sl.Schema):
    id: sl.IdField
    date: sl.Timestamp
    name: sl.String
    description: sl.String
    # review_scores_communication: sl.Float
    # review_scores_location: sl.Float
    # review_scores_cleanliness: sl.Float
    bedrooms: sl.Float
    beds: sl.Float
    bathrooms: sl.Float
    bathrooms_text: sl.String
    #room_text: sl.String
    review_scores_rating: sl.Float
    host_is_superhost: sl.Integer
    price: sl.Float
    amenities: sl.String
    number_of_reviews: sl.Integer
    room_type: sl.String
    listing_url: sl.String
    
airbnb = DataSchema()

description_space = sl.TextSimilaritySpace(
    text=airbnb.description, model="Alibaba-NLP/gte-large-en-v1.5"
)
review_rating_maximizer_space = sl.NumberSpace(
    number=airbnb.review_scores_rating, min_value=-1.0, max_value=5.0, mode=sl.Mode.MAXIMUM
)
price_minimizer_space = sl.NumberSpace(
    number=airbnb.price, min_value=-1.0, max_value=500000.0, mode=sl.Mode.MINIMUM
)
recency_space = sl.RecencySpace(
    timestamp=airbnb.date,
    period_time_list=[sl.PeriodTime(period=timedelta(days=365))]
)
amenities_space = sl.TextSimilaritySpace(
    text=airbnb.amenities, model="Alibaba-NLP/gte-large-en-v1.5"
)

airbnb_index = sl.Index(
    spaces=[
        description_space,
        review_rating_maximizer_space,
        price_minimizer_space,
        recency_space,
        amenities_space,
    ],
    fields=[airbnb.description, airbnb.review_scores_rating, airbnb.price, airbnb.date, airbnb.amenities],
)

airbnb_parser = 