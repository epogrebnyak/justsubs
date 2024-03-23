from justsubs import Video

# List subtitle options
video = Video("KzWS7gJX5Z8")
video.list_subs()

# Get subtitles
subs = Video("KzWS7gJX5Z8").subtitles(language="en-uYU-mmqFLq8")
subs.download()
print(subs.get_text_blocks()[:10])
print(subs.get_plain_text()[:550])
