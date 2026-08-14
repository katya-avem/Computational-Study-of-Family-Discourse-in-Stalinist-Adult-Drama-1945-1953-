import re
from pathlib import Path
from collections import Counter
from pprint import pprint
from transliterate import transliterate

input_folder = Path('C://Users/katya/Documents/PyCharmProjects/soviet_plays_PhD/plays_txt/Adult_Thaw_Plays').resolve()
output_folder = Path('C://Users/katya/Documents/PyCharmProjects/soviet_plays_PhD/plays_tei_raw/phd').resolve()

input_filename = "Якорная площадь.txt"
output_filename = "Якорная площадь.xml"


def find_block_between_empty_lines(lines: list, block_index: int) -> tuple:
    count = 0
    block_start_index = -1
    block_end_index = -1
    block_lines = []

    for index, line in enumerate(lines):
        if len(line.strip()) == 0:
            count += 1

            if count == block_index + 1:
                block_end_index = index
                break

            continue

        if count == block_index:
            if block_start_index == -1:
                block_start_index = index

            block_lines.append(line)

    if block_start_index != -1 and block_end_index == -1:
        block_end_index = len(lines)

    return block_start_index, block_end_index, block_lines


def mark_up_author_title(lines: list) -> list:
    block_start_index, block_end_index, block_lines = find_block_between_empty_lines(lines, 0)

    assert block_start_index == 0
    assert block_end_index != -1

    return [
        f"<docAuthor>{block_lines[0].strip()}</docAuthor>\n",
        "<docTitle>\n",
        f"<titlePart title=\"main\">{block_lines[1].strip()}</titlePart>\n",
        *[f"<titlePart title=\"sub\">{line.strip()}</titlePart>\n" for line in block_lines[2:]],
        "</docTitle>\n",
        *lines[block_end_index:]
    ]


def mark_up_cast_list(lines: list) -> list:
    block_start_index, block_end_index, block_lines = find_block_between_empty_lines(lines, 1)

    assert block_start_index != -1
    assert block_end_index != -1
    assert block_lines[0].strip() == 'ДЕЙСТВУЮЩИЕ ЛИЦА'

    head_line, *cast_lines = block_lines

    return [
        *lines[:block_start_index],
        "<castList>\n",
        f"<head>{head_line.strip()}</head>\n",
        *[f"<castItem>{line.strip()}</castItem>\n" for line in cast_lines],
        "</castList>\n",
        *lines[block_end_index:]
    ]


def mark_up_set(lines: list) -> list:
    block_start_index, block_end_index, block_lines = find_block_between_empty_lines(lines, 2)

    assert block_start_index != -1
    assert block_end_index != -1

    return [
        *lines[:block_start_index],
        "<set>\n",
        *[f"<p>{line.strip()}</p>\n" for line in block_lines],
        "</set>\n",
        *lines[block_end_index:]
    ]


def get_line_starts(acts: list) -> Counter:
    # starts = []
    #
    # for act in acts:
    #     for scene in act['scenes']:
    #         for line in scene['body']:
    #             if '.' in line:
    #                 line = line[:line.index('.')]
    #                 line = re.sub("[\(\[].*?[\)\]]", "", line)
    #                 starts.append(line.strip())
    #
    # return Counter(starts)

    lines = [line for act in acts for scene in act['scenes'] for line in scene['body']]
    lines = [line[:line.index('.')] for line in lines if '.' in line]
    lines = [re.sub("[\(\[].*?[\)\]]", "", line) for line in lines]
    lines = [line.strip() for line in lines]

    return Counter(lines)


