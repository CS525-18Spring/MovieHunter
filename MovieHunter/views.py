from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import random


@csrf_protect
def index(request):
    if request.POST:
        if request.POST.get('Search'):
            content = request.POST.get('title')
            return redirect('/movie/search/' + content)
    else:
        data = {}
        if request.user.is_authenticated:
            data = {'username': request.user.get_username()}

            movies = Movie.objects.all()
            elements = []
            corpus = []
            for movie in movies:
                if movie.plot != None and movie.plot != '':
                    elements.append({'movieid': movie.movieid})
                    corpus.append(movie.plot)

            vectorizer = CountVectorizer()
            transformer = TfidfTransformer()
            tfidf = transformer.fit_transform(
                vectorizer.fit_transform(corpus).todense())
            weight = tfidf.toarray()

            for i in range(len(elements)):
                elements[i]['vector'] = weight[i]

            recommendations = set()
            seens = Seen.objects.filter(username=request.user.get_username())
            if len(seens) != 0:
                find_recommendations(recommendations, seens, elements)
            else:
                expects = Expect.objects.filter(username=request.user.get_username())
                if len(expects) != 0:
                    find_recommendations(recommendations, expects, elements)

            recommendation = []
            print('num', len(recommendations))
            if len(recommendations) <= 5:
                print('zysssss')
                for movieid in recommendations:
                    try:
                        temp = {}
                        temp['movieid'] = movieid
                        temp['poster'] = Movie.objects.get(movieid=movieid).poster
                        recommendation.append(temp)
                    except:
                        continue
            else:
                for movieid in random.sample(recommendations, 5):
                    try:
                        temp = {}
                        temp['movieid'] = movieid
                        temp['poster'] = Movie.objects.get(movieid=movieid).poster
                        recommendation.append(temp)
                    except:
                        continue
            data['recommendations'] = recommendation

        popular_movies = Popularity.objects.all().order_by('-weight')
        popular = []
        for movie in popular_movies[:5]:
            try:
                temp = {}
                temp['movieid'] = movie.movieid_id
                temp['poster'] = Movie.objects.get(movieid=movie.movieid_id).poster
                popular.append(temp)
            except:
                continue
        data['popular'] = popular

        return render(request, 'base.html', data)


def find_recommendations(recommendations, seens_or_expects, elements):
    for seen in seens_or_expects:
        plot = Movie.objects.get(movieid=seen.movieid.movieid).plot
        if plot == None or plot == '':
            continue
        cur_vector = []
        for element in elements:
            if element['movieid'] == seen.movieid.movieid:
                cur_vector = element['vector']
        for element in elements:
            dist = euclidean_distances(cur_vector, element['vector'])
            element['dist'] = dist
        sorted(elements, key=lambda e: e['dist'])
        for i in range(1, 11):
            recommendations.add(elements[i]['movieid'])
        print('test', len(seens_or_expects))
