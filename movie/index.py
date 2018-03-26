from movie.models import *
from movie import binarytree

def _permute(term):
    x = term + "$"
    return [x[i:] + x[:i] for i in range(len(x))]

def tokenize(text):
    import re
    clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
    tokens = clean_string.split()
    return tokens

def index_dir():
    global permuterm_index
    permuterm_index = binarytree.binary_tree()
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        for term in tokenize(movie.title):
            for permuted_term in _permute(term):
                if permuted_term not in permuterm_index:
                    permuterm_index[permuted_term] = set()
                if movie.movieid not in permuterm_index[permuted_term]:
                    permuterm_index[permuted_term].add(movie.movieid)
    actor_objects = Actor.objects.all()
    for actor in actor_objects:
        for a_term in tokenize(actor.name):
            for a_permuted_term in _permute(a_term):
                if a_permuted_term not in permuterm_index:
                    permuterm_index[a_permuted_term] = set()
                if actor.actorid not in permuterm_index[a_permuted_term]:
                    permuterm_index[a_permuted_term].add(actor.actorid)
    # return permuterm_index


def rating_dir():
    global rating_dic
    rating_dic = {}
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        rating_dic[movie.movieid] = movie.rate
