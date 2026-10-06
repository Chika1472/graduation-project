# 분석 결과와 수집 기록

현재 분석 결과는 `20261006/`, 이전 분석 결과는 `20261005/`, 수집 기록은 자료 제공처별 폴더에 보관한다. 날짜 폴더는 `jupyter-notebook/20261005/`의 이전 분석 단계에 대응하며, 개별 파일의 생성일을 뜻하지 않는다.

| 폴더 | 내용 |
|---|---|
| [20261006](20261006/) | 현재 분석의 결과 표·그림·보고서. `jupyter-notebook/20261006/`에서 사용하는 출력 경로 |
| [20261005](20261005/) | 이전 분석 결과 표·요약과 `figures/`, `notebooks/`, `analysis_history/`, `audit_20261005/` |
| [kopis_collection](kopis_collection/) | KOPIS 수집 회차별 기록·검증·실행 로그 |
| [seoul_collection](seoul_collection/) | 서울시 원자료 수집 검증표·프로파일·요약 |

## 주요 보고서

- [수정 분석 결과](20261006/revised_quarterly/report.html)
- [비유의성 진단](20261006/null_diagnostics/report.html)
- [기준선 분석](20261006/analysis_report/report.html)
- [공연 시간창 분석](20261006/time_windows/공연시간창_분석보고서.html)
- [이전 분석 독립감사](20261005/audit_20261005/report.html)

## 보관과 경로

2026년 10월 6일 정리에서 기존 파일의 내용과 이름은 보존했다. 현재 분석이 참조하는 `20261006/`과 KOPIS 수집 경로는 유지했다. 서울시 수집 노트북은 이후 `seoul_collection/`에 결과를 저장한다.

이전 노트북과 결과 메타데이터 안의 경로는 당시 실행 기록이다. 예전 `reports/09_industry_effects.csv`는 이제 `reports/20261005/09_industry_effects.csv`에 있다. 이전 노트북을 재실행하려면 당시 경로를 현재 구조에 맞춰 조정해야 한다.

파일별 이전·현재 위치와 SHA-256은 [이동 명세](../metadata/reports_organization_20261006.json)에 기록했다. 원자료나 통계 결과를 다시 계산하지 않고 파일 이동 전후의 해시를 비교했다.

현재 실제 위치는 `20261006/`입니다. 과거 이동 명세는 당시 기록이며 최신 경로 대응은 `../environment/path_aliases.json`에서 관리합니다.
