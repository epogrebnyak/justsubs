from justsubs import Video

v = Video("gBnLl3QBOdM")
v.list_subs()
v.vtt("en").download().write_text("sarno_en.txt")
v.vtt("ru").download().write_text("sarno_ru.txt")
