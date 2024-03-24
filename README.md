# justsubs

Download subtitles from YouTube as plain text.

Pipelne:

- learn what captions or subtitles are available for a video;
- download VTT file with captions or subtitles;
- extract text from VTT.

VTT conversion based on [gist by glasslion](https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e).

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
`en-uYU-mmqFLq8` as simple `en` might not work.

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

Alternative and popular package is <https://github.com/jdepoix/youtube-transcript-api>.
