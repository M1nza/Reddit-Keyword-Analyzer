import streamlit as st
import requests
import pandas as pd

def fetch_reddit_posts(subreddit, size=100):
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={size}&sort=desc&sort_type=created_utc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        return []

st.title("Reddit Keyword & Engagement Analyzer")

subreddit = st.text_input("Enter a subreddit name (without r/)", value="beauty")

if st.button("Analyze"):
    st.write(f"Fetching and analyzing posts from r/{subreddit} ...")
    posts = fetch_reddit_posts(subreddit)
    if not posts:
        st.error("No posts found or error fetching data.")
    else:
        st.write(f"Fetched {len(posts)} posts.")
        df = pd.DataFrame(posts)
        df_display = df[['title', 'score', 'num_comments']].copy()
        df_display.rename(columns={'score':'Upvotes', 'num_comments':'Comments'}, inplace=True)
        st.dataframe(df_display)
