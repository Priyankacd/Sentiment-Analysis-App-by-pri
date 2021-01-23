  
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import emoji
from textblob import TextBlob

#!pip install wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment Analysis of Tweets ")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines ")



DATA_URL = ("Tweets.csv")
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()
#st.write(data)



st.subheader(emoji.emojize(' :red_heart::red_heart::red_heart: Sentiment analysis with emoji :red_heart::red_heart::red_heart: ',use_aliases=True))
raw_text = st.text_area("Enter Your Text","Type Here")
if st.button("Analyze"):
	blob = TextBlob(raw_text)
	result = blob.sentiment.polarity
	if result > 0.0:
		custom_emoji = ':smile::smile::smile::smile::smile:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	elif result < 0.0:
		custom_emoji = ':disappointed::disappointed::disappointed::disappointed::disappointed:'
		st.write(emoji.emojize(custom_emoji,use_aliases=True))
	else:
		st.write(emoji.emojize(':expressionless::expressionless::expressionless::expressionless::expressionless:',use_aliases=True))
	st.info("Polarity Score is:: {}".format(result))    
    
st.sidebar.subheader("Show a random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Plot Type', ['Histogram', 'Pie Chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
#st.write(sentiment_count)
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})



st.markdown("### Number of tweets by sentiment")
if select == "Histogram":
    fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)       
else:
    fig = px.pie(sentiment_count,values="Tweets", names='Sentiment')
st.plotly_chart(fig)



#st.map(data)
st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
#hour = st.sidebar.number_input("Hour of day", min_value=1, max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("### Tweet locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

    

st.sidebar.subheader("Breakdown airline by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'))
if len(choice) > 0:
    choice_data =data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc= 'count',color='airline_sentiment',facet_col='airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)


st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

st.subheader('Word cloud for %s sentiment' % (word_sentiment))
df = data[data['airline_sentiment']==word_sentiment]
words = ' '.join(df['text'])
processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
st.pyplot()









st.subheader("******************************** By - Priyanka Dhole ********************************")
