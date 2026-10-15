"""1단계: reports.csv의 메타데이터를 읽고, PDF를 페이지 단위 Document로 로딩한다."""

import csv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = PROJECT_ROOT / "data" / "pdf"
CSV_PATH = PROJECT_ROOT / "data" / "reports.csv"

REQUIRED_COLUMNS = {"file", "broker", "date", "opinion", "target_price"}


def read_report_table(csv_path: Path = CSV_PATH) -> list[dict]:
    """reports.csv를 읽어 리포트별 메타데이터 dict 리스트로 돌려준다."""
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"reports.csv에 필요한 컬럼이 없습니다: {sorted(missing)}")

        rows = []
        for row in reader:
            row = {k: (v or "").strip() for k, v in row.items()}
            # Chroma 메타데이터는 str/int/float/bool만 허용 → 목표주가는 int로 변환
            try:
                row["target_price"] = int(row["target_price"].replace(",", ""))
            except ValueError:
                row["target_price"] = 0  # 값이 비었거나 숫자가 아니면 0 = 미기재
            rows.append(row)
    return rows


def load_reports(pdf_dir: Path = PDF_DIR, csv_path: Path = CSV_PATH) -> list[Document]:
    """CSV에 적힌 PDF를 하나씩 로딩해, 각 페이지 Document에 CSV 메타데이터를 붙인다."""
    docs: list[Document] = []

    for row in read_report_table(csv_path):
        pdf_path = pdf_dir / row["file"]
        if not pdf_path.exists():
            print(f"[건너뜀] 파일 없음: {pdf_path.name}")
            continue

        try:
            pages = PyPDFLoader(str(pdf_path)).load()
        except Exception as e:  # 손상/암호화된 PDF 등
            print(f"[건너뜀] 로딩 실패: {pdf_path.name} ({e})")
            continue

        for page in pages:
            page.metadata.update(
                {
                    "file": row["file"],
                    "broker": row["broker"],
                    "date": row["date"],
                    "opinion": row["opinion"],
                    "target_price": row["target_price"],
                    # PyPDFLoader의 page는 0부터 시작 → 출처 표기용 1부터 시작하는 번호
                    "page_no": page.metadata.get("page", 0) + 1,
                }
            )
        docs.extend(pages)
        print(f"[로딩] {row['broker']} / {row['date']} / {pdf_path.name}: {len(pages)}쪽")

    return docs


if __name__ == "__main__":
    documents = load_reports()
    print(f"\n총 {len(documents)}개 페이지 Document")
    if documents:
        first = documents[0]
        print("첫 페이지 메타데이터:", first.metadata)
        print("첫 페이지 본문 앞부분:", first.page_content[:200].replace("\n", " "))
