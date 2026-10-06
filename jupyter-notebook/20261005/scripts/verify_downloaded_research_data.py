from pathlib import Path
import csv,json,collections,struct,hashlib,shutil
ROOT=Path('C:/Coding/grad/_paper')
WORK=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'metadata/download_manifest.json').read_text(encoding='utf-8'))
for item in manifest:
    file=ROOT/item['path']
    assert hashlib.sha256(file.read_bytes()).hexdigest()==item['sha256']
dbf=next((ROOT/'data/raw/seoul_areas/extracted').glob('*.dbf'))
raw=dbf.read_bytes()
dbf_encoding=next(dbf.parent.glob('*.cpg')).read_text().strip()
num=struct.unpack_from('<I',raw,4)[0]
hlen,rlen=struct.unpack_from('<HH',raw,8)
fields=[];offset=32
while raw[offset]!=13:
    desc=raw[offset:offset+32]
    fields.append((desc[:11].split(b'\x00')[0].decode('ascii'),desc[16]))
    offset+=32
area_records=[]
for i in range(num):
    row=raw[hlen+i*rlen:hlen+(i+1)*rlen]
    if row[:1]==b'*': continue
    pos=1;record={}
    for name,width in fields:
        record[name]=row[pos:pos+width].decode(dbf_encoding).strip();pos+=width
    area_records.append(record)
code_field=next(name for name,_ in fields if name.upper()=='TRDAR_CD')
area_codes={r[code_field] for r in area_records}
reports=[]
keys={}
for kind in ['sales','stores']:
    for year in [2023,2024,2025]:
        file=ROOT/f'data/raw/seoul_{kind}/{kind}_{year}.csv'
        counts=collections.Counter();seen=set();wanted=set();missing_area=set();n=dups=0
        with file.open(encoding='cp949',newline='') as f:
            reader=csv.DictReader(f);columns=reader.fieldnames
            for row in reader:
                q=row.get('기준_년분기_코드',row.get('stdr_yyqu_cd'))
                a=row.get('상권_코드',row.get('trdar_cd'))
                ind=row.get('서비스_업종_코드',row.get('svc_induty_cd'))
                key=(q,a,ind)
                dups+=key in seen;seen.add(key);counts[q]+=1;n+=1
                if ind in ['CS100001','CS100010']:
                    wanted.add(key)
                    if a not in area_codes:missing_area.add(a)
        keys[(kind,year)]=wanted
        reports.append({'dataset':kind,'year':year,'rows':n,'columns':columns,'encoding':'cp949','quarters':dict(counts),'duplicate_keys':dups,'target_rows':len(wanted),'target_area_codes_absent_from_boundary':sorted(missing_area)})
