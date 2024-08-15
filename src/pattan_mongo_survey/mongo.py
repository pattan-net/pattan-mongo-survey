from pymongo import MongoClient
from bson import ObjectId
import json
from bson.dbref import DBRef
from .exceptions import MissingSurveyId, DataSaveFailure, FetchResultsFailure, DeleteSurveyFailure, \
    DeleteSurveyResponseFailure, PattanMongoSurveyConfigurationError


class MongoSurveyService:
    """
    MongoSurveyService supports a mongo database backend for surveyJS
    """

    def __init__(self, config=None):
        """
        Constructor for MongoSurveyService
        :param config: A Dictionary containing the following configuration parameters
            'MONGDB_USER'
            'MONGDB_PASSWD'
            'MONGDB_HOST'
            'MONGDB_DB'
            'MONGDB_SURVEY_COLLECTION'
            'MONGDB_DB_RESPONSE_COLLECTION'
        """
        if config is None:
            raise PattanMongoSurveyConfigurationError
        else:
            self._is_configuration_valid(config)
        self.username = config['MONGDB_USER']
        self.password = config['MONGDB_PASSWD']
        self.host = config['MONGDB_HOST']
        self.database = config['MONGDB_DB']
        self.survey_collection = config['MONGDB_SURVEY_COLLECTION']
        self.response_collection = config['MONGDB_DB_RESPONSE_COLLECTION']
        self.mongo_con = MongoClient(self._get_mongo_connection_string())
        self.db = self.mongo_con[config['MONGDB_DB']]
        self.survey_db = self.db.survey

    def _get_mongo_connection_string(self):
        """
        Build the mongo db connection string.
        :return: None
        """
        return "mongodb+srv://{0}:{1}@{2}/".format(self.username, self.password, self.host)

    def get_survey_list(self):
        """
        Get a list of object ids and survey titles
        :return: list
        """
        result = []
        for survey in self.survey_db.find(projection={'_id': 1, 'survey': {'title': 1}}):
            survey['id'] = survey['_id']  # django template will not take a parameter that starts with in '_'
            result.append(survey)
        return result

    def get_survey(self, survey_id=None):
        """
        get_survey returns a survey object
        :param survey_id:
        :return: survey object id and a survey suitable to use as a surveyJS survey model
        """
        if survey_id is None:
            raise MissingSurveyId
        result = self.survey_db.find_one({'_id': ObjectId(survey_id)})
        return result

    def save_survey_response(self, response=None, survey_id=None):
        """
        Save a survey responses linked to a specific survey
        :param response: surveyJS response object
        :param survey_id: mongo object id of the survey
        :return: An instance of InsertOneResult (inserted id, and acknowledged)
        """
        if response is None:
            raise DataSaveFailure('Response cannot be None')
        if survey_id is None:
            raise MissingSurveyId
        survey_response = self.db.surveyResponse
        survey_reference = DBRef('survey', survey_id)
        try:
            result = survey_response.insert_one({'ref': survey_reference, 'answers': json.loads(response)})
        except Exception as e:
            raise DataSaveFailure
        return result

    def save_survey(self, data):
        data_dict = json.loads(data)
        survey_id = data_dict['survey_id']
        data_dict.pop('survey_id')
        try:
            if not survey_id:
                result = self.survey_db.insert_one({"survey": data_dict})
                survey_id = result.inserted_id
            else:
                # SurveyJS sends over the entire survey on every UI change
                # It also sends a saveNo, a value that increments with every call to save
                # NEVER save a smaller saveNo or you will lose data.
                # @todo send saveNo over with survey JSON
                self.survey_db.update_one(
                    {"_id": ObjectId(survey_id)},
                    {'$set': {"survey": data_dict}},
                    upsert=True
                )
        except Exception as e:
            return_message = {'message': 'failed to save survey'}
            return return_message
        return_message = {'message': 'results saved', 'survey_id': str(survey_id)}
        return return_message

    def get_survey_responses(self, survey_id=None):
        if survey_id is None:
            raise MissingSurveyId
        survey_response = self.db.surveyResponse
        survey_reference = DBRef('survey', survey_id)
        try:
            result = survey_response.find({'ref': survey_reference, })
        except Exception as e:
            raise FetchResultsFailure
        return list(result)

    def delete_survey(self, survey_id):
        if not survey_id:
            raise MissingSurveyId
        try:
            self.delete_survey_responses(survey_id)
        except DeleteSurveyResponseFailure:
            raise DeleteSurveyFailure('one or more responses failed to deleted')
        try:
            result = self.survey_db.delete_one({'_id': ObjectId(survey_id)})
        except Exception as e:
            raise DeleteSurveyFailure
        return True

    def delete_survey_responses(self, survey_id=None):
        if not survey_id:
            raise MissingSurveyId
        survey_response = self.db.surveyResponse
        survey_reference = DBRef('survey', survey_id)
        try:
            survey_response.delete_many({'ref': survey_reference})
        except Exception as e:
            raise DeleteSurveyResponseFailure
        return True

    def _is_configuration_valid(self, config_obj):
        config_keys = config_obj.keys()
        missing_keys = []

        if 'MONGDB_USER' not in config_keys:
            missing_keys.append('MONGDB_USER')
        if 'MONGDB_PASSWD' not in config_keys:
            missing_keys.append('MONGDB_PASSWD')
        if 'MONGDB_HOST' not in config_keys:
            missing_keys.append('MONGDB_HOST')
        if 'MONGDB_DB' not in config_keys:
            missing_keys.append('MONGDB_DB')
        if 'MONGDB_SURVEY_COLLECTION' not in config_keys:
            missing_keys.append('MONGDB_SURVEY_COLLECTION')
        if 'MONGDB_DB_RESPONSE_COLLECTION' not in config_keys:
            missing_keys.append('MONGDB_DB_RESPONSE_COLLECTION')

        if len(missing_keys) > 0:
            raise PattanMongoSurveyConfigurationError(
                "The following key(s) are missing {0}".format(' '.join(missing_keys)))
