"""Download subtitles from YouTube as plain text.
 
Using parts of code from https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e
"""
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Job:
    filename: Path
    args: list[str]

    def download(self, force=False):
        if force or not self.filename.exists():
            subprocess.run(self.args, shell=True)

    def get_text_blocks(self):
        vtt_text = self.filename.read_text()
        return get_plain_blocks(vtt_text)

    def get_plain_text(self):
        return "\n".join(self.get_text_blocks())


@dataclass
class Video:
    slug: str

    @property
    def url(self):
        return "https://www.youtube.com/watch?v=" + self.slug

    def list_subs(self):
        subprocess.run(["yt-dlp", "--list-subs", self.url], shell=True)

    def subtitles(self, language, subs_format="vtt") -> Job:
        return Job(
            filename=Path(f"{self.slug}.{language}.vtt"),
            args=[
                "yt-dlp",
                self.url,
                "--sub-langs",
                language,
                "--skip-download",
                "--sub-format",
                subs_format,
                "--write-subs",
                "--output",
                self.slug,
            ],
        )


def remove_tags(text):
    """
    Remove vtt markup tags
    """
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


def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for mark in (
        "##",
        "Language: en",
    ):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos + 1 :]
    return lines


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
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


def merge_short_lines(lines):
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


def get_plain_blocks(vtt_text: str):
    text = remove_tags(vtt_text)
    lines = remove_header(text.splitlines())
    lines = list(merge_duplicates(lines))
    return list(merge_short_lines(lines))
