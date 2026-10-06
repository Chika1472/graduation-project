# dataset

연구에 쓰는 모든 자료가 모여 있는 폴더다. 수집한 원문을 그대로 보관하는 `raw/`, 원문을 표로 펼친 `processed/`, 분석 노트북이 만든 패널·연결표를 담은 `analysis/`의 세 층으로 나뉜다.

자료는 항상 **raw → processed → analysis** 방향으로만 만들어진다. 아래 단계의 파일을 고치기 위해 위 단계의 원문을 수정하는 일은 없다.

> [!IMPORTANT]
> `raw/`는 읽기 전용이다. 기존 파일을 수정하거나 덮어쓰지 않고, 다시 수집한 자료는 새 회차 폴더로 추가한다. 분석 노트북은 네트워크 요청 없이 이 폴더를 읽기만 하며, 어떤 회차를 쓸지는 [`jupyter-notebook/20261006/metadata/`](../jupyter-notebook/20261006/metadata/)의 고정 입력 명세가 정한다.

## 한눈에 보기

```text
dataset/
├── raw/                        수집 원문 (읽기 전용)
│   ├── kopis/                  KOPIS Open API 1차 수집 원문
│   ├── kopis_recollection/     KOPIS 상세 재수집 회차 9개
│   ├── seoul_sales/            서울시 추정매출-상권 2023~2025
│   ├── seoul_stores/           서울시 점포-상권 2023~2025
│   ├── seoul_areas/            서울시 영역-상권 경계 (shapefile)
│   ├── seoul_recollection/     서울시 원자료 재수집 회차
│   ├── time_sales_access/      일자·시간대 매출 자료 확보 검토 원문
│   └── legacy_downloads/       초기 탐색 단계 다운로드 보관본
├── processed/
│   └── kopis/                  KOPIS 원문을 펼친 중간 CSV 12개
└── analysis/
    ├── final/                  현재 분석(20261006)의 파생 자료  ← 지금 쓰는 곳
    ├── baseline_two_industry/  두 업종 기준선 고정 입력 (읽기 전용)
    ├── kopis_snapshots/        검증을 마친 KOPIS 분석 스냅샷
    ├── kopis_collection/       수집기가 통합한 KOPIS 상세 CSV
    ├── knowledge_graph/        이전 분석의 RDF 그래프
    └── *.csv                   이전 분석(20261005)의 파생 자료
```

| 층 | 누가 만드나 | 지금 분석에서의 역할 |
|---|---|---|
| `raw/` | 수집 노트북·이전 수집 스크립트 | 모든 계산의 출발점. 해시로 고정 |
| `processed/` | 이전 수집 단계 | KOPIS 목록·후보·거리의 중간표. 연결 검증에 사용 |
| `analysis/final/` | `jupyter-notebook/20261006/notebooks/` | 현재 분석의 입력과 결과 패널 |
| `analysis/` 나머지 | 이전 분석·수집 노트북 | 고정 스냅샷, 기준선, 이전 결과 보존 |

---

## raw/ — 수집 원문

### KOPIS 응답의 저장 방식

KOPIS 응답은 모두 **XML 원문 + `.request.json` 한 쌍**으로 저장했다. `.request.json`에는 호출한 엔드포인트, 인증키를 뺀 요청 변수, 수집 시각(UTC), 바이트 수와 SHA-256이 들어 있다. **인증키는 어느 파일에도 저장하지 않았다.** `.request.json` 안의 `path`는 수집 당시 경로(`data/raw/...`)이며, 현재 위치(`dataset/raw/...`)와의 대응은 [`environment/path_aliases.json`](../environment/path_aliases.json)이 관리한다.

### `kopis/` — 1차 수집 (2026-10-03~04)

| 폴더 | 내용 | 원문 수 |
|---|---|---|
| `performance_lists/YYYYMM/` | 서울(`signgucode=11`) 월별 공연 목록. 100건 단위 페이지 | 36개월, XML 383개 |
| `facility_list/` | 서울 공연시설 목록 페이지 | XML 18개 (시설 1,755곳) |
| `facility_details/` | 시설 상세(`FC…`). 주소·위경도·좌석 규모·공연장 수 | XML 1,511개 |
| `performance_details/` | 공연 상세(`PF…`). 일정 문구·러닝타임·시설 ID | XML 195개 |
| `facility_statistics/` | 공연시설·공연장별 월 통계 (2023-01~2025-12) | XML 36개 |
| `probe/` | 응답 구조를 확인하려고 보낸 시험 호출 | XML 4개 |

