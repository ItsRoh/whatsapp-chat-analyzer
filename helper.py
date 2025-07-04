from urlextract import URLExtract
extract=URLExtract()

import matplotlib.pyplot as plt

from wordcloud import wordcloud, WordCloud

import pandas as pd
from collections import Counter

import emoji

def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        # 1. fetch number of messages
        num_messages=df.shape[0]
        # 2. fetch number of words
        words=[]
        for message in df['message']:
            words.extend(message.split())

        # 3. fetch number of media messages
        num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0]

        # 4. fetch number of links shared
        links = []
        for msg in df['message']:
            links.extend(extract.find_urls(msg))

        return num_messages,len(words),num_media_msg,len(links)
    else:
        new_df=df[df['user']==selected_user]
        num_messages=new_df.shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        # 3. fetch number of media messages
        num_media_msg = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        # 4. fetch number of links shared
        links = []
        for msg in new_df['message']:
            links.extend(extract.find_urls(msg))
        return num_messages, len(words), num_media_msg, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent_msgs'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stopwords_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_Common_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f=open('stopwords_hinglish.txt','r')
    stop_words=f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
