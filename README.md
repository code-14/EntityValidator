# EntityValidator
# Instructions to run the App in Docker

*Build the image: 
```
build . -t docker-django-v0.0
```
*Run the image:
```
docker run
```
*run the app
```
docker run docker-django-v0.0
```


#Assignment
*Assignment
*Terminology
*Utterance
*Anything the user says.



*For example, if a user says “I am 22 years old and I only have my college ID. Can I do a room booking?", the entire sentence is the utterance.

*Intent
*An intent is the user’s intention.



*For example, if a user says “Can I do a room booking ?”, the user’s intent is to ask their eligibility to book a room at a hotel. Intents are given a name, often a verb and a noun, such as room_booking_eligibility.

*Entity/Slot
*An entity modifies an intent.



*For example, if a user says “I am 22 years old and I only have my college ID”, the entities are “22 years old” and “college ID" i.e. age=22, govt_id=college. Entities are given a name, such as age and govt_id.



*Entities are also referred to as slots.



*NOTE: An intent may have multiple slots in it.

*Assignment
*Create a Django app which has 2 REST APIs.
*This Django app must then be runnable via Docker.



*The following are the 4 main steps in this assignment:

#1. POST API to validate a slot with a finite set of values.
*Sample Request:
```
{
  "invalid_trigger": "invalid_ids_stated",
  "key": "ids_stated",
  "name": "govt_id",
  "reuse": true,
  "support_multiple": true,
  "pick_first": false,
  "supported_values": [
    "pan",
    "aadhaar",
    "college",
    "corporate",
    "dl",
    "voter",
    "passport",
    "local"
  ],
  "type": [
    "id"
  ],
  "validation_parser": "finite_values_entity",
  "values": [
    {
      "entity_type": "id",
      "value": "college"
    }
  ]
}

```
*Sample Response based on sample request:


```
{
    "filled": true,
    "partially_filled": false,
    "trigger": '',
    "parameters": {
        "ids_stated": ["COLLEGE"]
    }
}
```

*Please refer to the func docstring below to get a better understanding of the incoming payload's JSON schema keys' meanings.  The input will be in this format exactly. The data referenced in the keys of the JSON will differ when testing your code.  Please try to keep your func as generic as possible. Tie it to the data at your own peril :)



*Use this JSON as input for the following function:
```
from typing import List, Dict, Callable, Tuple
SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                invalid_trigger: str = None, key: str = None,
                                support_multiple: bool = True, pick_first: bool = False, **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if the values extracted("values" arg) lies within the finite list of supported values(arg "supported_values").

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param supported_values: List of supported values for the slot
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    ...
```

*filled : True if all values are valid



*partially_filled:

*True when a subset of values are valid

*True when there are values and none of them are valid

*Expected results based on sample request for the function validate_finite_values_entity:


```
+--------------------------+--------------------------------------+
| Values Array             | Result                               |
+--------------------------+--------------------------------------+
| [                        | true,                                |
|   {                      | false,                               |
|     "entity_type": "id", | "",                                  |
|     "value": "college"   | {'ids_stated':['COLLEGE']}           |
|   }                      |                                      |
| ]                        |                                      |
+--------------------------+--------------------------------------+
| [                        | false,                               |
|   {                      | true,                                |
|     "entity_type": "id", | 'invalid_ids_stated',                |
|     "value": "other"     | {}                                   |
|   }                      |                                      |
| ]                        |                                      |
+--------------------------+--------------------------------------+
| []                       | false,                               |
|                          | false,                               |
|                          | 'invalid_ids_stated',                |
|                          | {}                                   |
+--------------------------+--------------------------------------+
| [                        | false,                               |
|   {                      | true,                                |
|     "entity_type": "id", | 'invalid_ids_stated',                |
|     "value": "college"   | {}                                   |
|   },                     |                                      |
|   {                      |                                      |
|     "entity_type": "id", |                                      |
|     "value": "other"     |                                      |
|   }                      |                                      |
| ]                        |                                      |
+--------------------------+--------------------------------------+
| [                        | true,                                |
|   {                      | false,                               |
|     "entity_type": "id", | "",                                  |
|     "value": "college"   | {'ids_stated':['COLLEGE','AADHAAR']} |
|   },                     |                                      |
|   {                      |                                      |
|     "entity_type": "id", |                                      |
|     "value": "aadhaar"   |                                      |
|   }                      |                                      |
| ]                        |                                      |
+--------------------------+--------------------------------------+

```


*If pick_first is true in the sample request, the ids_stated in params must be a string instead of a list.



*If support_multiple is true in the sample request, the ids_stated must be a list of supported IDs passed in the values list.



*This function's result should be wrapped by the Django view and the POST API's response should be in the format:


```
{
    "filled": <filled flag>,
    "partially_filled": <partially filled flag>,
    "trigger": <trigger value>,
    "parameters": <params dict from func>
}
```

*Example:
*If values is

```

{
    "entity_type": "id",
    "value": "college"
}
```

