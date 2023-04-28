import json
from typing import List

def parse_request(request: str) -> List[str]:
    return request.split(',')

def is_valid_json_format(json_data):
    if not isinstance(json_data, dict):
        return False

    required_top_level_keys = ["actions", "system"]
    if not all(key in json_data for key in required_top_level_keys):
        return False

    required_action_keys = ["name", "talk", "behavior", "emotion"]
    for action in json_data["actions"]:
        if not all(key in action for key in required_action_keys):
            return False

    # Check for unterminated strings in "talk", "behavior", and "emotion" fields
    for action in json_data["actions"]:
        for key in ["talk", "behavior", "emotion"]:
            if not isinstance(action[key], str):
                return False

    return True


#def is_valid_json_format(json_data):
#    if not isinstance(json_data, dict):
#        return False
#
#    required_top_level_keys = ["actions", "system"]
#    if not all(key in json_data for key in required_top_level_keys):
#        return False
#
#    required_action_keys = ["name", "talk", "behavior", "emotion"]
#    for action in json_data["actions"]:
#        if not all(key in action for key in required_action_keys):
#            return False
#
#    return True