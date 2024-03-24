from justsubs import Video
# https://www.youtube.com/watch?v=INezxhqtkW0

v = Video("KPmSwVr32Pc")
v.list_subs()
v.vtt("ru").download().write_text("dobrichev_ru.txt")