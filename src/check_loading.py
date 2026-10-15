"""1단계 점검: 로딩 결과를 출력해 페이지 수와 첫 페이지 텍스트 순서를 눈으로 확인한다.

실행: python -m src.check_loading
"""

from collections import defaultdict

from langchain_core.documents import Document

from src.loader import load_reports

PREVIEW_CHARS = 500


def group_by_report(docs: list[Document]) -> dict[str, list[Document]]:
    """페이지 Document들을 리포트 파일명(metadata['file'])별로 묶는다. 순서는 로딩 순서 그대로."""
    groups: dict[str, list[Document]] = defaultdict(list)
    for doc in docs:
        groups[doc.metadata["file"]].append(doc)
    return groups


def print_page_counts(groups: dict[str, list[Document]]) -> None:
    """리포트별 '증권사 / 날짜 / 파일명 : N쪽' 표를 출력한다."""
    print("\n=== 리포트별 페이지 수 ===")
    for file, pages in groups.items():
        meta = pages[0].metadata
        print(f"{meta['broker']} / {meta['date']} / {file} : {len(pages)}쪽")


def print_first_page_previews(groups: dict[str, list[Document]]) -> None:
    """리포트마다 첫 페이지 본문 앞 500자를 줄바꿈을 살린 원문 그대로 출력한다."""
    print(f"\n=== 리포트별 첫 페이지 본문 앞 {PREVIEW_CHARS}자 ===")
    for file, pages in groups.items():
        first = min(pages, key=lambda d: d.metadata["page_no"])
        meta = first.metadata
        text = first.page_content[:PREVIEW_CHARS]

        print("\n" + "=" * 70)
        print(f"{meta['broker']} / {meta['date']} / {file} / p.{meta['page_no']}")
        print(f"(첫 페이지 전체 {len(first.page_content)}자)")
        print("-" * 70)
        print(text if text.strip() else "[텍스트 없음 — 스캔(이미지) PDF일 수 있음]")
    print("=" * 70)


def main() -> None:
    docs = load_reports()
    print(f"\n총 페이지 Document 수: {len(docs)}")
    if not docs:
        print("로딩된 문서가 없습니다. data/pdf/ 와 data/reports.csv의 file 컬럼을 확인하세요.")
        return

    groups = group_by_report(docs)
    print_page_counts(groups)
    print_first_page_previews(groups)


if __name__ == "__main__":
    main()
