import requests
import streamlit as st

# here is the API request: curl -X 'POST' \
#   'http://0.0.0.0:8080/api/v1/search/filter_query' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{"natural_query": "Find apartments with rating bigger than 4."}'
def make_filter_query(query:str) -> dict | None:
    url = "http://0.0.0.0:8080/api/v1/search/filter_query"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"natural_query": query}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        
        return None
    
def main():
    st.title("🔍 Search Airbnb listings")
    st.markdown("### 📊 Using Semantic Tabular Search")
    st.markdown("#### ⚡🧩 Powered by Superlinked and Qdrant vector database")
    
    st.markdown("> Find Homes based on their description, price, review rating, and amenities.")
    st.markdown("> All in a single search! 🪄✨")
    
    query = st.text_input("Enter your search query:",
                          placeholder="e.g., apartments with rating bigger than 4."
                          )
    limit = st.number_input("Number of results to show:", min_value=1, max_value=100, value=10)
    
    if st.button("Search"):
        if query:
            with st.spinner("Searching..."):
                response = make_filter_query(query)
                
                if response and "results" in response:
                    st.subheader("Search Results")
                    for item in response["results"]:
                        with st.container():
                            apartment = item["obj"]
                            st.markdown(f"### {apartment['name']}\n"
                                        f"#### 📝 Description: {apartment['description']}\n"
                                        f"#### 💰 Price: {apartment['price']}\n"
                                        f"#### ⭐ Rating: {apartment['review_scores_rating']}\n"
                                        f"#### 🛏️ Room Type: {apartment['room_type']}")
                            
                    st.write(response)
                else:
                    st.error("Failed to fetch results.")
                    
if __name__ == "__main__":
    main()
    
    
    
    
    