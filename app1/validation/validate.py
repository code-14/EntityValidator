import collections
from typing import List, Dict, Callable
from simpleeval import simple_eval


def wrapper_validate_finite_values_entity(jsoninput):
    jsoninput1 = jsoninput
    invalid_trigger = jsoninput1["invalid_trigger"]
    key = jsoninput1["key"]
    supported_multiple = False
    pick_first = False
    supported_values = jsoninput1["supported_values"]
    values = jsoninput1["values"]

    if "pick_first" in jsoninput1:
        pick_first = jsoninput1["pick_first"]
    if "supported_multiple" in jsoninput1:
        supported_multiple = jsoninput1["supported_multiple"]

    finalResult = validate_finite_values_entity(values, supported_values, invalid_trigger, key, supported_multiple,
                                                pick_first)
    return finalResult


def validate_finite_values_entity(values: List[Dict], supported_values: List[str] = None,
                                  invalid_trigger: str = None, key: str = None,
                                  support_multiple: bool = True, pick_first: bool = False):
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
    # Initialization of the output values
    output = collections.OrderedDict()
    output['filled'] = False
    output['partially_filled'] = False
    output['trigger'] = ""
    output['parameters'] = {}

    # If there are no values provided, invalid trigger value is set to invalid trigger and
    # rest values are same as that of the initialised values
    if len(values) == 0:
        output['trigger'] = invalid_trigger
       # entity_validation_result = tuple(
        #    [filled, partially_filled, trigger, parameters])
        return output

    # If there is one or more than one value it doesn't matter if it is present in the supported values or not
    # partially filled is true
    if len(values) > 0:
        output['partially_filled'] = True

    supported_values = set(supported_values)

    # to return parameters if any value present is found in the supported values
    parameters[key] = []

    for val in values:
        if val["value"] in supported_values:
            parameters[key].append(val["value"].upper())
        else:
            # if any value present is not found in supported values trigger for invalid trigger is raised
            output['trigger'] = invalid_trigger
    # If all the values are present in the supported values then filled is true
    if output['trigger'] != invalid_trigger:
        output['filled'] = True
        output['partially_filled'] = False
    else:
        # to remove some values that we have appended which were found in supported values
        parameters = {}
    if (pick_first == true):
        # only first value is taken and a string is returned
        parameters[key] = str(values[0]["value"].upper())

    output['parameters'] = parameters
    # entity_validation_result = tuple(
    #   [filled, partially_filled, trigger, parameters])
    return output


def wrapper_validate_numeric_entity(jsoninput):
    jsoninput1 = jsoninput
    invalid_trigger = jsoninput1["invalid_trigger"]
    key = jsoninput1["key"]
    pick_first = False
    supported_multiple = False
    constraint = jsoninput1["constraint"]
    var_name = jsoninput1["var_name"]
    values = jsoninput1["values"]

    if "pick_first" in jsoninput1:
        pick_first = jsoninput1["pick_first"]
    if "supported_multiple" in jsoninput1:
        supported_multiple = jsoninput1["supported_multiple"]

    finalResult = validate_numeric_entity(values, invalid_trigger, key, supported_multiple, pick_first, constraint,
                                          var_name)
    return finalResult


def validate_numeric_entity(values: List[Dict], invalid_trigger: str = None, key: str = None,
                            support_multiple: bool = True, pick_first: bool = False, constraint=None, var_name=None):
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
    # Initialization of the output values
    output = collections.OrderedDict()
    output['filled'] = False
    output['partially_filled'] = False
    output['trigger'] = ""
    output['parameters'] = {}

    # If there are no values provided, invalid trigger value is set to invalid trigger and
    # rest values are same as that of the initialised values
    if len(values) == 0:
        output['trigger'] = invalid_trigger
        return output
    # If thre is no contraint provided any value(age) present is considered valid..here negative values is not onsidered
    if constraint == "":
        output['filled'] = True
        # only first value is taken and an integer is returned
        if pick_first:
            parameters[key] = values[0]["value"]
            return output

        # to return parameters if any value present valid according to the constraint
        parameters[key] = []
        for val in values:
            parameters[key].append(val["value"])

        output['parameters'] = parameters
        return output

    # If there is one or more than one value it doesn't matter if it is present in the supported values or not
    # partially filled is true
    if len(values) > 0:
        output['partially_filled'] = True

    parameters[key] = []
    # simple_eval is used as it can parse this constraint string and evaluate the expression easily
    # without evaluating and providing logic explicitly since constraint can be in any form
    # x = 30 || x<20 ||  50>x >=30 etc
    for val in values:
        valid = simple_eval(constraint, names={var_name: val})
        if valid:
            parameters[key].append(diction["value"])
        else:
            # if any value present is not valid according to the constraint then trigger for invalid trigger is raised
            output['trigger'] = invalid_trigger
    # If all the values are present are according to the constraint then filled is true
    if output['trigger'] != invalid_trigger:
        output['filled'] = True
        output['partially_filled'] = False

    if pick_first:
        parameters[key] = values[0]["value"]

    output['parameters'] = parameters
    return output


def entity_parse_and_validate(data):

    output = collections.OrderedDict()
    output["intents_info"] = {
            "name": data["intents_info"]["name"], "slots": []}
    output["parameters"] = []
    output["slots_filled"] = []
    output["trigger"] = ""
    slots_input = data["intents_info"]["slots"]
    mapper = {"finite_values_entity": wrapper_validate_finite_values_entity,
                            "numeric_values_entity": wrapper_validate_numeric_entity}

    # mapping the validation parser
    for slot in slots_input:
        validate = slot["validation_parser"]
    validate_func = mapper[validate]

    result = validate_func(slot)

    tslot = {"name": slot["name"], "filled": result["filled"],
                    "partially_filled": result["partially_filled"]}

    output["intents_info"]["slots"].append(tslot)
    output["parameters"].append(result["parameters"])
    output["slots_filled"].append(slot["name"])

    # creating new slots filled
    newslots_filled = []
    for i in range(len(output["intents_info"])):
        res = output["intents_info"][i]
        if not res["filled"]:
            output["trigger"] = output["trigger"] + \
                    "_" + output["slots_filled"][i]
        continue
        newslots_filled.append(output["slots_filled"][i])

    output["slots_filled"] = newslots_filled
    # creating new parameters
    new_parameters = {}
    for i in range(len(output["parameters"])):
        if len(output["parameters"][i]) > 0:
            li = tuple(output["parameters"][i].items())
        print(li)
        new_parameters[li[0][0]] = li[0][1]
    # returning result
    output["parameters"] = new_parameters
    output["trigger"] = "_" + output["intents_info"]["name"] + \
            "_collect_" + output["trigger"] + "_"
    finalResult = tuple([output["intents_info"], output["parameters"], output["slots_filled"], output["trigger"])
    return result
