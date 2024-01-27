# langchain 공부용

## 사용 스택
- FastAPI: 백엔드
- Next.js: 프론트엔드

## 0. 준비하기
- requirements.txt 설치
```bash
pip install -r requirements.txt
```

## 1. 챗봇 테스트 해보기

```
uvicorn main:app -p 8000
```
- http://localhost:8000 에서 테스트 가능

## 2. 주피터 노트북으로 단계별 학습하기
- `jupyter lab`을 실행하여 주피터 서버 실행
- [1. 챗봇 학습하기](1_chatbot.ipynb)
- [2. 임베딩 학습하기](2_embedding.ipynb)
- [3. RAG 학습하기](3_rag.ipynb)