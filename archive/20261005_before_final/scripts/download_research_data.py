from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.parse, zipfile, hashlib, json, datetime, shutil

ROOT = Path('C:/Coding/grad/_paper')
WORK = Path(__file__).resolve().parent
for folder in ['data/raw/seoul_sales','data/raw/seoul_stores','data/raw/seoul_areas','data/raw/kopis','docs','metadata','scripts']:
    (ROOT/folder).mkdir(parents=True, exist_ok=True)

def digest(b): return hashlib.sha256(b).hexdigest()
def request(url, body=None):
    req=urllib.request.Request(url, data=body, headers={'User-Agent':'Mozilla/5.0','Referer':'https://data.seoul.go.kr/'})
    with urllib.request.urlopen(req,timeout=60) as response: return response.read()

def get_file(item):
    kind,year,inf,seq,cached=item
    dest=ROOT/f'data/raw/seoul_{kind}/{kind}_{year}.zip'
    url=f'https://data.seoul.go.kr/dataList/{inf}/S/1/datasetView.do'
    if dest.exists():
        blob=dest.read_bytes(); method='existing'
    elif cached and (WORK/cached).exists():
        blob=(WORK/cached).read_bytes(); method='previously_downloaded_official_file'
    else:
        body=urllib.parse.urlencode({'infId':inf,'seq':seq,'seqNo':'','infSeq':'3'}).encode()
        blob=request('https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false',body)
        method='downloaded'
    import io
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        assert z.testzip() is None
        members=[]
        for member in z.infolist():
            if member.is_dir(): continue
            # Preserve archive bytes; give extracted CSVs stable ASCII filenames.
            if member.filename.lower().endswith('.csv'):
                path=dest.with_suffix('.csv')
                content=z.read(member)
                if path.exists() and path.read_bytes()!=content: raise ValueError('Existing CSV differs: '+str(path))
                path.write_bytes(content)
                members.append({'archive_member':member.filename,'path':str(path.relative_to(ROOT)),'bytes':len(content),'sha256':digest(content)})
    if not dest.exists(): dest.write_bytes(blob)
    return {'dataset':kind,'year':year,'source':url,'file_sequence':seq,'status':'available','acquisition':method,'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':str(dest.relative_to(ROOT)),'bytes':len(blob),'sha256':digest(blob),'extracted':members}

items=[('sales',2023,'OA-15572','49',None),('sales',2024,'OA-15572','50',None),('sales',2025,'OA-15572','51','seoul_sales_2025_download.bin'),('stores',2023,'OA-15577','18',None),('stores',2024,'OA-15577','19',None),('stores',2025,'OA-15577','20','seoul_stores_2025.zip')]
records=[]
with ThreadPoolExecutor(max_workers=2) as pool:
    futures={pool.submit(get_file,item):item for item in items}
    for future in as_completed(futures):
        item=futures[future]
        try:
            result=future.result(); records.append(result)
            print(item[0],item[1],result['status'],result['bytes'],flush=True)
        except Exception as exc:
            records.append({'dataset':item[0],'year':item[1],'status':'failed','error':str(exc)})
            print(item[0],item[1],'FAILED',str(exc),flush=True)
manifest=ROOT/'metadata/download_manifest.json'
previous=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
kept=[r for r in previous if r['dataset'] not in ['sales','stores']]
manifest.write_text(json.dumps(kept+records,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['졸업프로젝트_연구계획서_개정안.pdf','졸업프로젝트_연구계획서_개정안.md','졸업프로젝트_상세연구계획서_개정안.pdf','졸업프로젝트_상세연구계획서_개정안.md','데이터셋_접근안내.md']:
    original=WORK.parent/'outputs'/name
    if original.exists() and not (ROOT/'docs'/name).exists(): shutil.copy2(original,ROOT/'docs'/name)
for name in ['seoul_sales_page.html','seoul_stores_page.html']:
    if (WORK/name).exists(): shutil.copy2(WORK/name,ROOT/'metadata'/name)
if Path(__file__).resolve() != (ROOT/'scripts'/Path(__file__).name).resolve():
    shutil.copy2(__file__,ROOT/'scripts'/Path(__file__).name)
print('Manifest saved',flush=True)
