"""Extract text blocks from VTT text.

Original code from https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e
"""
import re
from datetime import time


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


def remove_header(lines: list[str]) -> list[str]:
    """Remove VTT file header."""
    pos = -1
    for mark in (
        "##",
        "Language: en",
    ):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos + 1 :]
    return lines


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


def merge_short_lines(lines: list[str]):
    buffer = ""
    for line in lines:
        if line == "" or re.match("^\d{2}:\d{2}$", line):
            yield "\n" + line
            continue

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


Block = tuple[time, list[str]]


def raw_extract(text: str) -> list[Block]:
    pass