*key is ids_stated, support_multiple is true
*and "college" exists in the supported_values list,



*then the response should be


```
{
    "filled": true,
    "partially_filled": false,
    "trigger": '',
    "parameters": {
        "ids_stated": ["COLLEGE"]
    }
}
```
#2. POST API to validate a slot with a numeric value extracted and constraints on the value extracted.
*Sample Request:


```
{
  "invalid_trigger": "invalid_age",
  "key": "age_stated",
  "name": "age",
  "reuse": true,
  "pick_first": true,
  "type": [
    "number"
  ],
  "validation_parser": "numeric_values_entity",
  "constraint": "x>=18 and x<=30",
  "var_name": "x",
  "values": [
    {
      "entity_type": "number",
      "value": 23
    }
  ]
}

```
*The constraint expression will follow python syntax.



*Sample Response based on sample request:
```
{
    "filled": true,
    "partially_filled": false,
    "trigger": '',
    "parameters": {
        "age_stated": 23
    }
}
```

*Use this JSON as input for the following function:


```
from typing import List, Dict, Callable
SlotValidationResult = Tuple[bool, bool, str, Dict]

def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None,
                            **kwargs) -> SlotValidationResult:
    """
    Validate an entity on the basis of its value extracted.
    The method will check if that value satisfies the numeric constraints put on it.
    If there are no numeric constraints, it will simply assume the value is valid.

    If there are numeric constraints, then it will only consider a value valid if it satisfies the numeric constraints.
    In case of multiple values being extracted and the support_multiple flag being set to true, the extracted values
    will be filtered so that only those values are used to fill the slot which satisfy the numeric constraint.

    If multiple values are supported and even 1 value does not satisfy the numeric constraint, the slot is assumed to be
    partially filled.

    :param pick_first: Set to true if the first value is to be picked up
    :param support_multiple: Set to true if multiple utterances of an entity are supported
    :param values: Values extracted by NLU
    :param invalid_trigger: Trigger to use if the extracted value is not supported
    :param key: Dict key to use in the params returned
    :param constraint: Conditional expression for constraints on the numeric values extracted
    :param var_name: Name of the var used to express the numeric constraint
    :return: a tuple of (filled, partially_filled, trigger, params)
    """
    ...

```
*filled : True if all values are valid



*partially_filled:

*True when a subset of values are valid

*True when there are values and none of them are valid



*Expected Results for the validate_numeric_entity function based on the sample input:


```
+------------------------------+------------------------+
| Values Array                 | Result                 |
+------------------------------+------------------------+
| [                            |                        |
|   {                          | true,                  |
|     "entity_type": "number", | false,                 |
|     "value": 21              | "",                    |
|   }                          | {'age_stated':21}      |
| ]                            |                        |
+------------------------------+------------------------+
| [                            |                        |
|   {                          | false,                 |
|     "entity_type": "number", | true,                  |
|     "value": -1              | 'invalid_age_stated',  |
|   }                          | {}     |
| ]                            |                        |
+------------------------------+------------------------+
|                              | false,                 |
| []                           | false,                 |
|                              | 'invalid_age_stated',  |
|                              | {}                     |
+------------------------------+------------------------+
| [                            |                        |
|   {                          |                        |
|     "entity_type": "number", |                        |
|     "value": 22              | false,                 |
|   },                         | true,                  |
|   {                          | 'invalid_age_stated',  |
|     "entity_type": "number", | {'age_stated': 22}     |
|     "value": 10              |                        |
|   }                          |                        |
| ]                            |                        |
+------------------------------+------------------------+
| [                            | true,                  |
|   {                          | false,                 |
|     "entity_type": "number", | "",                    |
|     "value": 24              | {'age_stated': 24}     |
|   },                         |                        |
|   {                          |                        |
|     "entity_type": "number", |                        |
|     "value": 22              |                        |
|   }                          |                        |
| ]                            |                        |
+------------------------------+------------------------+
```



*If pick_first is true, the age_stated in params must be an integer instead of a list. If support_multiple is true, the age_stated must be a list of valid ages passed in the values.



*This function's result should be wrapped by the Django view and the POST API's response should be in the form:


```
{
    "filled": <filled flag>,
    "partially_filled": <partially filled flag>,
    "trigger": <trigger value>,
    "parameters": <params dict from func>
}
```
#3. Creating a Dockerfile
*Once the Django app is complete. Create a Dockerfile which will be used to build a Docker image where your Django app will reside.



*Try to ensure that the dockerfile is as small as possible.



*Please also share the command required to start your docker container and run your Django app once the Docker image is built.



#4. Hosting the code on GitHub and sharing the same
*Please host the code written by you in a private GitHub repo and share the same.
*Please state the Docker image size in the README of the repo.



*Please host the code written by you in a private github repo and share the same. Please state the docker image size in the README of the repo.



*Add the following as contributors to the repo:

*VaiAutomation

*vipul-sharma20

*muku2211

*DebPaine

*dimplemathewkc
