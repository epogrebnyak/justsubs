"""Extract text blocks from VTT text.

About VTT: https://en.wikipedia.org/wiki/WebVTT

Original code from https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e
"""
import re
from collections import namedtuple
from dataclasses import dataclass
from datetime import time

Block = tuple[time, list[str]]
SegmentHeader = namedtuple("SegmentHeader", "start_time end_time styles")


def parse_segment_header(segment_header: str) -> SegmentHeader:
    _match = re.match(
        r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})(.*)", segment_header
    )
    if _match is None:
        raise ValueError("segment_header has invalid format")
    return SegmentHeader(
        time.fromisoformat(_match.group(1)),
        time.fromisoformat(_match.group(2)),
        _match.group(3).strip(),
    )


# ЕП: эта функция остается
def remove_header(lines: list[str]) -> list[str]:
    """Remove VTT file header."""
    pos = -1
    for mark in (
        "##",
        "Language: en",  # может и не 'en'
    ):
        if mark in lines:  # enumerate сюда
            pos = lines.index(mark)
    return lines[pos + 1 :]


# ЕП: эту функция разбиваем на две - достать метку времени и убрать служебные символы и теги
def remove_tags(text: str) -> str:
    """Remove VTT markup tags."""
    tags = [
        r"</c>",
        r"<c(\.color\w+)?>",
        r"<\d{2}:\d{2}:\d{2}\.\d{3}>",
    ]

    for pat in tags:
        text = re.sub(pat, "", text)

    # extract timestamp, only kep HH:MM
    text = re.sub(
        r"(\d{2}:\d{2}):\d{2}\.\d{3} --> .* align:start position:0%", r"\g<1>", text
    )

    text = re.sub(r"^\s+$", "", text, flags=re.MULTILINE)
    return text


# ЕП: этот функционал остается, функция другая
def merge_duplicates(lines: list[str]):
    """Remove duplicated subtitles. Duplacates are always adjacent."""
    last_timestamp = ""
    last_cap = ""
    for line in lines:
        if line == "":
            continue
        if re.match("^\d{2}:\d{2}$", line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


# ЕП: этот функционал остается, функция другая
def merge_short_lines(lines: list[str]):
    buffer = ""
    for line in lines:

        # эту часть видимо пропустим
        if line == "" or re.match("^\d{2}:\d{2}$", line):
            yield "\n" + line
            continue

        # накапливаем до длины строки 80?
        if len(line + buffer) < 80:
            buffer += " " + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer


def blocks_from_text(vtt_text: str) -> list[str]:
    text = remove_tags(vtt_text)
    lines = remove_header(text.splitlines())
    lines = list(merge_duplicates(lines))
    return list(merge_short_lines(lines))


def dict_from_text(vtt_text: str) -> dict[str, str]:
    return blocks_from_text(vtt_text)


@dataclass
class Segment:
    start: time
    body: str


RE_SEGMENT = r"(\d{2}:\d{2}:\d{2}\.\d{3} --> .*)\n"
RE_START = r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (.*)"


def parse_start_from_header(line):
    _match = re.match(RE_START, line)
    if _match:
        return time.fromisoformat(_match.group(1))
    return None


def yield_segments(text: str):
    for line in re.split(RE_SEGMENT, text.strip())[1:]:
        start = parse_start_from_header(line)
        if start:
            res = [start]
        else:
            res.append(line.strip())
            yield Segment(res[0], res[1])


def raw_extract(text: str) -> list[Block]:
    _split_segments = re.split(RE_SEGMENT, text.strip())[1:]
    res = [
        (
            parse_segment_header(segment_header).start_time,
            [remove_tags(_line.strip()) for _line in segment_body.strip().splitlines()],
        )
        for segment_header, segment_body in zip(
            _split_segments[::2], _split_segments[1::2]
        )
    ]
    return res


def deduplicate(blocks: list[Block]) -> list[Block]:
    prev_line = None
    for block in blocks:
        lines = block[1]
        for idx, line in list(enumerate(lines)):
            if line == prev_line:
                del lines[idx]
                continue
            prev_line = line
    return blocks


def merge(blocks: list[Block]) -> list[Block]:
    return blocks


def get_blocks(text: str) -> list[Block]:
    text = remove_header(text)  # убираем заголовок из текста
    blocks = raw_extract(text)  # разбиваем текст на блоки
    blocks = deduplicate(blocks)  # обходим блоки, убираем соседние повторы
    return merge(blocks)  # укрупняем блоки
