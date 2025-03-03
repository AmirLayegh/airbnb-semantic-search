from superlinked import framework as sl
from superlinked_app import constants
from datetime import timedelta, datetime

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

category_space = sl.CategoricalSpace(
    category=airbnb.room_type, categories=constants.TYPES
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
recency_space = sl.RecencySpace(
    timestamp=airbnb.date,
    period_time_list=[sl.PeriodTime(period=timedelta(days=365))]
)
amenities_space = sl.TextSimilaritySpace(
    text=airbnb.amenities, model="Alibaba-NLP/gte-large-en-v1.5"
)

airbnb_index = sl.Index(
    spaces=[
        category_space,
        description_space,
        review_rating_maximizer_space,
        price_minimizer_space,
        recency_space,
        amenities_space,
    ],
    fields=[airbnb.description, airbnb.review_scores_rating, airbnb.price, airbnb.date, airbnb.amenities],
)