"Read JSON file."

import json
from pathlib import Path

def read_json(path):
    "Read JSON file."
    assert isinstance(path, Path)
    try:
        with path.open('r') as json_file:
            dic = json.load(json_file)
    except json.decoder.JSONDecodeError as err:
        print(f"Could not read {path}: {str(err)}")
        return {}
    except FileNotFoundError as err:
        raise FileNotFoundError(err)
    return dic
