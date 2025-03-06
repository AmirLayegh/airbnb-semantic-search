import requests
import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import numpy as np

# Configure page
st.set_page_config(
    page_title="Airbnb Semantic Search",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF5A5F;  /* Airbnb color */
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #484848;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #1e1e24;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #FF5A5F;
        color: #ffffff;
    }
    .feature-icon {
        font-size: 1.2rem;
        margin-right: 8px;
    }
    .rating-high {
        color: #2ecc71;
        font-weight: bold;
    }
    .rating-medium {
        color: #f39c12;
        font-weight: bold;
    }
    .rating-low {
        color: #e74c3c;
        font-weight: bold;
    }
    .price-tag {
        background-color: #FF5A5F;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .card h3 {
        color: #ffffff;
    }
    
    .card p {
        color: #e0e0e0;
    }
    .search-history-item {
        cursor: pointer;
        padding: 5px;
        border-radius: 5px;
    }
    .search-history-item:hover {
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Constants
API_URL = "http://0.0.0.0:8080/api/v1/search/filter_query"
DEFAULT_TIMEOUT = 10  # seconds

# Session state initialization
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'favorite_listings' not in st.session_state:
    st.session_state.favorite_listings = set()
if 'last_query' not in st.session_state:
    st.session_state.last_query = ""
if 'last_results' not in st.session_state:
    st.session_state.last_results = None

def make_filter_query(query: str, limit: int = 10, timeout: int = DEFAULT_TIMEOUT) -> dict | None:
    """Make a request to the semantic search API with error handling and timeout"""
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"natural_query": query}
    
    try:
        with st.spinner("🔍 Searching..."):
            response = requests.post(
                API_URL, 
                headers=headers, 
                json=data,
                timeout=timeout
            )
        
        # Handle different status codes
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error("API endpoint not found. Please check if the service is running.")
        elif response.status_code == 400:
            st.error(f"Bad request: {response.json().get('detail', 'No details provided')}")
        elif response.status_code == 500:
            st.error("Server error. The search service might be experiencing issues.")
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            
        return None
    except requests.exceptions.Timeout:
        st.error(f"Request timed out after {timeout} seconds. The server might be overloaded.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check if the API server is running.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("Failed to parse API response. The server returned an invalid JSON.")
        return None

def display_listing(listing, idx):
    """Display a single listing with enhanced UI"""
    # Extract listing details with default values
    name = listing.get('name', 'Unnamed Listing')
    description = listing.get('description', 'No description available')
    price = listing.get('price', 'N/A')
    rating = listing.get('review_scores_rating', 'N/A')
    room_type = listing.get('room_type', 'N/A')
    accommodates = listing.get('accommodates', 'N/A')
    bathrooms = listing.get('bathrooms', 'N/A')
    bedrooms = listing.get('bedrooms', 'N/A')
    amenities = listing.get('amenities', [])
    
    # Try to parse amenities if it's a string
    if isinstance(amenities, str):
        try:
            amenities = json.loads(amenities)
        except json.JSONDecodeError:
            amenities = amenities.split(',')
    
    # Format amenities for display
    if isinstance(amenities, list) and len(amenities) > 0:
        amenities_display = ", ".join(amenities[:5])
        if len(amenities) > 5:
            amenities_display += f" + {len(amenities) - 5} more"
    else:
        amenities_display = "No amenities listed"
    
    # Determine rating class
    rating_class = "rating-medium"
    if rating != 'N/A':
        try:
            rating_float = float(rating)
            if rating_float >= 4.5:
                rating_class = "rating-high"
            elif rating_float < 4.0:
                rating_class = "rating-low"
        except (ValueError, TypeError):
            pass
    
    # Create listing card
    with st.container():
        st.markdown(f"""
        <div class="card">
            <h3>{name}</h3>
            <p><span class="feature-icon">📝</span> {description[:150]}{'...' if len(description) > 150 else ''}</p>
            <p><span class="feature-icon">💰</span> <span class="price-tag">${price}</span> per night</p>
            <p><span class="feature-icon">⭐</span> Rating: <span class="{rating_class}">{rating}</span></p>
            <p><span class="feature-icon">🏠</span> {room_type} · Accommodates: {accommodates} · Bedrooms: {bedrooms} · Bathrooms: {bathrooms}</p>
            <p><span class="feature-icon">🧰</span> {amenities_display}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 10])
        with col1:
            listing_id = listing.get('id', f"temp_id_{idx}")
            is_favorite = listing_id in st.session_state.favorite_listings
            if st.button("❤️" if is_favorite else "🤍", key=f"fav_{listing_id}"):
                if is_favorite:
                    st.session_state.favorite_listings.remove(listing_id)
                else:
                    st.session_state.favorite_listings.add(listing_id)
                st.rerun()
        with col2:
            if st.button("View Details", key=f"details_{idx}"):
                st.session_state.selected_listing = listing
                st.rerun()

def format_date(date_str):
    """Format date string to a more readable format"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except:
        return date_str

def add_to_search_history(query, results_count):
    """Add query to search history with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    history_item = {
        "query": query,
        "timestamp": timestamp,
        "results_count": results_count
    }
    # Avoid duplicates by removing previous occurrences of the same query
    st.session_state.search_history = [h for h in st.session_state.search_history if h["query"] != query]
    # Add new query to the beginning of the list
    st.session_state.search_history.insert(0, history_item)
    # Keep only the 10 most recent searches
    st.session_state.search_history = st.session_state.search_history[:10]

def create_listing_dataframe(results):
    """Create a dataframe from listing results for analysis"""
    listings = []
    for item in results:
        if "obj" in item:
            listings.append(item["obj"])
    
    if not listings:
        return None
        
    df = pd.DataFrame(listings)
    
    # Convert relevant columns to numeric
    numeric_columns = ['price', 'review_scores_rating', 'accommodates', 'bedrooms', 'bathrooms']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def display_analytics(df):
    """Display analytics about the search results using native Streamlit charts"""
    if df is None or df.empty:
        return
        
    st.subheader("📊 Search Results Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution using native Streamlit histogram
        if 'price' in df.columns:
            st.subheader("Price Distribution")
            price_data = df['price'].dropna()
            if not price_data.empty:
                # Create properly formatted price bins
                min_price = int(price_data.min())
                max_price = int(price_data.max() + 1)
                bin_size = (max_price - min_price) // 10
                
                # Create a list to hold bin data
                bins = []
                labels = []
                
                # Create bins with proper labels
                for i in range(min_price, max_price, bin_size):
                    bins.append((i, i + bin_size))
                    labels.append(f"${i}-${i + bin_size}")
                
                # Assign each price to a bin
                binned_data = pd.cut(price_data, bins=10)
                
                # Count values in each bin and create a clean DataFrame for charting
                price_counts = binned_data.value_counts().sort_index()
                price_chart_data = pd.DataFrame({
                    'Price Range': [f"${int(b.left)}-${int(b.right)}" for b in price_counts.index],
                    'Count': price_counts.values
                })
                
                # Create chart with clean labels
                st.bar_chart(price_chart_data.set_index('Price Range'))
                
                st.write(f"Average price: ${price_data.mean():.2f}")
                st.write(f"Price range: ${price_data.min():.2f} - ${price_data.max():.2f}")
    
    with col2:
        # Rating distribution using native Streamlit histogram
        if 'review_scores_rating' in df.columns:
            st.subheader("Rating Distribution")
            rating_data = df['review_scores_rating'].dropna()
            if not rating_data.empty:
                # Create properly formatted rating bins
                min_rating = max(3.0, float(rating_data.min()))  # Start at 3.0 or the min value
                max_rating = min(5.0, float(rating_data.max()))  # Cap at 5.0
                step = 0.25  # 0.25 increments for ratings
                
                # Create bins with clean labels
                rating_bins = [round(r, 2) for r in np.arange(min_rating, max_rating + step, step)]
                
                # Bin the data
                binned_ratings = pd.cut(rating_data, bins=rating_bins)
                
                # Count values in each bin and create a clean DataFrame for charting
                rating_counts = binned_ratings.value_counts().sort_index()
                rating_chart_data = pd.DataFrame({
                    'Rating': [f"{float(b.left):.1f}-{float(b.right):.1f}" for b in rating_counts.index],
                    'Count': rating_counts.values
                })
                
                # Create chart with clean labels
                st.bar_chart(rating_chart_data.set_index('Rating'))
                
                st.write(f"Average rating: {rating_data.mean():.2f}/5")
    
    # Room type breakdown using a simple table and bar chart
    if 'room_type' in df.columns:
        st.subheader("Room Type Distribution")
        room_counts = df['room_type'].value_counts()
        
        # Display as a table
        room_df = pd.DataFrame({
            'Room Type': room_counts.index,
            'Count': room_counts.values,
            'Percentage': (room_counts.values / room_counts.sum() * 100).round(1)
        })
        st.table(room_df)
        
        # Display as a bar chart
        st.bar_chart(room_counts)
    
    # Summary statistics
    st.subheader("Summary Statistics")
    
    # Create two columns for better layout
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        # Price statistics
        if 'price' in df.columns:
            st.write("**Price Statistics:**")
            st.write(f"- Median: ${df['price'].median():.2f}")
            st.write(f"- 25th percentile: ${df['price'].quantile(0.25):.2f}")
            st.write(f"- 75th percentile: ${df['price'].quantile(0.75):.2f}")
    
    with stat_col2:
        # Other interesting counts
        st.write("**Property Details:**")
        if 'accommodates' in df.columns:
            st.write(f"- Avg. accommodates: {df['accommodates'].mean():.1f} guests")
        if 'bedrooms' in df.columns:
            st.write(f"- Avg. bedrooms: {df['bedrooms'].mean():.1f}")
        if 'bathrooms' in df.columns:
            st.write(f"- Avg. bathrooms: {df['bathrooms'].mean():.1f}")

def display_search_tips():
    """Display helpful search tips to the user"""
    with st.expander("🔍 Search Tips"):
        st.markdown("""
        ### Effective Search Queries
        
        Try these search patterns:
        
        **Location-based:**
        - "Apartments in downtown with a view"
        - "Beachfront properties with a pool"
        
        **Price-based:**
        - "Affordable homes under $100 per night"
        - "Luxury accommodations with hot tub"
        
        **Rating-based:**
        - "Top-rated places with rating above 4.8"
        - "Best reviewed apartments with 2 bedrooms"
        
        **Amenities-focused:**
        - "Places with wifi and free parking"
        - "Family-friendly homes with kitchen and washer"
        
        **Combined criteria:**
        - "Quiet apartments with rating above 4.5 and price under $150"
        - "Pet-friendly houses with at least 2 bedrooms and good reviews"
        """)

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔎 Search Settings")
        
        # API endpoint configuration (for advanced users)
        with st.expander("⚙️ API Configuration"):
            api_url = st.text_input("API URL", value=API_URL)
            timeout = st.slider("Request Timeout (seconds)", 1, 30, DEFAULT_TIMEOUT)
        
        # Search filters
        st.markdown("### 🔍 Advanced Filters")
        min_price = st.number_input("Minimum Price ($)", 0, 1000, 0, 10)
        max_price = st.number_input("Maximum Price ($)", 0, 10000, 1000, 50)
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
        
        room_types = st.multiselect(
            "Room Types",
            ["Entire home/apt", "Private room", "Shared room", "Hotel room"],
            []
        )
        
        st.markdown("### 🕒 Search History")
        if st.session_state.search_history:
            for idx, item in enumerate(st.session_state.search_history):
                if st.button(
                    f"{item['query']} ({item['results_count']} results) - {item['timestamp']}", 
                    key=f"history_{idx}",
                    use_container_width=True,
                    type="secondary"
                ):
                    # Reuse the query from history
                    st.session_state.last_query = item['query']
                    st.rerun()
        else:
            st.write("No search history yet.")
            
        st.markdown("### ❤️ Favorites")
        if st.session_state.favorite_listings:
            st.write(f"{len(st.session_state.favorite_listings)} saved listings")
            if st.button("View Favorites"):
                st.session_state.show_favorites = True
                st.rerun()
        else:
            st.write("No favorites saved yet.")
            
        # Display tips for users
        display_search_tips()
        
    # Main content
    st.markdown('<h1 class="main-header">🏠 Airbnb Semantic Search</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Find your perfect stay with natural language search</p>', unsafe_allow_html=True)
    
    # Create three columns for the search interface
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        query = st.text_input(
            "What are you looking for?",
            placeholder="e.g., cozy apartments with a view under $150 with rating above 4.5",
            value=st.session_state.last_query
        )
    
    with col2:
        limit = st.number_input("Results limit", min_value=5, max_value=100, value=20, step=5)
    
    with col3:
        search_button = st.button("🔍 Search", use_container_width=True, type="primary")
    
    # Execute search
    if search_button and query:
        st.session_state.last_query = query
        
        # Prepare search query with filters
        enhanced_query = query
        filter_additions = []
        
        if min_price > 0:
            filter_additions.append(f"price greater than {min_price}")
        if max_price < 1000:
            filter_additions.append(f"price less than {max_price}")
        if min_rating > 0:
            filter_additions.append(f"rating above {min_rating}")
        if room_types:
            room_type_str = " or ".join(room_types)
            filter_additions.append(f"room type is {room_type_str}")
            
        if filter_additions:
            filter_str = " and ".join(filter_additions)
            enhanced_query = f"{query} with {filter_str}"
            
        # Make the search request
        response = make_filter_query(enhanced_query, limit=limit, timeout=timeout)
        
        if response and "results" in response:
            results = response["results"]
            st.session_state.last_results = results
            result_count = len(results)
            
            # Add to search history
            add_to_search_history(query, result_count)
            
            # Display results summary
            st.markdown(f"### 🔍 Found {result_count} listings matching your search")
            
            # Create dataframe for analytics
            results_df = create_listing_dataframe(results)
            
            # Display analytics
            if results_df is not None:
                display_analytics(results_df)
            
            # Display results
            st.markdown("### 📋 Search Results")
            
            # Create sorting options
            sort_col1, sort_col2 = st.columns([1, 3])
            with sort_col1:
                st.write("Sort by:")
            with sort_col2:
                sort_option = st.selectbox(
                    "",
                    ["Relevance", "Price (low to high)", "Price (high to low)", "Rating (high to low)"],
                    label_visibility="collapsed"
                )
            
            # Sort results based on selection
            if sort_option == "Price (low to high)" and results_df is not None:
                sorted_indices = results_df['price'].sort_values().index
                sorted_results = [results[i] for i in sorted_indices if i < len(results)]
            elif sort_option == "Price (high to low)" and results_df is not None:
                sorted_indices = results_df['price'].sort_values(ascending=False).index
                sorted_results = [results[i] for i in sorted_indices if i < len(results)]
            elif sort_option == "Rating (high to low)" and results_df is not None:
                sorted_indices = results_df['review_scores_rating'].sort_values(ascending=False).index
                sorted_results = [results[i] for i in sorted_indices if i < len(results)]
            else:
                sorted_results = results
            
            # Display listings
            for idx, item in enumerate(sorted_results):
                if "obj" in item:
                    display_listing(item["obj"], idx)
            
            # Offer export options
            if results_df is not None:
                st.markdown("### 📤 Export Results")
                col1, col2 = st.columns(2)
                with col1:
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        "airbnb_search_results.csv",
                        "text/csv",
                        key='download-csv'
                    )
                with col2:
                    json_str = results_df.to_json(orient="records")
                    st.download_button(
                        "Download JSON",
                        json_str,
                        "airbnb_search_results.json",
                        "application/json",
                        key='download-json'
                    )
        else:
            st.error("No results found. Try adjusting your search query or filters.")
            
    # Display detailed view of a selected listing
    if 'selected_listing' in st.session_state:
        listing = st.session_state.selected_listing
        
        st.markdown("---")
        st.markdown(f"## {listing.get('name', 'Listing Details')}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Description**: {listing.get('description', 'No description available')}")
            
            amenities = listing.get('amenities', [])
            if isinstance(amenities, str):
                try:
                    amenities = json.loads(amenities)
                except:
                    amenities = amenities.split(',')
                    
            if amenities:
                st.markdown("### Amenities")
                amenities_cols = st.columns(3)
                for i, amenity in enumerate(amenities):
                    col_idx = i % 3
                    amenities_cols[col_idx].markdown(f"- {amenity.strip()}")
            
            st.markdown("### Location Info")
            st.markdown(f"- Neighborhood: {listing.get('neighborhood', 'N/A')}")
            st.markdown(f"- Transit: {listing.get('transit', 'N/A')}")
            
        with col2:
            st.markdown("### Details")
            st.markdown(f"**Price**: ${listing.get('price', 'N/A')} per night")
            st.markdown(f"**Rating**: {listing.get('review_scores_rating', 'N/A')}/5")
            st.markdown(f"**Room Type**: {listing.get('room_type', 'N/A')}")
            st.markdown(f"**Accommodates**: {listing.get('accommodates', 'N/A')} guests")
            st.markdown(f"**Bedrooms**: {listing.get('bedrooms', 'N/A')}")
            st.markdown(f"**Bathrooms**: {listing.get('bathrooms', 'N/A')}")
            
            if 'host_name' in listing:
                st.markdown(f"**Host**: {listing.get('host_name', 'N/A')}")
                st.markdown(f"**Host Response Rate**: {listing.get('host_response_rate', 'N/A')}")
            
            # Availability info if present
            if any(k in listing for k in ['availability_30', 'availability_60', 'availability_90']):
                st.markdown("### Availability")
                if 'availability_30' in listing:
                    st.markdown(f"Next 30 days: {listing['availability_30']} days")
                if 'availability_60' in listing:
                    st.markdown(f"Next 60 days: {listing['availability_60']} days")
                if 'availability_90' in listing:
                    st.markdown(f"Next 90 days: {listing['availability_90']} days")
        
        if st.button("← Back to results"):
            del st.session_state.selected_listing
            st.rerun()
    
    # Show favorites if requested
    if st.session_state.get('show_favorites', False):
        st.markdown("## ❤️ Your Favorite Listings")
        
        if st.session_state.last_results:
            favorite_listings = []
            for item in st.session_state.last_results:
                if "obj" in item and item["obj"].get('id') in st.session_state.favorite_listings:
                    favorite_listings.append(item)
            
            if favorite_listings:
                for idx, item in enumerate(favorite_listings):
                    display_listing(item["obj"], f"fav_{idx}")
            else:
                st.write("No favorites from your last search.")
                
        if st.button("← Back to search results"):
            st.session_state.show_favorites = False
            st.rerun()

if __name__ == "__main__":
    main()
