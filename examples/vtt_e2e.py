from justsubs import Video

# List subtitle options, find out "en-uYU-mmqFLq8" from there
video = Video("KzWS7gJX5Z8")
video.list_subs()

# Download subtitles
subs = Video("KzWS7gJX5Z8").vtt(language="en-uYU-mmqFLq8")
subs.download()

# Print subtitles as plain text
print(subs.get_text_blocks()[:10])
print(subs.text()[:550])
