from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson import ObjectId
import json
from bson.dbref import DBRef
from .exceptions import MissingSurveyId, DataSaveFailure, FetchResultsFailure, DeleteSurveyFailure, \
    DeleteSurveyResponseFailure, PattanMongoSurveyConfigurationError


class MongoSurveyService:

    def __init__(self, config=None):
        if config is None:
            raise PattanMongoSurveyConfigurationError
        self.username = config['MONGDB_USER']
        self.password = config['MONGDB_PASSWD']
        self.host = config['MONGDB_HOST']
        self.database = config['MONGDB_DB']
        self.survey_collection = config['MONGDB_SURVEY_COLLECTION']
        self.response_collection = config['MONGDB_DB_RESPONSE_COLLECTION']
        self.mongo_con = MongoClient(self.get_mongo_connection_string())
        self.db = self.mongo_con[config['MONGDB_DB']]
        self.survey_db = self.db.survey

    def get_mongo_connection_string(self):
        return "mongodb+srv://{0}:{1}@{2}/".format(self.username, self.password, self.host)

    def get_survey_list(self):
        result = []
        for survey in self.survey_db.find(projection={'_id': 1, 'survey': {'title': 1}}):
            survey['id'] = survey['_id']  # django template will not take a parameter that starts with in '_'
            result.append(survey)
        return result

    def get_survey(self, survey_id=None):
        if not survey_id:
            raise MissingSurveyId
        result = self.survey_db.find_one({'_id': ObjectId(survey_id)})
        return result

    def save_survey_response(self, response, survey_id):
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

    def get_survey_responses(self, survey_id):
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

    def delete_survey_responses(self, survey_id):
        survey_response = self.db.surveyResponse
        survey_reference = DBRef('survey', survey_id)
        try:
            survey_response.delete_many({'ref': survey_reference})
        except Exception as e:
            raise DeleteSurveyResponseFailure
        return True
