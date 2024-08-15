Module pattan_mongo_survey.mongo
================================

Classes
-------

`MongoSurveyService(config=None)`
:   MongoSurveyService supports a mongo database backend for surveyJS
    
    Constructor for MongoSurveyService
    :param config: A Dictionary containing the following configuration parameters
        'MONGDB_USER'
        'MONGDB_PASSWD'
        'MONGDB_HOST'
        'MONGDB_DB'
        'MONGDB_SURVEY_COLLECTION'
        'MONGDB_DB_RESPONSE_COLLECTION'

    ### Methods

    `delete_survey(self, survey_id)`
    :

    `delete_survey_responses(self, survey_id=None)`
    :

    `get_survey(self, survey_id=None)`
    :   get_survey returns a survey object
        :param survey_id:
        :return: survey object id and a survey suitable to use as a surveyJS survey model

    `get_survey_list(self)`
    :   Get a list of object ids and survey titles
        :return: list

    `get_survey_responses(self, survey_id=None)`
    :

    `save_survey(self, data)`
    :

    `save_survey_response(self, response=None, survey_id=None)`
    :   Save a survey responses linked to a specific survey
        :param response: surveyJS response object
        :param survey_id: mongo object id of the survey
        :return: An instance of InsertOneResult (inserted id, and acknowledged)