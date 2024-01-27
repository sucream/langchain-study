# langchain 공부용

## 사용 스택
- FastAPI: 백엔드
- Next.js: 프론트엔드

## 0. 준비하기
- requirements.txt 설치
```bash
pip install -r requirements.txt
```

- llama-cpp-python 설치시 오류 발생하는 경우
  - requirements.txt에 있는 llama-cpp-python을 설치하면 오류가 발생하는 경우가 있습니다.
  - 이 경우, 해당 파일에서 llama-cpp-python을 삭제하고, 아래의 방법으로 설치해주세요.
    - [링크](https://github.com/abetlen/llama-cpp-python/releases/tag/v0.2.28)에서 본인 pc에 맞는 파일 다운로드
    - `pip install 해당파일.whl`로 설치

## 1. 챗봇 테스트 해보기

```
uvicorn main:app --port 8000
```
- http://localhost:8000 에서 테스트 가능

## 2. 주피터 노트북으로 단계별 학습하기
- `jupyter lab`을 실행하여 주피터 서버 실행
- [1. 챗봇 학습하기](1_chatbot.ipynb)
- [2. 임베딩 학습하기](2_embedding.ipynb)
- [3. RAG 학습하기](3_rag.ipynb)