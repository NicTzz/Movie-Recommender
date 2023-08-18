import psycopg2
from movie import *
import random

hostname = 'localhost'
database = 'Movies'
username = 'postgres'
pwd = '5432'
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

#Creating the table
cur = conn.cursor()
create_script = '''
CREATE TABLE IF NOT EXISTS movies(
name varchar(50) NOT NULL,
genre varchar(20) NOT NULL,
director varchar(50) NOT NULL,
imdb_rating real,
synopsis varchar(500)
);
'''
cur.execute(create_script)
conn.commit()
cur.close()
conn.close()

Movies = Movie_Graph()

def start():

    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )


    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    db = cur.fetchall()
    if not db:
        print("There are no movies in the database")
        print("That movie is not in the database, would you like to add it? Y/N")
        ans = str(input())
        if ans == "Y":
            add_movie()
        elif ans == "N":
            print("Ok!")
        else:
            print("That is not a valid answer.")
    conn.commit()
    cur.close()
    conn.close()

    #Setting up the movie graph from the data in the database
    for movie in db:
        print(movie[0])
        Movies.add_movie(movie[0], movie[1], movie[2], movie[3], movie[4])
        for item in dfs(Movies, 'Speed'):
            if Movies.graph_dict[item].genre == movie[1] or Movies.graph_dict[item].director == movie[2]:
                Movies.add_edge(Movies.graph_dict[item], Movies.graph_dict[movie[0]])

    user_movie = str(input("Enter movie name:"))
    if user_movie in dfs(Movies, 'Speed'):
        print(f"Movies similar to {user_movie}: ")
        rec = list(Movies.graph_dict[user_movie].recommendation.values())
        rec.remove(user_movie)
        for i in range(5):
            if rec:
                x = random.choice(rec)
                print(f"{i + 1}. " + x)
                print(f"Genre: {Movies.graph_dict[x].genre} \n Director: {Movies.graph_dict[x].director} \n Synopsis: {Movies.graph_dict[x].synopsis} \n IDMB: {Movies.graph_dict[x].rating}")
                rec.remove(x)
        
    else:
        print("That movie is not in the database, would you like to add it? Y/N")
        ans = str(input())
        if ans == "Y":
            add_movie()
        elif ans == "N":
            print("Ok!")
        else:
            print("That is not a valid answer.")
        
    




#depth-first-search
def dfs(graph, movie, visited = None):
    if visited is None:
        visited = []
    visited.append(movie)

    for neighbor in graph.graph_dict[movie].get_related_movies():
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def add_movie():

    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    #Inputting the details of the movie
    name = str(input("What is the name of the movie?"))
    if name in Movies.get_movies():
        print("This movie is already in the database.")
    else:
        genre = str(input("What is the genre of the movie?"))
        director = str(input("Who is the director of the movie?"))
        rating = float(input("What is the imdb rating of this movie?"))
        synopsis = str(input("What is the synopsis of the movie?"))
        Movies.add_movie(name, genre, director, rating, synopsis)

        # Adding the movie to my database
        cur = conn.cursor()
        insert_script = '''INSERT INTO movies (name, genre, director, imdb_rating, synopsis) VALUES (%s, %s, %s, %s, %s)'''
        insert_values = (name, genre, director, rating, synopsis)
        cur.execute(insert_script, insert_values)
        conn.commit()
        cur.close()
        conn.close()

    for item in dfs(Movies, 'Speed'):
        if Movies.graph_dict[item].genre == genre:
            Movies.add_edge(Movies.graph_dict[item], Movies.graph_dict[name])


start()
