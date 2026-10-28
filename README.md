# 부처별 보도자료 정적 검색 사이트

## 구성
- `index.html`: 카드, 부처·본문 검색, 결과 N건, 정합성 비교표 및 외부 Unsplash 이미지
- `보도자료데이터.json`: 사용자가 제공한 보도자료 3건 원본

## 배포
- Netlify: 사이트 추가 → Deploy manually 에 이 폴더(또는 ZIP 해제 폴더) 드래그 앤 드롭.
- Vercel: 새 프로젝트 생성 후 해당 폴더를 GitHub에 올려 import. 별도 빌드 명령 불필요(Other 프레임워크).
- 두 파일은 반드시 동일 폴더에 유지.

## 로컬 확인
`python -m http.server 8000` 을 폴더에서 실행하고 `http://localhost:8000` 접속.
`file://` 로 직접 열면 브라우저 보안 정책상 fetch가 차단될 수 있음.

## 외부 리소스
Unsplash 외부 호스팅 이미지 한 개를 `<img>`로 표시. 공식 보도자료 사진이 아닌 장식용 이미지.
Google Sheets의 공개 임베드 URL은 제공되지 않아 삽입하지 않음.
