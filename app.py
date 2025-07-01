import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Expanded sample static tweet data (25 tweets)
sample_tweets = [
    {"content": "Love the new summer fashion trends! #fashion #style", "likes": 120, "retweets": 30},
    {"content": "Beauty tips for glowing skin. #beauty #skincare", "likes": 200, "retweets": 50},
    {"content": "Latest makeup haul video is live! #makeup #beauty", "likes": 150, "retweets": 40},
    {"content": "Sustainable fashion is the future! #fashion #sustainability", "likes": 180, "retweets": 60},
    {"content": "Trying out the new organic face mask today! #beauty #skincare", "likes": 90, "retweets": 20},
    {"content": "Best shoes for summer outfits #fashion #shoes", "likes": 110, "retweets": 25},
    {"content": "Tips for long-lasting makeup #makeup #beauty", "likes": 140, "retweets": 35},
    {"content": "How to style oversized jackets #fashion #style", "likes": 160, "retweets": 45},
    {"content": "My favorite lipstick shades this season #makeup #beauty", "likes": 130, "retweets": 30},
    {"content": "DIY skincare routine for dry skin #beauty #skincare", "likes": 115, "retweets": 22},
    {"content": "The comeback of 90s fashion! #fashion #retro", "likes": 170, "retweets": 55},
    {"content": "Top 5 mascaras to try now #makeup #beauty", "likes": 125, "retweets": 28},
    {"content": "Eco-friendly fabrics to look for #fashion #sustainability", "likes": 105, "retweets": 18},
    {"content": "Easy hairstyles for every occasion #beauty #haircare", "likes": 145, "retweets": 33},
    {"content": "Summer dresses you need in your wardrobe #fashion #style", "likes": 155, "retweets": 40},
    {"content": "How to get flawless foundation coverage #makeup #beauty", "likes": 135, "retweets": 29},
    {"content": "Benefits of using natural oils on your skin #beauty #skincare", "likes": 120, "retweets": 26},
    {"content": "Casual outfits for weekend vibes #fashion #style", "likes": 140, "retweets": 32},
    {"content": "Step-by-step contouring guide #makeup #beauty", "likes": 160, "retweets": 50},
    {"content": "Must-have accessories this year #fashion #accessories", "likes": 110, "retweets": 21},
    {"content": "How to keep your skin hydrated all day #beauty #skincare", "likes": 130, "retweets": 27},
    {"content": "Mix and match your wardrobe basics #fashion #style", "likes": 150, "retweets": 38},
    {"content": "Best eyeshadow palettes for beginners #makeup #beauty", "likes": 140, "retweets": 35},
    {"content": "Why slow fashion matters #fashion #sustainability", "likes": 115, "retweets": 20},
    {"content": "Nighttime skincare routine essentials #beauty #skincare", "likes": 125, "retweets": 24},
]

df = pd.DataFrame(sample_tweets)

st.title("Twitter Keyword Engagement Analyzer — Demo")

st.write("Showing static sample tweets data for the Beauty & Fashion niche.")

st.dataframe(df)

# Combine all tweet content into one text
text = " ".join(df['content'])

# Generate a word cloud of keywords
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
