import json
from pprint import pprint
from pathlib import Path
from collections import defaultdict
from lxml import etree

MALE_CHARACTERS_FILENAME = "./male_characters.json"
FEMALE_CHARACTERS_FILENAME = "./female_characters.json"

INPUT_FILES_PATH = (Path('.') / 'source').resolve()
OUTPUT_FILES_PATH = (Path('.') / 'output').resolve()


def check_duplicate_characters(groups):
    print()

    characters_files = defaultdict(set)

    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            characters_files[character_id].add((text_name, group_name))

    for character_id, character_items in characters_files.items():
        if len(character_items) > 1:
            print(f"WARNING: character {character_id} is used more than once - {character_items}")



def check_files(speech_by_text_by_character, groups):
    print()

    all_files = set(speech_by_text_by_character.keys())
    used_files = set([text_name for group_name in groups for text_name, _ in groups[group_name]])

    diff = set(used_files) - set(all_files)
    if len(diff):
        raise Exception(f"ERROR: files {diff} are not present")

    diff = set(all_files) - set(used_files)
    if len(diff) > 0:
        print(f"WARNING: files {diff} are not used!")


def check_characters(speech_by_text_by_character, groups):
    print()

    characters_by_text_in_groups = defaultdict(set)
    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            characters_by_text_in_groups[text_name].add(character_id)

    characters_by_text_in_files = defaultdict(set)
    for text_name, speech_by_character in speech_by_text_by_character.items():
        characters_by_text_in_files[text_name] = set(speech_by_character.keys())

    for text_name in characters_by_text_in_groups:  # characters_by_text_in_groups.keys() is supposed to be subset of characters_by_text_in_files.keys()
        diff = characters_by_text_in_groups[text_name] - characters_by_text_in_files[text_name]
        if len(diff) > 0:
            raise Exception(f"ERROR: characters {diff} are not present in {text_name}")

        diff = characters_by_text_in_files[text_name] - characters_by_text_in_groups[text_name]
        if len(diff) > 0:
            print(f"WARNING: file {text_name} has unused characters {diff}")


def parse_text(file):
    parser = etree.XMLParser(encoding='utf-8', recover=True)  # consider remove_blank_text=True
    tree = etree.parse(file, parser=parser)
    etree.strip_elements(tree, 'stage', 'speaker', with_tail=False)  # with_tail=False is crucial! TODO: describe why

    speech_by_character = defaultdict(list)

    for item in tree.iter('sp'):
        who = item.get('who')
        if not who:
            print(etree.tostring(item, encoding='utf-8').decode('utf-8'))
        etree.strip_tags(item, 'l', 'lg', 'p')

        text = (item.text or '').strip()
        speech_by_character[who].append(text)

    return speech_by_character


def parse_texts():
    speech_by_text_by_character = {}

    for file in INPUT_FILES_PATH.iterdir():
        if file.is_file() and file.name.endswith('.xml'):
            speech_by_text_by_character[file.name] = parse_text(file)

    return speech_by_text_by_character


def main(groups):
    speech_by_text_by_character = parse_texts()

    check_duplicate_characters(groups)
    check_files(speech_by_text_by_character, groups)
    check_characters(speech_by_text_by_character, groups)

    speech_by_group = defaultdict(list)

    for group_name in groups:
        for text_name, character_id in groups[group_name]:
            speech_by_group[group_name].extend(
                speech_by_text_by_character[text_name][character_id]
            )

    if not OUTPUT_FILES_PATH.exists():
        OUTPUT_FILES_PATH.mkdir()

    for group_name in groups:
        file_path = OUTPUT_FILES_PATH / f"{group_name}.txt"

        with file_path.open(mode='w', encoding='utf-8') as file:
            file.writelines(speech_by_group[group_name])


if __name__ == '__main__':
    with open(MALE_CHARACTERS_FILENAME, encoding='utf-8') as male_characters_file:
        male_characters_data = json.load(male_characters_file)
        # print(male_characters_data)

    with open(FEMALE_CHARACTERS_FILENAME, encoding='utf-8') as female_characters_file:
        female_characters_data = json.load(female_characters_file)
        # print(female_characters_data)

    groups = {
        'male': [(play_name, character_id) for play_name, male_characters in male_characters_data.items() for [character_id, comment] in male_characters],
        'female': [(play_name, character_id) for play_name, female_characters in female_characters_data.items() for [character_id, comment] in female_characters]
    }

    main(groups)
