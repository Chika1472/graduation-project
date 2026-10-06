# metadata

자료를 **언제, 어디서, 어떻게** 받았고 무엇을 확인했는지 남겨 둔 공용 기록 폴더다. 수집 매니페스트, 원자료 점검 요약, 파일 이관 기록이 들어 있다. 모두 JSON이며 사람이 읽을 수 있는 형태로 저장했다.

> [!NOTE]
> 이 폴더는 **수집 쪽의 공용 기록**이다. 현재 분석이 실제로 읽는 고정 입력 명세는 [`jupyter-notebook/20261006/metadata/`](../jupyter-notebook/20261006/metadata/)에 따로 있다. 새로 수집해서 이 폴더의 최신 기록이 바뀌어도 분석 입력은 자동으로 바뀌지 않는다.

## 파일 안내

### 서울시 상권 자료

| 파일 | 내용 |
|---|---|
| `download_manifest.json` | 첫 다운로드 13건의 기록. 매출·점포 2023~2025, 상권 영역, KOPIS 개발가이드와 KOPIS 목록·상세 파일의 출처 URL, 파일 순번, 바이트, SHA-256, 상태(`available`·`partial`) |
| `data_inventory.json` | 원자료 점검 요약. 연도별 CSV 행·열, 매출–점포 키 결합 결과, 상권 경계 shapefile의 레코드 수(1,650)·필드·좌표계, KOPIS 수집 상태 |
| `seoul_recollection/20261004_091155_b8dd0e/manifest.json` | 서울시 원자료 재수집 회차의 매니페스트. 요청 변수, 원본 해시, 대상 범위(종로구·마포구, 2023~2025, `CS100001`~`CS100010`), 경계 버전 주의 |
| `seoul_refresh_latest.json` | 가장 최근 재수집 회차를 가리키는 기록. 지금은 위 회차와 내용이 같다 |
| `seoul_analysis_sources.json` | 분석 입력으로 검증한 서울시 회차 명세. 현재 분석의 고정본과 같은 내용 |
| `seoul_sales_page.html` 외 2개 | 서울 열린데이터광장의 매출·점포·영역 자료 안내 페이지 저장본 |

### KOPIS 공연 자료

| 파일 | 내용 |
|---|---|
| `kopis_download_manifest.json` | 1차 수집 원문 2,145건의 요청 기록. 엔드포인트, 인증키를 뺀 요청 변수, 수집 시각, 바이트, SHA-256 |
| `kopis_collection_status.json` | 1차 수집의 종료 상태. 목록·시설 목록·월 통계는 완료, 시설 상세 1,511건·공연 상세 195건에서 접근 차단으로 중단. 인증키가 프로젝트에 없음을 기록 |
| `kopis_validation.json` | 1차 원문 검증 결과. 공연 ID 30,047개, 월 관측 36,559건, 36개월 전체 포함, 중복 0건 |
| `kopis_list_inventory.json` | 공연 목록 요약. 서울 시설 1,755곳, 월별 공연 수, 2023년 이전에 시작한 공연 170건 |
| `kopis_spatial_inventory.json` | 공간 연결 요약. 대상 상권 151개, 좌표가 있는 시설 1,511곳, 상권 800m 안 시설 741곳, 시설–상권 관계 9,234건, 좌표계 가정(EPSG:4326 → EPSG:5181) |
| `kopis_analysis_sources.json` | 분석 입력으로 검증한 KOPIS 회차(`20261004_154020_1c7d3b`) 명세. 현재 분석의 고정본과 같은 내용 |

재수집 회차별 실행 기록은 [`reports/kopis_collection/`](../reports/kopis_collection/)에 있다.

### 이관과 정리 기록

| 파일 | 내용 |
|---|---|
| `migration_manifest.json` | 초기 작업 폴더에서 프로젝트로 파일 4,347개를 옮긴 기록. 파일별 상대 경로·바이트·SHA-256과 일치 확인 결과 |
| `legacy_download_migration.json` | 초기 다운로드 5개를 `dataset/raw/legacy_downloads/`로 옮긴 기록 |
| `notebook_completion_audit.json` | 초기 노트북 단계의 완료 점검. 파일 이동·해시, `.ipynb` 전용 코드, 새 커널 실행, 매출 결측 보존(827행)과 당시의 한계 |
| `reports_organization_20261006.json` | 2026-10-06 `reports/` 정리 기록. 보존 490개, 이동 222개 파일의 이전·현재 경로와 SHA-256 |

## 읽을 때 알아 둘 점

- **경로는 기록 당시의 것이다.** 파일 안의 `data/raw/...`, `reports/final/...` 같은 경로나 Windows 절대 경로는 수정하지 않고 그대로 둔다. 현재 위치는 [`environment/path_aliases.json`](../environment/path_aliases.json)과 `environment/project_paths.ipynb`의 `project_json_loads(...)`가 해석한다.
- **해시는 바꾸지 않는다.** 검증이 실패하더라도 기록된 SHA-256을 일괄 갱신하지 않는다. 의도한 소스·문서 변경만 `environment/path_migration.json`에서 추적한다.
- **인증키는 어디에도 없다.** KOPIS 요청 기록은 키를 뺀 변수만 남긴다.
