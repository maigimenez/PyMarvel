# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

import json
from datetime import datetime

from .core import MarvelObject, DataWrapper, DataContainer, Summary, List
from .comic import Comic, ComicDataWrapper

class CharacterDataWrapper(DataWrapper):
    @property
    def data(self):
        return CharacterDataContainer(self.marvel, self.dict['data'])

    def next(self):
        """
        Returns new CharacterDataWrapper
        TODO: Don't raise offset past count - limit
        """
        self.params['offset'] = str(int(self.params['offset']) + int(self.params['limit']))
        return self.marvel.get_characters(self.marvel, (), **self.params)

    def previous(self):
        """
        Returns new CharacterDataWrapper
        TODO: Don't lower offset below 0
        """
        self.params['offset'] = str(int(self.params['offset']) - int(self.params['limit']))
        return self.marvel.get_characters(self.marvel, (), **self.params)


class CharacterDataContainer(DataContainer):
    @property
    def results(self):
        return self.list_to_instance_list(self.dict['results'], Character)


class Character(MarvelObject):
    """
    Character object
    Takes a dict of character attrs
    """
    _resource_url = 'characters'


    @property
    def id(self):
        return self.dict['id']

    @property
    def name(self):
        return self.dict['name']

    @property
    def description(self):
        return self.dict['description']

    @property
    def modified(self):
        return str_to_datetime(self.dict['modified'])

    @property
    def modified_raw(self):
        return self.dict['modified']

    @property
    def resourceURI(self):
        return self.dict['resourceURI']

    @property
    def urls(self):
        return self.dict['urls']

    @property
    def wiki(self):
        for item in self.dict['urls']:
            if item['type'] == 'wiki':
                return item['url']
        return None

    @property
    def detail(self):
        for item in self.dict['urls']:
            if item['type'] == 'detail':
                return item['url']
        return None

    @property
    def thumbnail(self):
        return "%s.%s" % (self.dict['thumbnail']['path'], self.dict['thumbnail']['extension'] )


    """
    comics (ComicList, optional): A resource list containing comics which feature this character.,
    stories (StoryList, optional): A resource list of stories in which this character appears.,
    events (EventList, optional): A resource list of events in which this character appears.,
    series (SeriesList, optional): A resource list of series in which this character appears.
    """

    @property
    def comics(self):
        from .comic import ComicList
        """
        Returns ComicList object
        """
        return ComicList(self.marvel, self.dict['comics'])
        
        
        
    def get_comics(self, *args, **kwargs):
        """
        Returns a full ComicDataWrapper object this character.
        
        /characters/{characterId}/comics
        
        :returns:  ComicDataWrapper -- A new request to API. Contains full results set.
        """
        url = "%s/%s/%s" % (Character.resource_url(), self.id, Comic.resource_url())
        response = json.loads(self.marvel._call(url, self.marvel._params(kwargs)).text)
        return ComicDataWrapper(self, response)
        

class CharacterList(List):
    """
    CharacterList object
    """
    @property
    def items(self):
        """
        Returns List of CharacterSummary objects
        """
        return self.list_to_instance_list(self.dict['items'], CharacterSummary)

class CharacterSummary(Summary):
    """
    CharacterSummary object
    """
        
    @property
    def role(self):
        return self.dict['role']