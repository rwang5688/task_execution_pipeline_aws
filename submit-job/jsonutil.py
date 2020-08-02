import json

def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def get_pretty_string(json_data):
    return json.dumps(json_data, indent = 4, sort_keys=True)


def get_string(json_data):
    return json.dumps(json_data)

