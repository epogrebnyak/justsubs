from datetime import time

from justsubs.manage_vtt import get_blocks, raw_extract


def test_raw_extract_1():
    doc1 = """
00:03:01.110 --> 00:03:01.120 align:start position:0%
conventional risk premia that we know
"""
    assert raw_extract(doc1) == [
        time(0, 3, 1, 110),
        ["conventional risk premia that we know"],
    ]


def test_raw_extract_2():
    doc2 = """
00:03:17.340 --> 00:03:21.090 align:start position:0%
is coming from a different kind of
anomaly<00:03:18.340><c> if</c><00:03:18.520><c> you</c><00:03:18.700><c> want</c><00:03:19.410><c> that</c><00:03:20.410><c> we</c><00:03:20.650><c> didn't</c><00:03:20.980><c> know</c>

00:03:21.090 --> 00:03:21.100 align:start position:0%
anomaly if you want that we didn't know
"""
    assert raw_extract(doc2) == [
        (
            time(0, 3, 17, 340),
            [
                "is coming from a different kind of",
                "anomaly if you want that we didn't know",
            ],
        ),
        (time(0, 3, 21, 90), ["anomaly if you want that we didn't know"]),
    ]

def test_get_blocks():
    doc3 = """
WEBVTT
Kind: captions
Language: en

00:03:17.340 --> 00:03:21.090
abc
def              

00:03:21.090 --> 00:03:21.100
def  
esg  50000000000000000000000000000000000000000000000000000000000000000000000000000000000000

00:04:00.000 --> 00:04:21.100
klm klm klm
"""
    assert get_blocks(doc3) == [
        (time(0, 3, 17, 340), ["abc", "def", "esg  50000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]),
        (time(0, 4), ["klm klm klm"])
        ]