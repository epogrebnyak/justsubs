from justsubs import Video


def test_list_subs_completes():
    video = Video("KzWS7gJX5Z8")
    assert video.list_subs().returncode == 0


def test_get_text_blocks():
    subs = Video("KzWS7gJX5Z8").subtitles(language="en-uYU-mmqFLq8")
    subs.download()
    assert (
        subs.get_text_blocks()[1]
        == "THE SERGEANT AT ARMS: MADAM  SPEAKER, THE VICE PRESIDENT AND"
    )
