# 증권사 리서치 리포트 비교 RAG (개인 프로젝트)

## 목표
한 종목에 대한 여러 증권사 리포트(PDF)를 색인하고, 질문하면 증권사별로 의견을 나눠
근거 쪽수와 함께 비교 답변하는 RAG 시스템. 부트캠프 RAG 수업 내용을 적용하는 학습용 프로젝트.

## 스택 (수업에서 사용한 것과 동일하게 유지)
- Python, LangChain (langchain-community, langchain-classic, langchain-text-splitters)
- langchain-openai: ChatOpenAI(gpt-4o-mini), OpenAIEmbeddings(text-embedding-3-small)
- langchain-chroma (로컬 persist), python-dotenv
- 새 라이브러리가 필요하면 추가하기 전에 먼저 물어볼 것

## 데이터
- data/pdf/ : 리포트 PDF (저작권 때문에 git에 올리지 않음 → .gitignore)
- data/reports.csv : file, broker, date, opinion, target_price (직접 작성)
- 로딩 시 CSV의 값을 각 페이지 Document.metadata에 붙인다

## 핵심 기능
- 증권사별로 따로 검색(Chroma filter: broker)해서 비교 → 한 증권사가 결과를 독점하지 않게
- 답변마다 출처 표시: "증권사 / 날짜 / p.쪽번호"
- 문서에 근거가 없으면 지어내지 말고 "언급 없음"이라고 답한다

## 작업 규칙
- 한 번에 한 단계만 구현하고, 끝나면 멈춰서 내가 확인할 수 있게 한다
- 코드를 작성한 뒤에는 한국어로 자세히 설명한다: 각 함수가 하는 일, 왜 이렇게 짰는지,
  LangChain API의 입력과 반환값
- API 키는 .env에서만 읽는다. 코드에 하드코딩하지 않는다
- 외부 호출(PDF 로딩, OpenAI API)에는 최소한의 예외 처리를 넣는다
- 요청하지 않은 기능(테스트, 로깅, 웹 UI 등)은 만들지 말고 제안만 한다
