
import pandas as pd
import numpy as np
import streamlit as st
import pickle
import requests
from streamlit_option_menu import option_menu
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"


selected = option_menu(
    menu_title=f'Recommender System',
    menu_icon='film',

    options=['Home', 'Movie','Music','Book', 'Conclusion'],
    icons=['house','book','emoji-smile'],
    orientation="horizontal",
)

if selected == "Home":
    st.header(f'DY PATIL UNIVERSITY')
    st.subheader('School of Engineering and Technology')
    st.subheader('Project:- Content based Movie Recommender System')
    st.subheader('Group Members :')
    st.text(f'1. MOHAMMAD HASSAAN \n2. MOHAMMED USMAN KHALIL MOMIN \n3. AMAN SULTAN')


if selected == "Movie":

    def fetch_poster(movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=371729760f195c70054791d7104624b8&language=en-US'.format(movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters =[]
        for i in (movies_list):
             movie_id = movies.iloc[i[0]].movie_id

             recommended_movies.append(movies.iloc[i[0]].title)
             # fetch poster form API
             recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies,recommended_movies_posters

    movies_dict= pickle.load(open('movie_dict.pkl','rb'))
    movies=pd.DataFrame(movies_dict)

    similarity = pickle.load(open('similarity.pkl','rb'))

    st.title('Movie recommender System')
    selected_movie_name = st.selectbox(
    'How would yo like to be connected?',
    movies['title'].values)

    if st.button('Recommend'):

        recommended_movies, recommended_movies_posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movies[0])
            st.image(recommended_movies_posters[0])
        with col2:
            st.text(recommended_movies[1])
            st.image(recommended_movies_posters[1])
        with col3:
            st.text(recommended_movies[2])
            st.image(recommended_movies_posters[2])
        with col4:
            st.text(recommended_movies[3])
            st.image(recommended_movies_posters[3])
        with col5:
            st.text(recommended_movies[4])
            st.image(recommended_movies_posters[4])

if selected == "Music":
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    def get_song_album_cover_url(song_name, artist_name):
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track")

        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            album_cover_url = track["album"]["images"][0]["url"]
            print(album_cover_url)
            return album_cover_url
        else:
            return "https://i.postimg.cc/0QNxYz4V/social.png"


    def recommend(song):
        index = music[music['song'] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_music_names = []
        recommended_music_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            artist = music.iloc[i[0]].artist
            print(artist)
            print(music.iloc[i[0]].song)
            recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
            recommended_music_names.append(music.iloc[i[0]].song)

        return recommended_music_names, recommended_music_posters


    st.header('Music Recommender System')
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    music_list = music['song'].values
    selected_movie = st.selectbox(
        "Type or select a song from the dropdown",
        music_list
    )

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_music_names[0])
            st.image(recommended_music_posters[0])
        with col2:
            st.text(recommended_music_names[1])
            st.image(recommended_music_posters[1])

        with col3:
            st.text(recommended_music_names[2])
            st.image(recommended_music_posters[2])
        with col4:
            st.text(recommended_music_names[3])
            st.image(recommended_music_posters[3])
        with col5:
            st.text(recommended_music_names[4])
            st.image(recommended_music_posters[4])

if selected == "Book":
    st.header("Book Recommender")
    model = pickle.load(open("model3.pkl", 'rb'))
    books_name = pickle.load(open("book_names.pkl", 'rb'))
    final_rating = pickle.load(open("b_final_rating.pkl", 'rb'))
    book_pivot = pickle.load(open("book_pivot.pkl", 'rb'))


    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
        poster_url = []

        for book_id in suggestion:
            book_name.append(book_pivot.index[book_id])
        for name in book_name[0]:
            ids = np.where(final_rating['title'] == name)[0][0]
            ids_index.append(ids)

        for idx in ids_index:
            url = final_rating.iloc[idx]['image_url']
            poster_url.append(url)
        return poster_url

    def recommend_books(book_name):
        book_list = []
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
        poster_url = fetch_poster(suggestion)

        for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                book_list.append(j)

        return book_list, poster_url


    selected_books = st.selectbox("Type or select a book", books_name)
    if st.button("show recommendation"):
        recommendation_books, poster_url = recommend_books(selected_books)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommendation_books[1])
            st.image(poster_url[1])
        with col2:
            st.text(recommendation_books[2])
            st.image(poster_url[2])

        with col3:
            st.text(recommendation_books[3])
            st.image(poster_url[3])
        with col4:
            st.text(recommendation_books[4])
            st.image(poster_url[4])
        with col5:
            st.text(recommendation_books[5])
            st.image(poster_url[5])

if selected == "Conclusion":
    st.subheader('Information retrieval has become very difficult nowadays because of the overloading of data and this issue has restricted'
            ' the user from accessing the item that best match their preference. The content based recommendation approach does not consider'
            ' other user profile while making recommendation. This will help the user to get personalised suggest for their input. ')
    st.title(f'THANK YOU')