joins=[{'year':year,'sales_keys':len(keys['sales',year]),'matched_store_keys':len(keys['sales',year]&keys['stores',year]),'store_keys_without_sales':len(keys['stores',year]-keys['sales',year])} for year in [2023,2024,2025]]
kopis_status=ROOT/'metadata/kopis_collection_status.json'
summary={'csv_files':reports,'sales_store_joins':joins,'boundary':{'records':len(area_records),'fields':[name for name,_ in fields],'prj':next(dbf.parent.glob('*.prj')).read_text(),'note':'코드 포함 여부만 검사했다. 연도별 경계 동일성·유효기간 호환성을 입증한 것은 아니다.'},'kopis':json.loads(kopis_status.read_text(encoding='utf-8')) if kopis_status.exists() else {'status':'pending_api_key','data_downloaded':False,'guide_downloaded':True}}
(ROOT/'metadata/data_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
table='\n'.join(f"| {r['dataset']} | {r['year']} | {r['rows']:,} | {r['target_rows']:,} |" for r in reports)
readme=f'''# 졸업프로젝트 연구 데이터

정리일: 2026-09-22

**서울시 핵심 자료는 확보했습니다. KOPIS 공연·공연장 원자료는 인증키 미발급으로 아직 없습니다.** 개발가이드 PDF는 데이터셋이 아닙니다.

## 확보한 파일

- `data/raw/seoul_sales/`: 2023·2024·2025년 추정매출 ZIP과 압축 해제 CSV.
- `data/raw/seoul_stores/`: 2023·2024·2025년 점포 ZIP과 압축 해제 CSV.
- `data/raw/seoul_areas/`: 공식 상권 경계 ZIP과 SHP·SHX·DBF·PRJ·CPG 구성 파일. 도형 {len(area_records):,}개.
- `docs/`: KOPIS Open API 개발가이드와 기존 연구계획서·자료 접근 안내.
- `metadata/download_manifest.json`: 출처·수집 방식·크기·SHA-256·압축 해제 목록.
- `metadata/data_inventory.json`: 연도별 행 수·열·분기·키 중복·기초 결합 검사.
- `scripts/`: 다운로드·검사에 사용한 Python 스크립트.

파일은 연구 지역을 미리 잘라내지 않은 **서울 전체 원본**입니다. 인접 자치구 공연장과의 거리 계산과 추후 표본 변경을 위해 보존했습니다. CSV는 원본 CP949 인코딩을 유지했습니다. pandas에서는 `pd.read_csv(path, encoding="cp949")`로 읽을 수 있습니다. ZIP은 원본 그대로이며 CSV 파일명만 영문으로 정리했습니다.

| 자료 | 연도 | 전체 행 수 | 한식·커피음료 목표 행 수 |
| --- | --- | ---: | ---: |
{table}

## 현재 남은 자료

`data/raw/kopis/`는 아직 비어 있습니다. KOPIS에서 인증키를 발급받으면 공연 목록·상세·공연장 위치와 선택적 상연 횟수를 수집해야 합니다. 연구 기간은 2023-2025년이지만, 기간 시작 전 개막한 장기 공연도 누락되지 않도록 날짜 필터를 확인해야 합니다.

- 공식 사이트: https://kopis.or.kr/por/main/main.do
- 키는 로컬 환경변수 `KOPIS_API_KEY` 또는 별도 설정 파일에 저장하고 공유 문서에 기록하지 않습니다.
- 공개 지역별 집계 통계는 개별 공연·시설 ID와 위치를 대체하지 못하므로 원자료 대신 넣지 않았습니다.

## 사용 전 확인

1. 매출 열 이름 `당월_매출_금액`과 달리 관측 단위는 분기입니다.
2. 매출이 제공되지 않는 키를 0원으로 채우지 않습니다.
3. 경계는 공식 페이지에 게시된 스냅샷입니다. 코드가 연결되더라도 과거 기간의 공간 범위가 동일함을 보장하지 않습니다. 연도별 경계 호환성은 추가 확인이 필요합니다.
4. `docs/`의 계획서·기존 접근 안내는 다운로드 전 작성본이므로, **현재 확보 상태는 이 README와 metadata 기록을 우선**합니다.
5. SHA-256과 ZIP 무결성, CSV 전체 읽기·분기·키 검사를 수행했습니다. 실증분석이나 공연·매출 공간 결합까지 완료한 것은 아닙니다.

## 공식 출처

- 추정매출: https://data.seoul.go.kr/dataList/OA-15572/A/1/datasetView.do
- 점포: https://data.seoul.go.kr/dataList/OA-15577/S/1/datasetView.do
- 상권영역: https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do

서울시·서울신용보증재단 자료이며 공식 페이지의 공공누리 제1유형 출처표시 조건을 따릅니다. 결과물에 자료명·기관·출처·수집 기준을 표시하세요. ZIP과 추출본은 같은 데이터의 보관 형식이므로 행 수를 더하지 않습니다.
'''
if not kopis_status.exists():
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
for name in ['download_research_data.py','download_research_supplements.py','verify_downloaded_research_data.py']:
    if (WORK/name).resolve() != (ROOT/'scripts'/name).resolve():shutil.copy2(WORK/name,ROOT/'scripts'/name)
print(json.dumps({'rows':[{k:r[k] for k in ['dataset','year','rows','target_rows','duplicate_keys']} for r in reports],'joins':joins,'boundary_records':len(area_records),'boundary_missing_codes':{f"{r['dataset']}_{r['year']}":len(r['target_area_codes_absent_from_boundary']) for r in reports},'size_bytes':sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())}))
