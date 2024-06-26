# justsubs

Download subtitles from YouTube as plain text.

## Quick try

```console
pip install justsubs
justsubs gBnLl3QBOdM --list
justsubs gBnLl3QBOdM > sarno.txt
justsubs --help
```

## Pipeline

1. Decide what captions or subtitles are available for a video;
2. Download [VTT file](https://en.wikipedia.org/wiki/WebVTT);
3. Extract text from VTT[^1].

[^1]: VTT conversion based on [gist by glasslion](https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e).


## Install

```console
pip install justsubs
```

Latest:

```console
git clone https://github.com/epogrebnyak/justsubs.git
cd justsubs
pip install -e .
```

## Usage

### 1. List subtitle options

```python
from justsubs import Video

video = Video("KzWS7gJX5Z8")
video.list_subs()
```

From the output above you may need a language identifier like
`en-uYU-mmqFLq8`, default is `en`.

### 2. Download subtitles

```python
subtitles = Video("KzWS7gJX5Z8").vtt(language="en-uYU-mmqFLq8")
subtitles.download()
```

### 3. Print subtitles as plain text

```python
print(subtitles.text()[:500])
```

### Entire pipeline

```python
from justsubs import get_text

text = get_text(video_id="KzWS7gJX5Z8", language="en-uYU-mmqFLq8")
print(text[:500])
```

## Alternatives

- Popular package for Youtube subtitles is <https://github.com/jdepoix/youtube-transcript-api>.
- [Whisper](https://github.com/openai/whisper) allows to do speech recognition locally.