1차 수집은 시설 상세 1,511개, 공연 상세 195개를 받은 뒤 API 접근 차단으로 멈췄다(`../metadata/kopis_collection_status.json`). 나머지 상세는 아래 재수집 회차에서 채웠다.

### `kopis_recollection/<run_id>/` — 상세 재수집

1차 수집에서 빠진 시설·공연 상세를 회차별 폴더에 추가했다. 기존 원문은 건드리지 않는다. 회차별 실행 기록은 [`reports/kopis_collection/`](../reports/kopis_collection/)에 있다.

| 회차 | 시설 상세 | 공연 상세 | 종료 상태 |
|---|---:|---:|---|
| `20261004_084931_94f7dc` | – | 1 | 1건 제한 시험 실행 |
| `20261004_085253_11064a` | 204 | – | API 접근 차단으로 중단 |
| `20261004_091713_d06862` | 40 | 93 | API 접근 차단으로 중단 |
| `20261004_092358_9b279a` | – | 659 | API 접근 차단으로 중단 |
| `20261004_094229_d83a34` | – | 22 | API 접근 차단으로 중단 |
| `20261004_094252_180604` | – | 28 | API 접근 차단으로 중단 |
| `20261004_094340_81fed6` | – | 52 | API 접근 차단으로 중단 |
| `20261004_153201_a288ce` | – | 32 | 사용자 중지 |
| **`20261004_154020_1c7d3b`** | – | **12,645** | **완료. 현재 분석의 고정 회차** |

1차 수집과 재수집을 합치면 시설 상세 **1,755개**(1,511 + 204 + 40), 후보 공연 상세 **13,727개**(195 + 13,532)다. 이것은 연구 상권 주변 후보 공연의 상세를 모두 받았다는 뜻이며, 서울 전체 공연 30,047건의 상세를 모두 받았다는 뜻은 아니다.

### 서울시 상권분석서비스 원자료

