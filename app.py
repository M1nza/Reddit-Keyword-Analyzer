import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

st.set_page_config(page_title="Twitter Keyword Engagement Analyzer", layout="wide")

st.title("Twitter Keyword Engagement Analyzer")
st.markdown("""
Enter a niche keyword (e.g., beauty, fashion) to fetch recent tweets and analyze top keywords driving engagement (likes + retweets + replies).
""")

@st.cache_data(show_spinner=True)
def fetch_tweets(keyword, limit=100):
    query = f"{keyword} lang:en"
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets_list.append({
            'content': tweet.content,
            'likes': tweet.likeCount,
            'retweets': tweet.retweetCount,
            'replies': tweet.replyCount,
            'engagement': tweet.likeCount + tweet.retweetCount + tweet.replyCount
        })
    return pd.DataFrame(tweets_list)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"@\w+", "", text)     # remove mentions
    text = re.sub(r"[^a-z\s]", "", text) # keep only letters and spaces
    return text

def extract_keywords(tweets_df):
    all_words = []
    for text in tweets_df['content']:
        clean = clean_text(text)
        words = clean.split()
        all_words.extend(words)
    # Filter out common English stopwords
    stopwords = set([
        'the', 'and', 'to', 'a', 'of', 'in', 'for', 'is', 'on', 'that', 'with', 'as',
        'at', 'this', 'it', 'be', 'by', 'are', 'was', 'from', 'or', 'an', 'have', 'has',
        'but', 'not', 'you', 'i', 'my', 'me', 'we', 'our', 'your', 'so', 'if', 'they',
        'all', 'just', 'about', 'like', 'get', 'up', 'out', 'what', 'can', 'now', 'more',
        'will', 'no', 'one', 'do', 'how', 'when', 'who', 'which', 'been', 'had', 'did',
        'were', 'their', 'them'
    ])
    filtered_words = [w for w in all_words if w not in stopwords and len(w) > 2]
    return filtered_words

def keyword_engagement(tweets_df, keywords):
    # For each keyword, sum engagement from tweets that contain it
    kw_engagement = {}
    for kw in set(keywords):
        mask = tweets_df['content'].str.lower().str.contains(kw)
        total_engagement = tweets_df.loc[mask, 'engagement'].sum()
        count = mask.sum()
        if count > 0:
            kw_engagement[kw] = {'engagement': total_engagement, 'count': count}
    # Convert to DataFrame
    df = pd.DataFrame.from_dict(kw_engagement, orient='index')
    df['avg_engagement'] = df['engagement'] / df['count']
    df = df.sort_values(by='avg_engagement', ascending=False)
    return df

def plot_bar(df):
    fig, ax = plt.subplots(figsize=(10,6))
    df.head(15)['avg_engagement'].plot(kind='bar', ax=ax, color='mediumvioletred')
    ax.set_ylabel('Average Engagement (Likes + Retweets + Replies)')
    ax.set_xlabel('Keyword')
    ax.set_title('Top Keywords by Average Engagement')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_wordcloud(keywords):
    text = ' '.join(keywords)
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='magma').generate(text)
    fig, ax = plt.subplots(figsize=(12,6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def main():
    keyword = st.text_input("Enter niche keyword (e.g., beauty, fashion)", value="beauty")
    tweet_limit = st.slider("Number of tweets to analyze", min_value=50, max_value=200, value=100, step=10)

    if st.button("Analyze"):
        with st.spinner("Fetching tweets and analyzing..."):
            tweets_df = fetch_tweets(keyword, limit=tweet_limit)
            if tweets_df.empty:
                st.warning("No tweets found for this keyword. Try another one!")
                return

            keywords = extract_keywords(tweets_df)
            eng_df = keyword_engagement(tweets_df, keywords)

            st.subheader(f"Top Keywords Driving Engagement for '{keyword}'")
            st.dataframe(eng_df[['avg_engagement', 'engagement', 'count']].head(20))

            st.subheader("Bar Chart of Top Keywords")
            st.pyplot(plot_bar(eng_df))

            st.subheader("Word Cloud of Keywords")
            st.pyplot(plot_wordcloud(keywords))

            st.subheader("Sample High Engagement Tweets")
            top_tweets = tweets_df.sort_values(by='engagement', ascending=False).head(5)
            for idx, row in top_tweets.iterrows():
                st.markdown(f"**Engagement:** {row['engagement']}  \n{row['content']}")

if __name__ == "__main__":
    main()
