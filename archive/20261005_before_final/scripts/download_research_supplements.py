from pathlib import Path
import urllib.request,urllib.parse,zipfile,io,json,hashlib,datetime,shutil
from concurrent.futures import ThreadPoolExecutor
ROOT=Path('C:/Coding/grad/_paper')
WORK=Path(__file__).resolve().parent
guide='https://kopis.or.kr/upload/openApi/'+urllib.parse.quote('공연예술통합전산망OpenAPI개발가이드.pdf')
def download(item):
    name,url,body,path=item
    request=urllib.request.Request(url,data=body,headers={'User-Agent':'Mozilla/5.0','Referer':'https://data.seoul.go.kr/'})
    with urllib.request.urlopen(request,timeout=60) as response: blob=response.read()
    dest=ROOT/path
    if name=='seoul_areas':
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            assert archive.testzip() is None
            members=[]
            base=dest.parent/'extracted'
            base.mkdir(exist_ok=True)
            for member in archive.infolist():
                if member.is_dir():continue
                filename=member.filename
                if not (member.flag_bits&0x800):
                    try:filename=filename.encode('cp437').decode('cp949')
                    except (UnicodeError,LookupError):pass
                target=(base/filename).resolve()
                if not target.is_relative_to(base.resolve()):raise ValueError('Unsafe ZIP path')
                target.parent.mkdir(parents=True,exist_ok=True)
                content=archive.read(member)
                if target.exists() and target.read_bytes()!=content:raise ValueError('Existing file differs')
                target.write_bytes(content)
                members.append({'path':str(target.relative_to(ROOT)),'bytes':len(content)})
    else:
        assert blob.startswith(b'%PDF-'), 'Response was not a PDF'
        members=[]
    if dest.exists() and dest.read_bytes()!=blob:raise ValueError('Existing file differs')
    dest.write_bytes(blob)
    return {'dataset':name,'status':'available','source':url,'path':path,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'extracted':members,'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
body=urllib.parse.urlencode({'infId':'OA-15560','seq':'5','seqNo':'','infSeq':'3'}).encode()
items=[('seoul_areas','https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false',body,'data/raw/seoul_areas/areas.zip'),('kopis_api_guide',guide,None,'docs/KOPIS_OpenAPI_guide.pdf')]
records=[]
with ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(download,items):
        records.append(result);print(result['dataset'],result['bytes'],[m['path'] for m in result['extracted']],flush=True)
records[0]['source_page']='https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do'
records[0]['file_sequence']='5'
manifest=ROOT/'metadata/download_manifest.json'
existing=json.loads(manifest.read_text(encoding='utf-8'))
existing=[x for x in existing if x['dataset'] not in {r['dataset'] for r in records}]
manifest.write_text(json.dumps(existing+records,ensure_ascii=False,indent=2),encoding='utf-8')
if (WORK/'areas_download_page.html').exists(): shutil.copy2(WORK/'areas_download_page.html',ROOT/'metadata/seoul_areas_page.html')
if Path(__file__).resolve() != (ROOT/'scripts'/Path(__file__).name).resolve():
    shutil.copy2(__file__,ROOT/'scripts'/Path(__file__).name)
