# 증권사 리서치 리포트 비교 RAG (개인 프로젝트)

## 목표
한 종목에 대한 여러 증권사 리포트(PDF)를 색인하고, 질문하면 증권사별로 의견을 나눠
근거(증권사/날짜/쪽)와 함께 비교 답변하는 RAG 시스템.
- 부트캠프 RAG 수업 내용을 적용하는 학습용 프로젝트
- 금융권 AI·디지털 직무 지원용 포트폴리오. 기능 개수보다
  "정량 평가 결과"와 "설계 근거·시행착오 기록"을 더 중요하게 본다

## 범위
- 종목 1~2개, 증권사 3~5곳, 리포트 10~15개
- 핵심 기능: 증권사별 의견 비교 + 출처 표시 + 문서에 없으면 "언급 없음"
- 기간: 약 2주, 팀 프로젝트와 병행 (하루 1~2시간)

## 환경
- Windows + VS Code + PowerShell, Python 3.10 이상
- 프로젝트 위치: my_llm_service/research-report-rag/
- API 키는 상위 폴더의 my_llm_service/.env 에 있다
  - load_dotenv()를 인자 없이 호출하면 find_dotenv()가 상위 폴더까지 올라가며 찾는다
  - 프로젝트 안에 .env를 새로 만들지 않는다. 키 값은 절대 출력하지 않는다(존재 여부만 확인)
- 가상환경은 프로젝트 안의 .venv
- git은 로컬에서만 사용하고, 프로젝트가 끝나면 GitHub에 push한다

## 스택 (수업과 동일하게 유지)
- LangChain: langchain-community, langchain-classic, langchain-text-splitters
- langchain-openai: ChatOpenAI(gpt-4o-mini), OpenAIEmbeddings(text-embedding-3-small)
- langchain-chroma (로컬 persist: chroma_db/), python-dotenv, pypdf
- 새 라이브러리가 필요하면 추가하기 전에 먼저 물어본다

## 폴더 구조
- data/pdf/          리포트 PDF (저작권 때문에 git 제외)
- data/reports.csv   file, broker, date, opinion, target_price (직접 작성, utf-8-sig로 읽음)
- src/loader.py      CSV 정보를 페이지별 Document.metadata에 붙여 로드 (1단계 완료)
- check_loading.py   로딩 3종 점검: 개수 / 첫 페이지 본문 / 텍스트 없는 페이지
- eval/              평가셋과 평가 스크립트 (4단계)
- docs/devlog.md     시행착오와 설계 결정 기록

## 단계 계획
1. PDF 로딩과 점검 — 2단 레이아웃으로 첫 페이지 문장 순서가 섞이는지 확인
2. 청킹과 Chroma 색인 — 색인은 저장해서 재사용. chunk_size는 평가 결과로 결정
3. 증권사별 비교 체인 — broker 필터로 증권사마다 따로 검색해서
   한 증권사가 결과를 독점하지 않게 한다. 출처 표시, "언급 없음" 처리, 터미널 CLI
4. 정량 평가 — 이 프로젝트의 핵심
   - 평가셋: 질문 20개 내외, 각 질문에 정답 리포트 파일명과 쪽 번호를 내가 직접 적는다
   - 문서에 없는 질문도 일부 포함한다(file이 비어 있는 항목)
   - 지표: 검색 hit@k(정답 쪽이 상위 k개 안에 있는지),
     거절 정확도(문서에 없는 질문에 "언급 없음"으로 답했는지), 출처 표시 정확도
   - 설정(chunk_size, k, 필터 유무)을 바꿔 가며 같은 평가셋으로 비교하고 결과를 표로 남긴다
5. README 정리 — 문제 정의, 구조, 평가 결과 표, 시행착오

이후 확장(2주 이후, 수업 진도에 맞춰): 증권사-종목-섹터-경쟁사 관계를 지식그래프로 만들어
Graph RAG로 연결, DART 공시와 리포트 전망 교차 검증

## 작업 규칙
- 한 번에 한 단계만 구현하고, 끝나면 멈춰서 내가 실행·확인할 수 있게 한다
- 코드를 짜기 전에 바꿀 파일과 이유를 먼저 짧게 보여준다
- 코드를 작성한 뒤에는 한국어로 코드 주석보다 자세히 설명한다:
  각 함수가 하는 일, 왜 이렇게 짰는지, LangChain API의 입력과 반환값
- 실행 명령어는 Windows PowerShell 기준으로 안내한다
- 외부 호출(PDF 로딩, OpenAI API)에는 최소한의 예외 처리를 넣는다
- Chroma metadata에는 None 값을 넣지 않는다
- 설계를 바꾸거나 문제를 해결하면 docs/devlog.md에 기록할 내용을 제안한다
  (형식: 날짜 / 문제 / 원인 / 해결 / 결과 수치)
- 요청하지 않은 기능(웹 UI, 로깅, 테스트 코드 등)은 만들지 말고 제안만 한다
- 각 단계가 끝나면 커밋 메시지를 제안한다
