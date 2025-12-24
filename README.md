# 사주 PDF 생성 서버

WeasyPrint 기반 HTML → PDF 변환 서버

## 배포 방법 (Render)

1. 이 저장소를 GitHub에 푸시
2. [Render](https://render.com) 접속
3. New → Web Service
4. GitHub 저장소 연결
5. 자동 배포 완료!

## API 사용법

### PDF 생성 (파일 다운로드)

```javascript
const response = await fetch('https://your-server.onrender.com/generate-pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        html: '<html><body><h1>사주 리포트</h1></body></html>',
        filename: 'report.pdf'
    })
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
window.open(url);
```

### PDF 생성 (Base64 반환)

```javascript
const response = await fetch('https://your-server.onrender.com/generate-pdf-base64', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        html: '<html><body><h1>사주 리포트</h1></body></html>'
    })
});

const data = await response.json();
// data.pdf_base64에 PDF 데이터 (Base64)
```

## 로컬 테스트

```bash
# Docker 사용
docker build -t saju-pdf .
docker run -p 5000:5000 saju-pdf

# 또는 직접 실행 (WeasyPrint 의존성 필요)
pip install -r requirements.txt
python app.py
```
