import os
import json
import csv
from pathlib import Path

PATHS : dict[str, str] = {
    "beastie_data" : "JSONs/beastie_data.json",
    "move_dict" : "JSONs/move_dic.json",
    "all_text" : "JSONs/game.json",
    "internal_name" : "JSONs/beastie_internal_name.json",
}

OUTPUT_TEXT : str = "vanilla_playdex.txt"
OUTPUT_CSV : str = "vanilla_playdex.csv"
OUTPUT_FULL : str = "Vanilla Playdex"

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

    match _get_result_type(): # Input prompt
        case 1:
            _output_text()
        case 2:
            _output_csv()
        case 3:
            _output_full()
        case _:
            print("Error: Wrong output type!")
            return


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


def _get_result_type() -> int:
    result_type : int = 0
    prompt : str = "Select output type.\n"
    prompt += "> Type \"1\" for text file.\n"
    prompt += "> Type \"2\" for csv file.\n"
    prompt += "> Type \"3\" for full mod folder.\n"
    while True:
        try:
            result_type = int(input(prompt))
            if result_type < 1 or result_type > 3:
                print("* No option for that number.")
                continue
            break
        except ValueError:
            print("* Number only please.")
    return result_type


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


def _get_playdex_list(name : str) -> list[str]:
    internal_name = _get_internal_name(name)
    if internal_name == "":
        return []
    if not internal_name in dicts["beastie_data"].keys():
        return []

    result : list[str] = [] # type: ignore
    full_playdex : list[str] = dicts["beastie_data"][internal_name]["attklist"] # type: ignore
    raw_level_playdex : list[list[int, str]] = dicts["beastie_data"][internal_name]["learnset"] # type: ignore
    raw_level_no_int : list[str] = [] # type: ignore
    level_playdex : str = ""
    from_friend_playdex : str = ""

    result.append(name)

    for list in raw_level_playdex:
        level_playdex += str(list[0]) # Level number (converted to string)
        level_playdex += ", "
        raw_level_no_int.append(list[1])
        ingame_name : str = _get_move_ingame_name(list[1]) # Move name (converted from internal name)
        level_playdex += ingame_name
        level_playdex += ", "
    level_playdex = level_playdex.rstrip(", ")
    result.append(level_playdex)

    for move_name in full_playdex:
        if not move_name in raw_level_no_int:
            ingame_name : str = _get_move_ingame_name(move_name)
            from_friend_playdex += ingame_name
            from_friend_playdex += ", "
    from_friend_playdex = from_friend_playdex.rstrip(", ")
    result.append(from_friend_playdex)

    return result 
            

def _output_text() -> None:
    output_text : str = ""
    for beastie in dicts["internal_name"].keys():
        playdex : list[str] = _get_playdex_list(beastie)
        output_text += f">> {beastie}'s Playdex <<\n"
        output_text += "[playbook]\n"
        output_text += f"plays_level = \"{playdex[1]}\"\n"
        output_text += f"plays_extra = \"{playdex[2]}\"\n"
        output_text += "\n--------------------------------------------------------\n\n"

    with open(OUTPUT_TEXT, mode="w") as file:
        file.write(output_text)
        print(f"Created {OUTPUT_TEXT}!")


def _output_csv() -> None:
    output_list : list[list[str]] = []
    for beastie in dicts["internal_name"].keys():
        playdex : list[str] = _get_playdex_list(beastie)
        output_list.append(playdex)

    with open(OUTPUT_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(output_list)
        print(f"Created {OUTPUT_CSV}!")


def _output_full() -> None:
    output_dir = Path(OUTPUT_FULL)
    output_dir.mkdir(parents=True, exist_ok=True)

    for beastie in dicts["internal_name"].keys():
        output_beastie_dir = output_dir.joinpath(beastie)
        output_beastie_dir.mkdir(parents=True, exist_ok=True)

        output_ini = output_beastie_dir.joinpath("beastie_data.ini")
        playdex : list[str] = _get_playdex_list(beastie)
        content : str = f"[basic]\nreskins = \"{beastie}\"\n\n"
        content += "[playbook]\n"
        content += f"plays_level = \"{playdex[1]}\"\n"
        content += f"plays_extra = \"{playdex[2]}\"\n"
        with open(output_ini, mode="w") as file:
            file.write(content)

    print(f"Created full mod folder!\nPutting these folders inside the pre-created mod folder (the one with config.ini)\nshould label all beasties with MOD tag but does nothing to their playdex.)")


if __name__ == "__main__":
    main()