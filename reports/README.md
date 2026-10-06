# reports

분석 노트북이 만든 결과 표·그림·검증 기록·HTML 보고서와 자료 수집 기록을 보관하는 폴더다. 현재 분석 결과는 `20261006/`, 이전 분석 결과는 `20261005/`, 수집 기록은 자료 제공처별 폴더에 있다. 날짜 폴더 이름은 `jupyter-notebook/`의 같은 이름 분석 폴더에 대응하며, 개별 파일의 생성일을 뜻하지 않는다.

| 폴더 | 내용 |
|---|---|
| [20261006](20261006/) | 현재 분석의 결과 표·그림·보고서. `jupyter-notebook/20261006/`이 쓰는 출력 경로 |
| [20261005](20261005/) | 이전 분석 결과 표·요약과 `figures/`, `notebooks/`, `analysis_history/`, `audit_20261005/` |
| [kopis_collection](kopis_collection/) | KOPIS 수집 회차별 기록·검증·실행 로그 |
| [seoul_collection](seoul_collection/) | 서울시 원자료 수집 검증표·프로파일·요약 |

## 주요 보고서

| 보고서 | 내용 |
|---|---|
| [수정 분석 결과](20261006/revised_quarterly/report.html) | 예정 시작회차·중심점 500m·총매출액/야간 매출액. **현재 결과** |
| [비유의성 진단](20261006/null_diagnostics/report.html) | 결과가 뚜렷하지 않은 이유를 측정·변동·표본·정밀도로 진단 |
| [기준선 분석](20261006/analysis_report/report.html) | 등록 공연 ID 수·최단거리 500m 기준선 |
| [공연 시간창 분석](20261006/time_windows/공연시간창_분석보고서.html) | 공연 종료 후 0~3시간 등 4개 시간창 |
| [이전 분석 독립감사](20261005/audit_20261005/report.html) | 회귀·공간·표본 독립감사 종합 |

HTML 보고서는 저장소를 내려받아 브라우저로 열어야 제대로 보인다. 같은 보고서를 알아보기 쉬운 이름으로 복사한 것이 [`documents/reports/`](../documents/reports/)에 있다.

---

## 20261006/ — 현재 분석 결과

### 하위 폴더

| 폴더 | 만드는 노트북 | 내용 |
|---|---|---|
| `notebooks/` | `00_전체실행` | 분석 노트북 01~08의 실행 결과 HTML |
| `figures/` | 분석 02~06 | 좌표 누락, 시설·상권 지도, 업종 제공률, 회귀 계수 그림 |
| `analysis_report/` | 보고서 01·02·03 | 기준선 보고서 `report.html`, 보고서용 표, 근거표(`evidence/`), 공연 시간 정보 점검(`time_feasibility/`) |
| `time_windows/` | 분석 09~11 | 시간창 노출·시간대 매출 검증·회귀 결과, 보고서 HTML, `execution_manifest.json` |
| `null_diagnostics/` | 보고서 04~07 | 정밀도(`inference_*`)·노출(`exposure_*`)·표본(`sample_*`) 진단과 종합 `report.html` |
| `revised_quarterly/` | 분석 12·13, 보고서 08·09 | 예정회차 데이터셋 검증(`12_*`), 수정 회귀(`13_*`), 표본 대표성(`14_*`), `report.html`, `execution_manifest.json` |
| `data_access/` | 수집 05 | 일자·시간대 매출 자료 후보·샘플 구조·검토 HTML, 이용신청 설명 초안과 문의 초안(미발송) |

### 최상위 결과 파일의 번호

최상위 파일은 이전 분석의 번호 체계를 그대로 쓴다. 그래서 파일 번호와 지금의 노트북 번호가 다를 수 있다.

