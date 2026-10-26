"""Build static case data from a CSV/JSON file, and refresh government news when possible.
Usage: python build.py --input reports.csv
Requires Python 3.10+; optional: pip install beautifulsoup4
"""
import argparse,csv,json,re,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parent
REPORTS=ROOT/'data/reports.json'
NEWS=ROOT/'data/news.json'
RSS='https://www.korea.kr/rss/dept_mois.xml'
LIST_URL='https://www.korea.kr/briefing/pressReleaseList.do?pWiseMinistry=ministryNews&repCode=A00031&repCodeType=%EC%A0%95%EB%B6%80%EB%B6%80%EC%B2%98'
ALIASES={'신고일자':['신고일자','신고일','접수일자','접수일'],'신고유형':['신고유형','유형','신고분류'],'지역':['지역','소재지','발생지역'],'처리상태':['처리상태','진행상태','상태']}
def normalize(rows):
 out=[]
 for i,row in enumerate(rows,1):
  if not isinstance(row,dict): raise ValueError(f'{i}번째 행은 객체가 아닙니다')
  result={name:next((str(row[k]).strip() for k in keys if k in row and row[k] is not None),'') for name,keys in ALIASES.items()}
  if not any(result.values()):continue
  out.append(result)
 return out
def import_data(path):
 p=Path(path)
 if p.suffix.lower()=='.json':
  rows=json.loads(p.read_text(encoding='utf-8-sig'))
 else:
  with p.open('r',encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not isinstance(rows,list):raise ValueError('입력 데이터는 JSON 배열이나 CSV여야 합니다')
 cleaned=normalize(rows)
 REPORTS.write_text(json.dumps(cleaned,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'신고 {len(cleaned)}건 변환 -> {REPORTS}')
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; static-integrity-site/1.0)'})
 with urllib.request.urlopen(req,timeout=15) as f:return f.read()
def refresh_news():
 # RSS is officially discontinued; try once then fall back to verified Ministry landing page.
 try:
  root=ET.fromstring(fetch(RSS))
  items=[]
  for node in root.findall('.//item'):
   title=(node.findtext('title') or '').strip();link=(node.findtext('link') or '').strip()
   if title and link.startswith('https://www.korea.kr/'):
    items.append({'title':title,'url':link,'date':(node.findtext('pubDate') or '').strip()})
  if len(items)>=5:
   NEWS.write_text(json.dumps({'source':RSS,'note':'korea.kr RSS 빌드 수집 자료','items':items[:10]},ensure_ascii=False,indent=2),encoding='utf-8');print('RSS 최신 항목 갱신');return
 except Exception as e:print(f'RSS 수집 불가: {e}')
 # This requires beautifulsoup4 and may need updating if source markup changes.
 try:
  from bs4 import BeautifulSoup
  soup=BeautifulSoup(fetch(LIST_URL),'html.parser')
  items=[];seen=set()
  for a in soup.find_all('a',href=True):
   href=urljoin(LIST_URL,a['href']); title=a.get_text(' ',strip=True)
   if 'pressReleaseView.do' not in href or not title or len(title)<12 or title in seen:continue
   # Only capture results when the list page presents actual article links.
   seen.add(title);items.append({'title':title,'url':href,'date':''})
   if len(items)>=10:break
  if len(items)>=5:
   payload={'source':LIST_URL,'note':'RSS 서비스 중단에 따라 정책브리핑 보도자료 페이지에서 빌드 시 수집한 자료입니다.','items':items}
   NEWS.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');print(f'보도자료 {len(items)}건 갱신');return
  print('보도자료 목록에서 검증 가능한 항목 5건 미만; 기존 스냅샷 유지')
 except Exception as e:print(f'보도자료 수집 불가: {e}; 기존 스냅샷 유지')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',help='신고 CSV 또는 JSON 파일 경로');ap.add_argument('--refresh-news',action='store_true');args=ap.parse_args()
 if args.input:import_data(args.input)
 if args.refresh_news:refresh_news()
