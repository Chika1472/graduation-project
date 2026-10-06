"""Download the study's KOPIS records. Credentials stay outside the project.

Run with Python 3.11+: python download_kopis.py lists|facilities|details
Requests use HTTPS, bounded pagination, retries, and on-disk resume files.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import calendar
import collections
import csv
import datetime as dt
import hashlib
import json
import os
import threading
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/kopis'
OUT = ROOT / 'data/processed/kopis'
BASE = 'https://www.kopis.or.kr/openApi/restful/'
KEY_FILE = Path.home() / '.config/grad/kopis.env'
LOCK = threading.Lock()
NEXT_REQUEST = 0.0
KEY = ''
STOP = threading.Event()


class AccessBlocked(RuntimeError):
    pass


def load_key():
    key = os.environ.get('KOPIS_API_KEY')
    if not key and KEY_FILE.exists():
        key = KEY_FILE.read_text(encoding='utf-8-sig').strip().split('=', 1)[1]
    if not key:
        raise RuntimeError('Set KOPIS_API_KEY or create ~/.config/grad/kopis.env')
    return key.strip()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def request(endpoint, params, relative, expected='dbs'):
    global NEXT_REQUEST
    path = RAW / relative
    if path.exists():
        root = ET.fromstring(path.read_bytes())
        if root.tag != expected:
            raise RuntimeError(f'Unexpected cached XML: {relative}')
        return root
    query = urllib.parse.urlencode(dict(service=KEY, **params))
    for attempt in range(4):
        if STOP.is_set():
            raise AccessBlocked('Collection stopped after an API access/rate rejection')
        with LOCK:
            delay = max(0, NEXT_REQUEST - time.monotonic())
            NEXT_REQUEST = max(time.monotonic(), NEXT_REQUEST) + 1.0
        time.sleep(delay)
        if STOP.is_set():
            raise AccessBlocked('Collection stopped after an API access/rate rejection')
        try:
            req = urllib.request.Request(BASE + endpoint + '?' + query,
                                         headers={'User-Agent': 'GraduationResearch/1.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                blob = response.read()
            root = ET.fromstring(blob)
            if root.tag != expected:
                msg = ' '.join(root.itertext())[:300].replace(KEY, '[REDACTED]')
                raise RuntimeError(f'API {endpoint}: {root.tag}: {msg}')
            if KEY.encode() in blob:
                raise RuntimeError('Response unexpectedly contains the credential')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
            save_json(path.with_suffix('.request.json'), {
                'endpoint': BASE + endpoint, 'params_without_key': params,
                'collected_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest(),
                'path': path.relative_to(ROOT).as_posix(),
            })
            return root
        except urllib.error.HTTPError as exc:
            message = exc.read().decode('utf-8', errors='replace')
            if exc.code in (401, 403, 429) or 'Request Blocked' in message:
                STOP.set()
                raise AccessBlocked(f'API access rejected (HTTP {exc.code}); stopped without retry') from None
            error = f'HTTP {exc.code}'
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
            error = str(exc).replace(KEY, '[REDACTED]')
        if attempt < 3:
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f'{endpoint}: {error}') from None


def flat(db):
    return {e.tag: (e.text or '').strip() for e in db if len(e) == 0}


def paged(endpoint, params, folder, tag='db', root='dbs'):
    rows = []
    seen_pages = set()
    for page in range(1, 1000):
        body = request(endpoint, dict(params, cpage=page, rows=100),
                       f'{folder}/{page:03}.xml', root)
        batch = [flat(e) for e in body.findall(tag)]
        signature = json.dumps(batch, ensure_ascii=False, sort_keys=True)
        if batch and signature in seen_pages:
            raise RuntimeError(f'Repeated page in {folder}: {page}')
        seen_pages.add(signature)
        rows.extend(batch)
        if len(batch) < 100:
            return rows
    raise RuntimeError(f'Pagination exceeded 999 pages: {folder}')


def write_csv(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open('w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(name):
    with (OUT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def month_list(year, month):
    label = f'{year}{month:02}'
    params = dict(stdate=label + '01',
                  eddate=label + str(calendar.monthrange(year, month)[1]), signgucode='11')
    rows = paged('pblprfr', params, 'performance_lists/' + label)
    for row in rows:
        row['query_month'] = label
    print(f'Performances {label}: {len(rows)}', flush=True)
    return rows


def lists():
    facilities = paged('prfplc', {'signgucode': '11'}, 'facility_list')
    write_csv('facilities_list_seoul.csv', facilities)
    print(f'Seoul facilities: {len(facilities)}', flush=True)
    observations = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(month_list, year, month)
                   for year in (2023, 2024, 2025) for month in range(1, 13)]
        for future in as_completed(futures):
            observations.extend(future.result())
    observations.sort(key=lambda r: (r['query_month'], r['mt20id']))
    write_csv('performance_month_observations_seoul_2023_2025.csv', observations)
    unique = {}
    for row in observations:
        unique[row['mt20id']] = {k: v for k, v in row.items() if k != 'query_month'}
    write_csv('performances_list_seoul_2023_2025.csv', [unique[k] for k in sorted(unique)])
    save_json(ROOT / 'metadata/kopis_list_inventory.json', {
        'seoul_facilities': len(facilities), 'performance_ids': len(unique),
        'monthly_observations': len(observations),
        'months': dict(sorted(collections.Counter(r['query_month'] for r in observations).items())),
        'started_before_2023': sum(r['prfpdfrom'] < '2023.01.01' for r in unique.values()),
        'note': 'Current API snapshot, not a historical as-of archive. Monthly rows repeat long-running IDs.',
    })
    print(f'Unique Seoul performances: {len(unique)}', flush=True)


def detail_batch(ids, endpoint, folder, idkey):
    records = []
    failures = []
    def one(id_):
        root = request(endpoint + '/' + id_, {}, folder + '/' + id_ + '.xml')
        db = root.find('db')
        if db is None:
            raise RuntimeError('Empty detail response')
        row = flat(db)
        if row.get(idkey) != id_:
            raise RuntimeError('Detail ID mismatch')
        return row
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(one, id_): id_ for id_ in sorted(set(ids))}
        for n, future in enumerate(as_completed(futures), 1):
            id_ = futures[future]
            try:
                records.append(future.result())
            except Exception as exc:
                failures.append({'id': id_, 'error': str(exc).replace(KEY, '[REDACTED]')})
            if n % 100 == 0 or n == len(futures):
                print(f'{folder}: {n}/{len(futures)}, failed {len(failures)}', flush=True)
    save_json(ROOT / f'metadata/kopis_{folder}_failures.json', failures)
    records.sort(key=lambda r: r[idkey])
    return records


def facilities():
    records = detail_batch([r['mt10id'] for r in read_csv('facilities_list_seoul.csv')],
                           'prfplc', 'facility_details', 'mt10id')
    districts = {r['mt10id']: r['gugunnm'] for r in read_csv('facilities_list_seoul.csv')}
    for row in records:
        row['gugunnm'] = districts.get(row['mt10id'], '')
    write_csv('facilities_detail_seoul.csv', records)


def details():
    records = detail_batch([r['mt20id'] for r in read_csv('performance_detail_candidates.csv')],
                           'pblprfr', 'performance_details', 'mt20id')
    write_csv('performances_detail_candidates_2023_2025.csv', records)


def facility_stats():
    observations = []
    for year in (2023, 2024, 2025):
        for month in range(1, 13):
            label = f'{year}{month:02}'
            params = dict(stdate=label+'01',
                          eddate=label+str(calendar.monthrange(year, month)[1]), sharea='11',
                          cpage=1, rows=100)
            root = request('prfstsPrfByFct', params, f'facility_statistics/{label}.xml', 'prfsts')
            batch = [dict(flat(row), query_month=label) for row in root.findall('prfst')]
            observations.extend(batch)
            print(f'Facility statistics {label}: {len(batch)}', flush=True)
    write_csv('facility_statistics_seoul_monthly_2023_2025.csv', observations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['lists', 'facilities', 'details', 'facility_stats'])
    args = parser.parse_args()
    KEY = load_key()
    try:
        globals()[args.phase]()
    except Exception as exc:
        print('STOPPED:', str(exc).replace(KEY, '[REDACTED]'), flush=True)
        raise SystemExit(1) from None
