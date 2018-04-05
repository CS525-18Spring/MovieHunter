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

def _rotate(term):
    x = term + "$"
    if "*" not in term:
        return x
    n = x.index("*") + 1
    return (x[n:] + x[:n])


def wildcard_search(text):
    result = []
    intersection_result = set()
    union_result = set()
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        intersection_result.add(movie.movieid)
    actor_objects = Actor.objects.all()
    for actor in actor_objects:
        intersection_result.add(actor.actorid)
    for token in tokenize(text):
        result_files = set()
        # search_token = _rotate(token)
        search_token_1 = _rotate("*" + token)
        search_token_2 = _rotate(token + "*")
        # result_files = result_files.union(crawl_tree(permuterm_index.root, search_token))
        result_files = result_files.union(crawl_tree(permuterm_index.root, search_token_1))
        result_files = result_files.union(crawl_tree(permuterm_index.root, search_token_2))
        intersection_result = intersection_result.intersection(result_files)
        union_result = union_result.union(result_files)
    movies, actors = set(), set()
    for id in intersection_result:
        movies.add(id) if id[:2] == "tt" else actors.add(id)
    for id in union_result:
        movies.add(id) if id[:2] == "tt" else actors.add(id)
    result.append(list(movies))
    result.append(list(actors))
    return result


def crawl_tree(node, term):
    if not node:
        return set()
    if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
        x = node.data
    else:
        x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))
