# 예비 실험 결과 파일 안내

이 폴더는 본 연구와 구분되는 예비 실험의 CSV·JSON·그림을 모읍니다. 먼저 [실험 종합 보고서](../../reports/experiments/report.html)를 읽고, 아래 표에서 근거 파일을 찾으세요. 실행 순서와 설명은 [실험 노트북 안내](../../notebooks/experiments/README.md)에 있습니다.

실제자료 사후 탐색, 의도적 오용 시연, 효과를 주입한 모의실험을 구분합니다. 이 결과를 본 연구의 검증 결과로 사용하지 않습니다.

## 파일 번호별 찾기

| 번호 | 용도 | 먼저 볼 파일 | 표본과 검증 기록 |
|---|---|---|---|
| 01 | 측정·공간 연결·가용률·매출 정의의 실제자료 탐색 | [전체 사양 결과](01_specification_results.csv), [요약](01_summary.json) | [모형별 표본](01_model_samples.csv), [검증](01_validation.csv), [핵심상권 포함 상태](01_restored_core_areas.csv) |
| 02 | 군집 무시·고정효과 제거·행 복제·관측 선택의 의도적 시연 | [시연 결과](02_results.csv), [방법별 개수](02_counts.csv), [요약](02_summary.json) | [구현 검증](02_implementation_checks.csv), [관측 선택 기록](02_trim_selection.csv) |
| 03 | 효과를 주입한 모의실험과 영가설 보정 점검 | [모의 검출력](03_power.csv), [영가설 점검](03_null_calibration.csv), [요약](03_summary.json) | [반복별 결과](03_simulation_draws.csv), [주입 자료 예시](03_injected_example.csv), [기준선 재현 점검](03_baseline_checks.csv) |
| 04 | 실제자료 탐색 결과를 통합한 종합 보고서용 표 | [실제자료 탐색 전수 결과](04_all_real_exploratory_results.csv), [실험군별 요약](04_family_summary.csv) | 실험군별 보정과 전체 탐색 보정은 각 열의 이름 및 종합 보고서에서 구분합니다. |
| 05 | PPML 매출모형 탐색과 OLS 비교 | [PPML 결과](05_results.csv), [OLS 비교](05_ols_comparison.csv), [요약](05_summary.json) | [표본 흐름](05_sample_flow.csv), [포함 관측](05_sample_membership.csv), [제외 행](05_removed_rows.csv), [단위 검증](05_unit_checks.csv) |
| 06 | 공식 공연장 ID·현재 좌석 연결과 핵심상권 제외 사유 감사 | [감사 요약](06_summary.json), [핵심상권 요약](06_core_summary.csv), [원문 확인 대상](06_core_verification_priority.csv) | [공식 ID 확인](06_raw_ID_confirmation.csv), [좌석 가용률](06_seat_coverage.csv), [제외 사유](06_core_exclusion_causes.csv), [분기별 가용률](06_core_quarter_coverage.csv) |
| 07 | 같은 표본에서 예정회차와 현재 좌석 가중 노출 비교 | [계수 결과](07_results.csv), [요약](07_summary.json), [다중검정 집계](07_multiplicity_counts.csv) | [모형별 표본](07_model_samples.csv), [포함 관측](07_sample_membership.csv), [핵심상권 가용률](07_core_area_coverage.csv) |

## 그림과 실행 기록

- 그림: [행 복제 시연](02_replication_demo.png), [관측 선택 시연](02_trim_demo.png), [모의 검출력](03_power_heatmap.png), [PPML 계수](05_coefficient_plot.png).
- [execution_manifest.json](execution_manifest.json): 단계별 실행 상태, 소요 시간과 실행 파일 지문.
- [report_notes.json](report_notes.json): 종합 보고서의 입력 출처, 해석 범위와 검증 기록.
- [artifact.json](artifact.json): 보고서의 표·차트·본문 구성 자료.
- [delivery_receipt.json](delivery_receipt.json): 보고서 생성과 화면 검증 상태.

`*_summary.json`은 각 실험의 조건·검증·한계를 확인하는 출발점입니다. `*_sample_membership.csv`는 포함된 관측 키, `*_model_samples.csv`는 모형별 표본 기록입니다. 결측이나 미추정은 해당 파일의 상태 열과 요약을 함께 확인하세요.

## 연결된 폴더

- 분석 코드: [notebooks/experiments](../../notebooks/experiments/README.md)
- 파생 자료: `../../data/analysis/experiments/`
- 고정 계획: [실험 계획](../../metadata/experiments/lab_plan.json), [좌석 공급 탐색 계획](../../metadata/experiments/07_analysis_plan.json)
- 읽기용 HTML: [reports/experiments](../../reports/experiments/report.html)

폴더 정리 전 기록은 `../../archive/20261006_before_organization.zip`, 경로 대응표는 [이동 기록](../../metadata/organization/20261006_moves.json)에 있습니다.
