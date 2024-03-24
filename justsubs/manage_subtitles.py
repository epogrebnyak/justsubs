"""Download subtitles from YouTube as plain text.

Must have yt-dlp installed (pip install yt-dlp).
Using parts of code from https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e.
Alternative package is https://github.com/jdepoix/youtube-transcript-api.
"""
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


def get_text(video_id: str, language: str = "en") -> str:
    """Get subtitles as plain text from YouTube video."""
    return Video(video_id).vtt(language).download().text()


def get_blocks(video_id: str, language: str = "en") -> list[str]:
    """Get subtitles as list of strings from YouTube video."""
    return Video(video_id).vtt(language).download().blocks()


@dataclass
class Subtitles:
    filename: Path
    download_args: list[str]

    def download(self, force=False):
        if force or not self.filename.exists():
            subprocess.run(self.download_args)
        return self

    @property
    def cli(self):
        """Show a command for download as string."""
        return " ".join(self.download_args)


class VTT(Subtitles):
    def blocks(self) -> list[str]:
        vtt_text = self.filename.read_text(encoding="utf-8")
        return blocks_from_text(vtt_text)

    def text(self) -> str:
        return "\n".join(self.blocks())

    def write_text(self, filename):
        Path(filename).write_text(self.text(), encoding="utf-8")    


@dataclass
class Video:
    slug: str

    @property
    def url(self):
        return "https://www.youtube.com/watch?v=" + self.slug

    def list_subs(self):
        """Print available subtitles to screen."""
        return subprocess.run(["yt-dlp", "--list-subs", self.url])

    def vtt(self, language: str):
        """Create subtitles object of VTT type."""
        return self.subtitles(language, subtitles_format="vtt", cls=VTT)

    def subtitles(
        self, language: str, subtitles_format: str, cls=Subtitles
    ) -> Subtitles:
        """Create subtitles object."""
        return cls(
            filename=Path(f"{self.slug}.{language}.{subtitles_format}"),
            download_args=[
                "yt-dlp",
                self.url,
                "--sub-langs",
                language,
                "--skip-download",
                "--sub-format",
                subtitles_format,
                "--write-subs",
                "--write-auto-subs",  # save captions
                "--output",
                self.slug,
            ],
        )


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
