class Movie:
    def __init__(self, name, genre, director, rating, synopsis):
        self.name = name
        self.genre = genre
        self.director = director
        self.rating = rating
        self.synopsis = synopsis
        self.recommendation = {}

    def relate(self, movie):
        self.recommendation[movie] = movie

    def get_related_movies(self):
        return list(self.recommendation.keys())
    
class Movie_Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_movie(self, name, genre, director, rating, synopsis):
        self.graph_dict[name] = Movie(name, genre, director, rating, synopsis)

    def add_edge(self, movie1, movie2):
        self.graph_dict[movie1.name].relate(movie2.name)
        self.graph_dict[movie2.name].relate(movie1.name)

    def get_movies(self):
        return list(self.graph_dict.keys())
