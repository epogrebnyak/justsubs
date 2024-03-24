from justsubs import Video, get_text

v = Video("upNWhz4w2vM")
v.list_subs()
subs = v.vtt("ru")
print(subs.cli)

subs.download()
print(subs.text())
