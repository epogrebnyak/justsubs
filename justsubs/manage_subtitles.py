"""Download subtitles from YouTube videos as plain text.

Must have yt-dlp installed (pip install yt-dlp).

Alternative package is https://github.com/jdepoix/youtube-transcript-api.
"""
import subprocess
from dataclasses import dataclass
from pathlib import Path

from justsubs.manage_vtt import blocks_from_text


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
