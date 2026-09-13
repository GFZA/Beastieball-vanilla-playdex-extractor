import os
import json

PATHS : dict[str, str] = {
    "beastie_data" : "JSONs/beastie_data.json",
    "move_dict" : "JSONs/move_dic.json",
    "all_text" : "JSONs/game.json",
    "internal_name" : "JSONs/beastie_internal_name.json",
}

OUTPUT_PATH : str = "C:/Users/MSII/Desktop/output.json"

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
    _output_files()


def _is_paths_valid() -> bool:
    for path in PATHS.values():
        if not os.path.exists(path):
            print(f"JSON at {path} doesn't exist!")
            return False
    return True


def _get_internal_name(name : str) -> str:
    if name == "":
        return ""
    if not name in dicts["internal_name"].keys():
        return ""
    return dicts["internal_name"][name]


def _get_move_ingame_name(internal_name : str) -> str:
    if internal_name == "":
        return ""
    if not internal_name in dicts["move_dict"].keys():
        return ""
    ref_text : str = dicts["move_dict"][internal_name]["name"] # type: ignore
    ref_text = ref_text.strip("Â¦")
    return dicts["all_text"][ref_text]


def _get_playdex(name : str) -> str:
    internal_name = _get_internal_name(name)
    if internal_name == "":
        return ""
    if not internal_name in dicts["beastie_data"].keys():
        return ""

    full_playdex : list[str] = dicts["beastie_data"][internal_name]["attklist"] # type: ignore
    raw_level_playdex : list[list[int, str]] = dicts["beastie_data"][internal_name]["learnset"] # type: ignore
    raw_level_no_int : list[str] = []
    level_playdex : str = ""
    from_friend_playdex : str = ""

    for list in raw_level_playdex:
        level_playdex += str(list[0]) # Level number (converted to string)
        level_playdex += ", "
        raw_level_no_int.append(list[1])
        ingame_name : str = _get_move_ingame_name(list[1]) # Move name (converted from internal name)
        level_playdex += ingame_name
        level_playdex += ", "
    level_playdex = level_playdex.rstrip(", ")

    for move_name in full_playdex:
        if not move_name in raw_level_no_int:
            ingame_name : str = _get_move_ingame_name(move_name)
            from_friend_playdex += ingame_name
            from_friend_playdex += ", "
    from_friend_playdex = from_friend_playdex.rstrip(", ")

    return f"[playbook]\nplays_level = \"{level_playdex}\"\n\nplays_extra = \"{from_friend_playdex}\""


def _load_jsons() -> None:
    for key in PATHS.keys():
        with open(PATHS[key], mode="r") as file:
            dicts[key] = json.load(file)
            

def _output_files() -> None:
    # with open(OUTPUT_PATH, mode="w") as file:
    #     json.dump(dicts["internal_name"], file, indent=4)
    for beastie in dicts["internal_name"].keys():
        print(_get_playdex(beastie))
        print("\n")


if __name__ == "__main__":
    main()