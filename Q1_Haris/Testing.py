import http.client
import json
import csv
from collections import Counter
class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param string movie_id: a movie_id
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """

        'Opening connection'

        'Establishing initial connection with server'
        base_link='api.themoviedb.org'
        conn=http.client.HTTPSConnection(host=base_link)

        'Sending request for the movie_id to server'
        url_request='/3/movie/{}/credits?api_key={}&language=en-US'.format(movie_id,self.api_key)
        conn.request('GET',url_request)
        response=conn.getresponse()
        if response.status!=200:
            print('The particular movie id resulted in server sending an unindentified response')
            return None

        'Reading the data return by the server, the server sends the response back as a byte list, needs to be converted to Python object'
        byte_data=response.read()
        data=json.loads(byte_data)
        
        'Iterating through the returned data to create the required list of cast members'
        if limit is None:
            limit=2**32

        if exclude_ids is None:
            exclude_ids=[]

        results=[]

        'Checking if cast is in returned data'
        if 'cast' not in data.keys():
            return None

        for cast in data['cast']:
            if cast['id'] in exclude_ids:
                continue
            if cast['order']>=limit:
                continue
            cast['name']=cast['name'].replace(',','')
            results.append(cast)

        return results


    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        'Establishing initial connection with server'
        base_link='api.themoviedb.org'
        conn=http.client.HTTPSConnection(host=base_link)

        'Sending request for the person_id to server'
        url_request='/3/person/{}/movie_credits?api_key={}&language=en-US'.format(person_id,self.api_key)
        conn.request('GET',url_request)
        response=conn.getresponse()

        if response.status!=200:
            print('The particular movie id resulted in server sending an unindentified response')
            return None

        'Reading the data return by the server, the server sends the response back as a byte list, needs to be converted to Python object'
        byte_data=response.read()
        data=json.loads(byte_data)

        'Iterating through the returned data to create the required list of movies the cast member was in'
        results=[]

        if vote_avg_threshold is None:
            vote_avg_threshold=0

        'Checking if cast is in returned data'
        if 'cast' not in data.keys():
            return None

        for movie in data['cast']:
            if movie['vote_average']<vote_avg_threshold:
                continue
            else:
                results.append(movie)
                
        return results

test=TMDBAPIUtils(api_key='dda851cd3e59527d775becc901149227')
a=test.get_movie_cast('60112',2,['295'])
print(a[0])