| 폴더 | 출처 | 파일 |
|---|---|---|
| `seoul_sales/` | [추정매출-상권 OA-15572](https://data.seoul.go.kr/dataList/OA-15572/A/1/datasetView.do) | `sales_2023~2025.csv` + 내려받은 `.zip` |
| `seoul_stores/` | [점포-상권 OA-15577](https://data.seoul.go.kr/dataList/OA-15577/S/1/datasetView.do) | `stores_2023~2025.csv` + `.zip` |
| `seoul_areas/` | [영역-상권 OA-15560](https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do) | `areas.zip`, 압축을 푼 shapefile(`extracted/`, 상권 1,650개) |
| `seoul_recollection/20261004_091155_b8dd0e/` | 위 세 자료의 재수집 | `sales/`, `stores/`, `areas/`, 당시 안내 페이지 `source_pages/` |

원자료는 서울 전역·전체 업종 단위로 받았고, 종로구·마포구와 외식업 10종(`CS100001`~`CS100010`)은 분석 노트북에서 고른다. 재수집 회차 `20261004_091155_b8dd0e`는 36개 검증 항목을 모두 통과했고, CSV 내용이 기존 원본과 같음을 확인했다(`../reports/seoul_collection/`). 상권 경계는 **현재 버전**이며 과거 분기의 경계와 같다는 보장은 없다.

### `time_sales_access/<run_id>/` — 일자·시간대 매출 자료 검토

공연 직후 몇 시간의 매출을 볼 수 있는 자료를 찾기 위해 서울시 빅데이터캠퍼스의 공개 문서를 모은 폴더다.

- `20261005_052652_803257`: 자료 카탈로그(B042·B079), 캠퍼스 이용 안내, 데이터 설명서·반출 정책 PDF
- `20261005_052911_f98e59`: 위 문서 + 공개 가공 샘플 CSV 4개(`*_PUBLIC_SAMPLE.csv`)

실제 매출 원자료는 받지 않았고(캠퍼스 내부 분석 자료), **샘플은 실제 매출 분석에 쓰지 않는다.** 검토 결과는 [`reports/20261006/data_access/`](../reports/20261006/data_access/)에 있다.

### `legacy_downloads/`

연구 초기에 내려받은 2022년 매출, 2025년 매출·점포 파일과 매출 샘플, 자료 구조 프로파일(`verified_dataset_profile.json`)이다. 현재 분석에는 쓰지 않으며, 옮긴 기록은 `../metadata/legacy_download_migration.json`에 있다.

---

## processed/kopis/ — KOPIS 중간표

KOPIS 원문을 CSV로 펼치고 연구 상권과의 거리로 상세 수집 후보를 고른 결과다. 1차 수집 시점의 상태를 담고 있으므로 `pending_*` 목록은 이후 재수집으로 모두 해소됐다.

| 파일 | 행 | 내용 |
|---|---:|---|
| `performances_list_seoul_2023_2025.csv` | 30,047 | 2023~2025년 서울 공연 목록 (공연 ID 단위) |
| `performance_month_observations_seoul_2023_2025.csv` | 36,559 | 월별 목록 관측. 장기 공연은 여러 달에 반복된다 |
| `facilities_list_seoul.csv` | 1,755 | 서울 공연시설 목록 |
| `facilities_detail_seoul.csv` | 1,511 | 1차 수집 시설 상세 (좌표 포함) |
| `venue_area_links_800m.csv` | 9,234 | 연구 상권 800m 안의 시설–상권 거리, 300·500·800m 여부 |
| `performance_detail_candidates.csv` | 13,727 | 상세를 받을 후보 공연 (대상 구 또는 상권 800m 이내 시설) |
| `performance_detail_excluded_by_location.csv` | 16,320 | 위치 기준으로 후보에서 뺀 공연 |
| `performances_detail_candidates_2023_2025.csv` | 195 | 1차 수집 공연 상세 |
| `facility_statistics_seoul_monthly_2023_2025.csv` | 8,078 | 월별 공연시설 통계 |
| `facility_statistics_duplicate_name_keys.csv` | 2 | 통계에서 시설·공연장 이름이 중복된 행 |
| `pending_facility_details.csv` | 244 | 1차 수집 중단 시점의 미수집 시설 |
| `pending_performance_details.csv` | 13,532 | 1차 수집 중단 시점의 미수집 공연 |

---

## analysis/ — 분석용 파생 자료

### `final/` — 현재 분석

[`jupyter-notebook/20261006/`](../jupyter-notebook/20261006/)의 실행 노트북이 다시 만드는 폴더다. 연구 범위는 **종로구·마포구 151개 상권 × 외식업 10종 × 2023~2025년 12분기**다.

| 파일 | 행 | 만드는 노트북 | 내용 |
|---|---:|---|---|
| `study_areas.csv` | 151 | 01 | 연구 대상 상권 |
| `sales_stores_panel.csv` | 3,624 | 01 | 두 업종(한식·커피) 매출·점포 패널. 연결 검증용 |
| `performance_facility_linkage.csv` | 30,047 | 02 | 공연–시설 연결. 공식 상세 ID 13,727건, 시설명 임시 연결 16,320건 |
| `performance_facility_quarter.csv` | 31,988 | 02 | 공연 × 시설 × 분기 |
| `venue_area_distances_800m.csv` | 10,493 | 02 | 시설–상권 폴리곤 최단거리 |
| `area_performance_quarter.csv` | 1,812 | 02 | 상권 × 분기의 300·500·800m 등록 공연 수 |
| `performance_sales_panel.csv` | 3,624 | 02 | 두 업종 패널 + 공연 노출 |
| `food_industry_catalog.csv` | 10 | 04 | 외식업 10종과 업종별 매출·점포 제공률 |
| **`food_industry_panel.csv`** | **18,120** | 04 | **외식업 10종 기본 패널** (151 × 10 × 12) |
| `knowledge_graph/` | – | 07 | `ontology.ttl`(개념·규칙), `knowledge_graph.ttl`(부분 그래프) |
| `time_windows/` | – | 09·10 | 공연 시간창 분석 자료 (아래 표) |
| `revised_quarterly/` | – | 12 | 예정회차 수정 분석 자료 (아래 표) |

<details>
<summary><b>time_windows/ · revised_quarterly/ 파일 보기</b></summary>

| 파일 | 행 | 내용 |
|---|---:|---|
| `time_windows/nominal_sessions.csv` | 135,362 | 일정 문구로 만든 예정 회차와 추정 종료시각 |
| `time_windows/availability.csv` | 1,812 | 상권 × 분기의 일정 가용률 |
| `time_windows/area_quarter_timebin_exposure.csv` | 10,872 | 6개 매출 시간대별 공연 전후 시간창 노출 |
| `time_windows/sales_time_panel.csv` | 108,720 | 6개 시간대 매출 패널 (151 × 10 × 12 × 6) |
| `revised_quarterly/area_centroids.csv` | 151 | 상권 중심점 (EPSG:5181, 미터) |
| `revised_quarterly/facility_area_links.csv` | 4,999 | 중심점·최단거리 기준 시설–상권 연결 |
| `revised_quarterly/performance_schedule_audit.csv` | 12,839 | 공연별 일정 문구·러닝타임 파싱 결과 |
| `revised_quarterly/performance_quarter_schedule.csv` | 14,202 | 공연 × 분기 예정 시작회차 |
| `revised_quarterly/area_quarter_exposure.csv` | 3,624 | 상권 × 분기 × 공간정의별 노출과 가용률 |
| `revised_quarterly/revised_quarterly_panel.csv` | 18,120 | 수정 분석 패널 |

</details>

### 패널에서 자주 쓰는 열

| 열 | 뜻 | 주의할 점 |
|---|---|---|
| `area_id`, `industry_id`, `quarter` | 상권 × 업종 × 분기 키 | 분석 단위. 일대일 결합만 허용 |
| `total_sales`, `night_sales` | 분기 총매출, 21~24시 매출(원) | **미제공은 결측으로 둔다.** 0원으로 채우지 않는다 |
| `sales_record_present` | 원자료에 매출 행이 있었는지 | 실제 0원과 미제공을 구분하는 기준 |
| `regular_store_count`, `franchise_store_count`, `total_store_count` | 일반·프랜차이즈·전체 점포 | `store_count`는 일반점포의 호환용 별칭 |
| `positive_sales_zero_regular_stores` | 일반점포 0인데 매출이 있는 행 | 프랜차이즈만 있는 경우. 오류가 아니다 |
| `known_performance_count_300m/500m/800m` | 분기와 기간이 겹치는 등록 공연 ID 수 | 실제 회차·관객 수가 아니다 |
| `night_share`, `weekend_share` | 야간·주말 매출 비중 | 수정 분석에서는 기술통계로만 쓴다 |

### 그 밖의 폴더

| 폴더·파일 | 내용 |
|---|---|
| `baseline_two_industry/` | 처음 계획한 두 업종 기준선의 고정 입력과 결과(`05_interaction_results.csv` 등). 계산 검증용이며 **읽기 전용** |
| `kopis_snapshots/<run_id>/` | 수집본을 원문과 대조해 고정한 `facility_details.csv`·`performance_details.csv`. `20261004_154020_1c7d3b`(시설 1,755 · 공연 13,727)가 현재 분석의 입력 |
| `kopis_collection/` | 수집기가 통합한 최신 상세 CSV와 미수집 목록(현재 0건). 분석은 이 폴더를 직접 읽지 않고 스냅샷을 읽는다 |
| `knowledge_graph/` | 이전 분석(20261005)의 RDF 그래프 |
| `*.csv` (최상위) | 이전 분석(20261005)이 만든 패널·연결표. `industry_interaction_panel.csv`는 이전 05 노트북의 업종 상호작용 패널 |

최상위 CSV와 `knowledge_graph/`는 이전 분석의 결과로 보존한다. 현재 분석은 `final/`만 쓰고 읽는다.

---

## 자료를 다룰 때의 약속

- **미제공 매출을 0원으로 채우지 않는다.** 원자료에 실제로 0원이 적힌 값만 0으로 둔다.
- **분기 자료를 일별 자료로 나누지 않는다.** 시간대 매출도 분기 합계의 6개 구간일 뿐이다.
- 공연–시설 연결은 **공식 ID 연결**과 **시설명 임시 연결**을 구분한다. 연구 범위 부분 그래프에는 공식 연결만 쓴다.
- 시설 좌표와 상권 경계는 수집 시점의 현재 값이다. 과거 분기에 그대로 적용한다는 한계를 결과에 함께 적는다.
- 매출 모집단을 확인하기 전에는 점포당 매출을 만들지 않는다.
- 파일 줄바꿈과 바이트는 해시 검증에 쓰이므로 `.gitattributes`에서 변환을 끄고 그대로 보존한다.
