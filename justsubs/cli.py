import sys
from typing import Optional
from justsubs import Video

import typer

app = typer.Typer()

# TODO: add test for CLI
# TODO: add donwload-direcotry where to store files
@app.command()
def main(
    video_id: str,
    language: str = "en",  # Default subtitles
    list: bool = False,  # Show available captions and subtitles
    segments: bool = True,  # Text by small segment
):
    """Download subtitles from YouTube videos as plain text."""
    v = Video(video_id)
    if list:
        v.list_subs()
        sys.exit(0)
    subtitles = v.vtt(language)
    subtitles.download()
    print(subtitles.text())


if __name__ == "__main__":
    app()
