# justsubs

Download subtitles from YouTube as plain text

Based on [gist by glasslion](https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e).

2024-03-23: Tested on Windows, may fail on Linux.

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

List subtitle options:

```python
from justsubs import Video

video = Video("KzWS7gJX5Z8")
video.list_subs()
```

From the output above you will need a language slug like
`en-uYU-mmqFLq8` as simple `en` might not work.

Get subtitles as plain text:

```python
from justsubs import Video

subs = Video("KzWS7gJX5Z8").subtitles(language="en-uYU-mmqFLq8")
subs.download()
print(subs.get_text_blocks()[:10])
print(subs.get_plain_text()[:550])
```
