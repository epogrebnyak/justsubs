from datetime import time

import pytest

from justsubs.manage_vtt import get_blocks, raw_extract, yield_segments, Segment


from datetime import time


@pytest.mark.issue_3
def test_yield_segments():
    doc = """
00:03:17.340 --> 00:03:21.090 align:start position:0%
is coming from a different kind of
anomaly<00:03:18.340><c> if</c><00:03:18.520><c> you want</c>

00:03:21.090 --> 00:03:21.100 align:start position:0%
anomaly if you want
"""
    assert list(yield_segments(doc)) == [
        Segment(
            start=time(0, 3, 17, 340000),
            body="is coming from a different kind of\nanomaly<00:03:18.340><c> if</c><00:03:18.520><c> you want</c>",
        ),
        Segment(start=time(0, 3, 21, 90000), body="anomaly if you want"),
    ]


@pytest.mark.issue_3
def test_raw_extract_1():
    doc1 = """
00:03:01.110 --> 00:03:01.120 align:start position:0%
conventional risk premia that we know
"""
    assert raw_extract(doc1) == [
        (time(0, 3, 1, 110000), ["conventional risk premia that we know"]),
    ]


@pytest.mark.issue_3
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
            time(0, 3, 17, 340000),
            [
                "is coming from a different kind of",
                "anomaly if you want that we didn't know",
            ],
        ),
        (time(0, 3, 21, 90000), ["anomaly if you want that we didn't know"]),
    ]


@pytest.mark.skip
@pytest.mark.issue_3
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
        (
            time(0, 3, 17, 340000),
            [
                "abc",
                "def",
                "esg  50000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            ],
        ),
        (time(0, 4), ["klm klm klm"]),
    ]
