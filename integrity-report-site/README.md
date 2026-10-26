# 청렴 신고 정보조회 정적 사이트

## 반영된 원본 데이터
- `청렴신고_사건데이터.csv` 500행을 `data/reports.json`으로 변환하여 기본 탑재했습니다. 공개 조회 항목은 신고일자, 신고유형, 지역, 처리상태입니다.
- `청렴교육_현황.csv` 120행을 `data/education.json`으로 변환해 동봉했습니다. 현재 사이트에서는 교육 현황을 화면에 표시하지 않습니다.
- 입력 CSV는 UTF-8-SIG 방식으로 로드했고, 빈 값은 표시 시 '미기재'로 처리합니다.

신고 JSON 재생성:
```bash
python3 build.py --input /path/to/청렴신고_사건데이터.csv
python3 -m http.server 8000
```
브라우저에서 http://localhost:8000 으로 확인할 수 있습니다.

## 배포
- Netlify: 폴더를 Git 저장소에 커밋하고 새 사이트의 배포 원본으로 연결합니다. netlify.toml을 이용합니다.
- Vercel: 같은 저장소를 Import하고 Static Other 프레임워크를 선택합니다. vercel.json을 이용합니다.
- 매 배포 시 `build.py --refresh-news`가 시도됩니다. RSS 주소는 2026-07-01 이후 중단되어 404일 수 있으며, 스크립트는 정책브리핑 보도자료 HTML 목록 대체 수집을 시도합니다. 이 동작은 HTML 변경 또는 네트워크 차단에 영향을 받을 수 있습니다.
- 기본 `data/news.json`에는 2026-10-26 웹에서 확인한 행정안전부 보도자료 6건의 정적 스냅샷이 들어 있으며, 제목별 링크는 검증되지 않은 개별 글 대신 공식 목록 페이지로 연결됩니다.

## 주의
- 신고자 이름, 전화번호, 주소, 세부 신고내용 등 개인 식별 정보를 절대 공개 저장소 또는 클라이언트 JSON에 올리지 마세요.
- 본 사이트는 **조회 전용**이며 신고 접수나 처리상태 갱신을 제공하지 않습니다.
- 출처: https://www.korea.kr/briefing/pressReleaseList.do?pWiseMinistry=ministryNews&repCode=A00031&repCodeType=%EC%A0%95%EB%B6%80%EB%B6%80%EC%B2%98
- RSS 서비스 중단 공지: https://www.korea.kr/etc/noticeList.do
