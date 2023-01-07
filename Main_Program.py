
# Libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from Function_file import convert, convert3, stem, fetch_director
from sklearn.metrics.pairwise import cosine_similarity


# Loading data
credits = pd.read_csv("tmdb_5000_credits.csv")
movies = pd.read_csv("tmdb_5000_movies.csv")

# Merging data
movies = movies.merge(credits, on='title')

# Feature extraction
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace = True)

# Preprocessing
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ", "") for i in x])


# Making a tagline
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df =  movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df['tags'].apply(stem)

# Object of vectorizer
cv = CountVectorizer(max_features=5000, stop_words = 'english')

# Vectorizing the tagline for finding the similarity
vectors = cv.fit_transform(new_df['tags']).toarray()

# Cosine similarity is used to find the similar movies
similarity = cosine_similarity(vectors)
sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x:x[1])


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse= True, key=lambda x:x[1])[:30]
    counter = 1
    for i in movie_list:
        print(str(counter) + ".", new_df.iloc[i[0]].title)
        counter += 1


# Taking Input Movie
Enter = input('Enter the Movie Name: ')
recommend(Enter)






