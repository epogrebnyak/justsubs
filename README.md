# justsubs

Download subtitles from YouTube as plain text

Based on [gist by glasslion](https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e)

Install (not a package yet):

```console
git clone https://github.com/epogrebnyak/justsubs.git
cd justsubs
```

List subtitle options:

```python
from justsubs import Video

video = Video("KzWS7gJX5Z8")
video.list_subs()
```

Get subtitles as plain text:

```python
from justsubs import Video

subs = Video("KzWS7gJX5Z8").subtitles(language="en-uYU-mmqFLq8")
subs.download()
print(subs.get_text_blocks()[:10])
print(subs.get_plain_text()[:550])
```