| 파일 접두어 | 만드는 노트북 (`notebooks/`) | 내용 |
|---|---|---|
| `01_*` | 01 입력검증과_준비 | 고정 입력 지문 |
| `03_*` | 02 공연과_상권_연결 | 수집 범위, 노출 갱신, 공식명 충돌 |
| `04_*` | 03 연결검증 | 키·스키마·연결 방법·좌표 누락·재계산 검증 |
| `08_*` | 04 외식업_데이터셋 | 업종·지역·분기별 제공률, 값 플래그, 이전 두 업종과의 대조 |
| `09_*` | 05 외식업_고정효과분석 | **업종별 효과(`09_industry_effects.csv`)**, 결합검정, 표본, 정보집중도 |
| `10_*` | 06 GEE_보조분석 | GEE 효과, within/between 분해, 고정효과와의 비교 |
| `06_*` | 07 RDF_지식그래프 | 그래프 범위, SPARQL 질의 5개 결과, 검증 |
| `07_*` | 08 분석도구 | 도구 계약, 호출 로그, 준비 상태 |
| `05_prior_primary_reproducibility.json`, `06_prior_primary_reproducibility.json` | 05·06 | 코드 정리 전 주분석과의 수치 대조 |

번호가 없는 파일은 주로 01·02의 전처리·연결 기록이다. `panel_coverage.csv`, `source_quality.csv`, `value_flags.csv`, `preprocessing_summary.json`, `python_environment.json`은 01이, `linkage_analysis_summary.json`, `facility_coordinate_coverage.csv`, `geometry_repairs.csv`, `performances_unresolved_for_spatial_analysis.csv`는 02가 만든다. 전체 실행 기록은 `execution_manifest.json`, 최종본 검증 기록은 `release_validation.json`, 수집기 오프라인 검증은 `cli_offline_validation.json`에 있다.

---

## 20261005/ — 이전 분석 결과

[`jupyter-notebook/20261005/`](../jupyter-notebook/20261005/) 노트북 01~16의 결과다. 보관본이므로 수정하지 않는다.

| 위치 | 내용 |
|---|---|
| 최상위 `03_*`~`10_*` 등 | 이전 노트북 번호를 그대로 따른 결과 표·요약 |
| `figures/` | 매출 제공률, 분포, 추세, 회귀 그림 15개 |
| `notebooks/` | 이전 노트북 01~12의 실행 결과 HTML |
| `analysis_history/20261004_092358_9b279a/` | 이전 KOPIS 스냅샷(`20261004_092358_9b279a`) 기준으로 실행했던 분석 묶음(자료·노트북·결과) |
| `audit_20261005/` | 독립감사. `statistics/`(회귀), `exposure/`(공간·노출), `sample/`(자료·표본)와 종합 `report.html` |

## kopis_collection/ — KOPIS 수집 기록

| 파일 | 내용 |
|---|---|
| `<run_id>.json` | 회차별 실행 요약. 요청 수, 새로 받은 상세 수, HTTP 400 재시도, 종료 상태 |
| `<run_id>/` | 스냅샷을 만든 회차의 `collection_run.json`, 원문 목록 `raw_source_manifest.csv`, `snapshot_manifest.json` |
| `latest.json` | 마지막 완료 회차. 현재는 `20261004_154020_1c7d3b`(시설 1,755 · 공연 13,727, 미수집 0) |
| `cli_offline_validation.json` | 수집기 오프라인 검증 결과 |
| `worker.*` | 마지막 수집 프로세스의 상태와 로그 |

## seoul_collection/ — 서울시 수집 기록

재수집 회차 `20261004_091155_b8dd0e`의 검증표(`11_seoul_refresh_checks.csv`), 파일 프로파일, 요약이다. 36개 점검 항목을 모두 통과했다. 서울시 수집 노트북은 이후에도 이 폴더에 결과를 저장한다.

---

## 보관과 경로

2026년 10월 6일 정리에서 기존 파일의 내용과 이름은 보존했다. 현재 분석이 참조하는 `20261006/`과 KOPIS 수집 경로는 유지했다.

이전 노트북과 결과 메타데이터 안의 경로는 당시 실행 기록이다. 예전 `reports/09_industry_effects.csv`는 이제 `reports/20261005/09_industry_effects.csv`에 있다. 이전 노트북을 재실행하려면 당시 경로를 현재 구조에 맞춰 조정해야 한다.

파일별 이전·현재 위치와 SHA-256은 [이동 명세](../metadata/reports_organization_20261006.json)에 기록했다. 원자료나 통계 결과를 다시 계산하지 않고 파일 이동 전후의 해시를 비교했다.

현재 실제 위치는 `20261006/`이다. 과거 이동 명세는 당시 기록이며, 최신 경로 대응은 [`../environment/path_aliases.json`](../environment/path_aliases.json)에서 관리한다.
