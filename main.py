import os
import json

PATHS : dict[str, str] = {
    "beastie_data" : "JSONs/beastie_data.json",
    "move_dict" : "JSONs/move_dic.json",
    "all_text" : "JSONs/game.json",
    "internal_name" : "JSONs/beastie_internal_name.json",
}

dicts : dict[str, dict[str, str]] = {
    "beastie_data" : {},
    "move_dict" : {},
    "all_text" : {},
    "internal_name" : {},
}


def main() -> None:
    if not _is_paths_valid():
        return
    
    _load_jsons()


def _is_paths_valid() -> bool:
    for path in PATHS.values():
        if not os.path.exists(path):
            print(f"JSON at {path} doesn't exist!")
            return False
    return True


def _load_jsons() -> None:
    for key in PATHS.keys():
        with open(PATHS[key], mode="r") as file:
            dicts[key] = json.load(file)
            

if __name__ == "__main__":
    main()