# Mongo

[Pattan_mongo_survey Index](./README.md#pattan_mongo_survey-index) / Mongo

> Auto-generated documentation for [mongo](../../../mongo.py) module.

- [Mongo](#mongo)
  - [MongoSurveyService](#mongosurveyservice)
    - [MongoSurveyService()._get_mongo_connection_string](#mongosurveyservice()_get_mongo_connection_string)
    - [MongoSurveyService()._is_configuration_valid](#mongosurveyservice()_is_configuration_valid)
    - [MongoSurveyService().delete_survey](#mongosurveyservice()delete_survey)
    - [MongoSurveyService().delete_survey_responses](#mongosurveyservice()delete_survey_responses)
    - [MongoSurveyService().get_survey](#mongosurveyservice()get_survey)
    - [MongoSurveyService().get_survey_list](#mongosurveyservice()get_survey_list)
    - [MongoSurveyService().get_survey_responses](#mongosurveyservice()get_survey_responses)
    - [MongoSurveyService().save_survey](#mongosurveyservice()save_survey)
    - [MongoSurveyService().save_survey_response](#mongosurveyservice()save_survey_response)

## MongoSurveyService

[Show source in mongo.py:12](../../../mongo.py#L12)

MongoSurveyService supports a mongo database backend for surveyJS

#### Signature

```python
class MongoSurveyService:
    def __init__(self, config=None): ...
```

### MongoSurveyService()._get_mongo_connection_string

[Show source in mongo.py:42](../../../mongo.py#L42)

Build the mongo db connection string.

#### Returns

None

#### Signature

```python
def _get_mongo_connection_string(self): ...
```

### MongoSurveyService()._is_configuration_valid

[Show source in mongo.py:169](../../../mongo.py#L169)

Called by constructor to check if a configuration object is valid.

#### Arguments

- `config_obj` - python dictionary containing configuration parameters

#### Returns

True if the configuration is valid, raises PattanMongoSurveyConfigurationError otherwise.

#### Signature

```python
def _is_configuration_valid(self, config_obj): ...
```

### MongoSurveyService().delete_survey

[Show source in mongo.py:135](../../../mongo.py#L135)

Delete a survey and all its related responses

#### Arguments

- `survey_id` - mongo object id of the survey

#### Returns

True if the survey was deleted, raises DeleteSurveyFailure exception otherwise

#### Signature

```python
def delete_survey(self, survey_id): ...
```

### MongoSurveyService().delete_survey_responses

[Show source in mongo.py:153](../../../mongo.py#L153)

Delete all user response to a specific survey but not the survey.

#### Arguments

- `survey_id` - mongo object id of the survey

#### Returns

True if all survey responses were deleted, raises DeleteSurveyResponseFailure exception otherwise

#### Signature

```python
def delete_survey_responses(self, survey_id=None): ...
```

### MongoSurveyService().get_survey

[Show source in mongo.py:60](../../../mongo.py#L60)

get_survey returns a survey object

#### Arguments

- `survey_id`

#### Returns

survey object id and a survey suitable to use as a surveyJS survey model

#### Signature

```python
def get_survey(self, survey_id=None): ...
```

### MongoSurveyService().get_survey_list

[Show source in mongo.py:49](../../../mongo.py#L49)

Get a list of object ids and survey titles

#### Returns

list

#### Signature

```python
def get_survey_list(self): ...
```

### MongoSurveyService().get_survey_responses

[Show source in mongo.py:119](../../../mongo.py#L119)

Get all user response to a specific survey

#### Arguments

- `survey_id` - mongo object id of the survey

#### Signature

```python
def get_survey_responses(self, survey_id=None): ...
```

### MongoSurveyService().save_survey

[Show source in mongo.py:90](../../../mongo.py#L90)

Save a surveyJS model to the mongo survey collection

#### Arguments

- `data` - surveyJS model

#### Returns

JSON containing a message object indicating success or failure

#### Signature

```python
def save_survey(self, data): ...
```

### MongoSurveyService().save_survey_response

[Show source in mongo.py:71](../../../mongo.py#L71)

Save a survey responses linked to a specific survey

#### Arguments

- `response` - surveyJS response object
- `survey_id` - mongo object id of the survey

#### Returns

An instance of InsertOneResult (inserted id, and acknowledged)

#### Signature

```python
def save_survey_response(self, response=None, survey_id=None): ...
```