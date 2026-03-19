"""common/pdf_reader.py 单元测试。"""

from __future__ import annotations

import fitz

from common.pdf_reader import read_pdf, read_pdf_pages


def _create_test_pdf(tmp_path, pages: list[str]) -> str:
    """辅助函数：创建包含指定页面文本的测试 PDF。"""
    pdf_path = str(tmp_path / "test.pdf")
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text, fontsize=12)
    doc.save(pdf_path)
    doc.close()
    return pdf_path


class TestReadPdf:
    """read_pdf() 测试。"""

    def test_single_page(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Hello World"])
        result = read_pdf(pdf_path)
        assert "Hello World" in result

    def test_multi_page_separated_by_double_newline(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Page one", "Page two"])
        result = read_pdf(pdf_path)
        assert "Page one" in result
        assert "Page two" in result
        # 页间应有双换行分隔
        assert "\n\n" in result

    def test_excessive_blank_lines_collapsed(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Line A\n\n\n\n\nLine B"])
        result = read_pdf(pdf_path)
        # 连续 3+ 空行应合并为 2 个换行
        assert "\n\n\n" not in result

    def test_file_not_found_raises(self):
        import pytest
        with pytest.raises(FileNotFoundError):
            read_pdf("/nonexistent/path.pdf")

    def test_returns_string(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Test"])
        result = read_pdf(pdf_path)
        assert isinstance(result, str)


class TestReadPdfPages:
    """read_pdf_pages() 测试。"""

    def test_returns_list_of_dicts(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Page 1", "Page 2"])
        result = read_pdf_pages(pdf_path)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_dict_has_page_and_text(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["Content"])
        result = read_pdf_pages(pdf_path)
        assert result[0]["page"] == 1
        assert "Content" in result[0]["text"]

    def test_page_numbers_are_sequential(self, tmp_path):
        pdf_path = _create_test_pdf(tmp_path, ["A", "B", "C"])
        result = read_pdf_pages(pdf_path)
        pages = [r["page"] for r in result]
        assert pages == [1, 2, 3]
