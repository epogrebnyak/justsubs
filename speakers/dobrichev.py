from justsubs import Video

v = Video("KPmSwVr32Pc")
v.list_subs()
v.vtt("ru").download().write_text("dobrichev_ru.txt")