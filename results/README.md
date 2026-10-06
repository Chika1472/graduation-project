# 계산 결과와 검증 기록

읽는 보고서는 [reports](../reports/index.html)에 있습니다. 이 폴더는 재현·추가 계산에 쓰는 CSV·JSON·그림을 보관합니다.

| 위치 | 내용 |
|---|---|
| `main/baseline/` | 기초 연결·외식업 데이터 검증, 고정효과·GEE, RDF·분석 도구 결과 |
| `main/revised_quarterly/` | 현재 분기 예정회차 분석의 효과 추정·표본 진단 |
| `main/time_windows/` | 공연시간과 시간대 매출 연결·회귀 결과 |
| `main/null_diagnostics/` | 비유의성의 노출·표본·추론 진단 |
| `main/analysis_report/` | 기준선 보고서용 집계표·근거 |
| `main/data_access/` | 추가 자료 확보 검토표 |
| `experiments/` | 실제자료 탐색·의도적 오용·합성 실험 결과 |
| `collection/` | 수집 진행·검증·실행 로그 |
| `audits/` | 과거 감사표와 검증 기록 |
| `legacy/` | 이전 버전의 결과표 |

`*_effects.csv`는 효과 추정, `*_sample*.csv`는 표본, `*_checks.csv`는 검증, `*_summary.json`은 해당 실행의 가정·범위·출처입니다. `artifact.json`은 HTML 보고서 생성용 데이터이고, `execution_manifest.json`은 실제 실행 이력입니다.
