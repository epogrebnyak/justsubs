from justsubs import Video, get_blocks, get_text


def test_list_subs_completes():
    video = Video("KzWS7gJX5Z8")
    assert video.list_subs().returncode == 0


def test_get_text_blocks_on_vtt_file():
    subs = Video("KzWS7gJX5Z8").vtt(language="en-uYU-mmqFLq8")
    subs.download()
    assert (
        subs.blocks()[1]
        == "THE SERGEANT AT ARMS: MADAM  SPEAKER, THE VICE PRESIDENT AND"
    )


def test_get_text():
    assert get_text("KzWS7gJX5Z8", "en-uYU-mmqFLq8")


def test_get_text_blocks_on_vtt_file_on_non_latin_captions():
    assert get_blocks("upNWhz4w2vM", "ru")[2][:25] == "раз магистратура цифровые"
