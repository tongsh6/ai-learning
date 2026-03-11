import pytest

from common.text_splitters import chunk_by_fixed_length, chunk_by_paragraph, chunk_by_sliding_window


def test_chunk_by_fixed_length_keeps_tail_chunk():
    chunks = chunk_by_fixed_length("abcdefghij", chunk_size=4)

    assert chunks == ["abcd", "efgh", "ij"]



def test_chunk_by_fixed_length_rejects_non_positive_size():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_by_fixed_length("abc", chunk_size=0)



def test_chunk_by_paragraph_filters_empty_blocks():
    text = "第一段\n\n\n\n 第二段 \n\n第三段"

    chunks = chunk_by_paragraph(text)

    assert chunks == ["第一段", "第二段", "第三段"]



def test_chunk_by_sliding_window_generates_overlap():
    chunks = chunk_by_sliding_window("abcdefghij", window_size=4, overlap=1)

    assert chunks == ["abcd", "defg", "ghij", "j"]



def test_chunk_by_sliding_window_rejects_invalid_overlap():
    with pytest.raises(ValueError, match="overlap"):
        chunk_by_sliding_window("abc", window_size=3, overlap=3)
