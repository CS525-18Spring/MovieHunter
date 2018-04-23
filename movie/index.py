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


def get_rating(id):
    return rating_dic[id]


def get_act_num(id):
    records = Act.objects.filter(actorid_id=id)
    return len(records)


def _rotate(term):
    x = term + "$"
    if "*" not in term:
        return x
    n = x.index("*") + 1
    return (x[n:] + x[:n])


def add_Wild_Card(term):
    tokens = []
    n = len(term)
    for i in range(n + 1):
        tokens.append(term[:i] + "*" + term[i:])
    return tokens


def wildcard_search(text):
    result = []
    intersection_result, union_result = set(), set()
    movie_objects = Movie.objects.all()
    for movie in movie_objects:
        intersection_result.add(movie.movieid)
    actor_objects = Actor.objects.all()
    for actor in actor_objects:
        intersection_result.add(actor.actorid)
    for token in tokenize(text):
        result_files = set()
        tokens = add_Wild_Card(token)
        for t in tokens:
            search_token = _rotate(t)
            result_files = result_files.union(crawl_tree(permuterm_index.root, search_token))
            intersection_result = intersection_result.intersection(result_files)
            union_result = union_result.union(result_files)

    inter_movies, inter_actors = set(), set()
    for id in intersection_result:
        inter_movies.add(id) if id[:2] == "tt" else inter_actors.add(id)
    inter_movies = sorted(inter_movies, key=get_rating, reverse=True)
    inter_actors = sorted(inter_actors, key=get_act_num, reverse=True)

    union_movies, union_actors = set(), set()
    for id in union_result:
        if id not in inter_movies and id not in inter_actors:
            union_movies.add(id) if id[:2] == "tt" else union_actors.add(id)
    union_movies = sorted(union_movies, key=get_rating, reverse=True)
    union_actors = sorted(union_actors, key=get_act_num, reverse=True)

    result.append(inter_movies + union_movies)
    result.append(inter_actors + union_actors)
    return result


def crawl_tree(node, term):
    if not node:
        return set()
    if ('*' in term and node.key.startswith(term[:-1])) or term == node.key:
        x = node.data
    else:
        x = set()
    return x.union(crawl_tree(node.left, term)).union(crawl_tree(node.right, term))
