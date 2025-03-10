from superlinked import framework as sl
from superlinked_app import constants
# from superlinked_app.constants import TYPES as typ
from datetime import timedelta, datetime

class DataSchema(sl.Schema):
    id: sl.IdField
    #date: sl.Timestamp
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

category_space = sl.CategoricalSimilaritySpace(
    category_input=airbnb.room_type, categories=['Private room', 'Entire home/apt', 'Shared room', 'Hotel room']
)

description_space = sl.TextSimilaritySpace(
    text=airbnb.description, model="Alibaba-NLP/gte-large-en-v1.5"
)
review_rating_maximizer_space = sl.NumberSpace(
    number=airbnb.review_scores_rating, min_value=-1.0, max_value=5.0, mode=sl.Mode.MAXIMUM
)
price_minimizer_space = sl.NumberSpace(
    number=airbnb.price, min_value=-1.0, max_value=500000.0, mode=sl.Mode.MINIMUM
)
# recency_space = sl.RecencySpace(
#     timestamp=airbnb.date,
#     period_time_list=[sl.PeriodTime(period=timedelta(days=365))]
# )
amenities_space = sl.TextSimilaritySpace(
    text=airbnb.amenities, model="Alibaba-NLP/gte-large-en-v1.5"
)

airbnb_index = sl.Index(
    spaces=[
        category_space,
        description_space,
        review_rating_maximizer_space,
        price_minimizer_space,
        # recency_space,
        amenities_space,
    ],
    fields=[airbnb.room_type, airbnb.description, airbnb.review_scores_rating, airbnb.price, airbnb.amenities],
)