def mark_up_scene_lines(lines: list, speakers: dict) -> list:
    lines = [{'speaker': None, 'text': line} for line in lines]

    for i in range(len(lines)):
        line = lines[i]
        line['text'] = re.sub("([\(\[](.*?)[\)\]])", "<stage>\g<1></stage>", line['text'])

        for speaker in speakers:
            if line['text'].startswith(f"{speaker}."):
                line['speaker'] = speakers[speaker]
                line['text'] = re.sub("(.*?\.)( .*)", "<speaker>\g<1></speaker>\g<2>", line['text'])

            if line['text'].startswith(f"{speaker} <stage"):
                line['speaker'] = speakers[speaker]
                line['text'] = re.sub("(.*?stage\>\.)( .*)", "<speaker>\g<1></speaker>\g<2>", line['text'])

    for i in range(len(lines) - 1):
        if lines[i]['text'].startswith('<speaker>') and lines[i + 1]['text'].startswith('<speaker>'):
            lines[i]['text'] = re.sub("(.*speaker\>) (.*)", f"<sp who=\"{lines[i]['speaker']}\">\g<1> <p>\g<2></p></sp>", lines[i]['text'])

    return [line['text'] for line in lines]


def mark_up_acts(lines: list) -> list:
    block_start_index, block_end_index, block_lines = find_block_between_empty_lines(lines, 3)

    assert block_start_index != -1
    assert block_lines[0].find('ДЕЙСТВИЕ') != -1 or block_lines[0].find('АКТ') != -1

    # -------- Get structured acts

    acts = []
    append_to_act_stage = False

    for line in block_lines:
        if line.find('ДЕЙСТВИЕ') != -1 or line.find('АКТ') != -1:
            acts.append({
                'head': line,
                'stage': [],
                'scenes': []
            })
            append_to_act_stage = True
            continue

        current_act = acts[-1]

        if line.find('ЯВЛЕНИЕ') != -1 or line.find('КАРТИНА') != -1 or line.find('СЦЕНА') != -1:
            current_act['scenes'].append({
                'head': line,
                'body': []
            })
            append_to_act_stage = False
            continue

        if append_to_act_stage:
            current_act['stage'].append(line)
        else:
            current_scene = current_act['scenes'][-1]
            current_scene['body'].append(line)

    # -------- Mark up scene lines

    line_starts = get_line_starts(acts)

    pprint(line_starts)
    speakers = list(iter(input, ""))
    speakers = {speaker: transliterate(speaker).lower().replace(' ', '_') for speaker in speakers}
    pprint(speakers)

    for act in acts:
        for scene in act['scenes']:
            scene['body'] = mark_up_scene_lines(scene['body'], speakers)

    # -------- Write outer tags

    acts_lines = []

    for act in acts:
        acts_lines.append('<div type="act">\n')
        acts_lines.append(f"<head>{act['head'].strip()}</head>\n")

        for line in act['stage']:
            acts_lines.append(f"<stage>{line.strip()}</stage>\n")

        for scene in act['scenes']:
            acts_lines.append('<div type="scene">\n')
            acts_lines.append(f"<head>{scene['head'].strip()}</head>\n")
            acts_lines.extend(scene['body']) # line = replace_braces_with_stage_tags(line)
            acts_lines.append('</div>\n')

        acts_lines.append('</div>\n')

    return [
        *lines[:block_start_index],
        *acts_lines,
        *lines[block_end_index:]
    ]


def mark_up_top_level_markup(lines: list) -> list:
    body_start_index = -1

    for (index, line) in enumerate(lines):
        if line.startswith('<div'):
            body_start_index = index
            break

    assert body_start_index != -1

    return [
        '<TEI xml:lang="rus">\n',
        '<teiHeader></teiHeader>\n',
        '<text>\n',
        '<front>\n',
        *lines[:body_start_index],
        '</front>\n',
        '<body>\n',
        *lines[body_start_index:],
        '</body>\n',
        '</text>\n',
        '</TEI>\n',
    ]


def main():
    input_filepath = input_folder / input_filename
    with open(input_filepath, encoding='utf-8') as file:
        lines = file.readlines()

    lines = mark_up_author_title(lines)
    lines = mark_up_cast_list(lines)
    lines = mark_up_set(lines)
    lines = mark_up_acts(lines)
    lines = mark_up_top_level_markup(lines)

    output_filepath = output_folder / output_filename
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.writelines(lines)


if __name__ == '__main__':
    main()
