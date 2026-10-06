# 기초 분석 결과 파일 안내

입력 검증, 공연·상권 연결, 외식업 데이터셋, 고정효과·GEE 분석, RDF와 분석 도구의 기초 결과를 모은 폴더입니다. 읽는 문서는 [기준선 분석 보고서](../../../reports/main/baseline/report.html), 재현 방법은 [본 분석 실행 안내](../../../notebooks/main/README.md)에서 확인하세요.

현재 분기 수정 분석은 [별도 보고서](../../../reports/main/revised_quarterly/report.html)와 `../revised_quarterly/`에 있습니다. 아래 번호는 결과 파일의 접두어이며 노트북 번호와 항상 일치하지 않습니다.

## 파일 번호별 찾기

| 접두어 | 용도 | 먼저 볼 파일 | 세부 확인 파일 |
|---|---|---|---|
| 01 | 고정 입력 파일 지문 | [고정 입력 지문](01_fixed_input_fingerprints.csv) | 원본 경로와 SHA 확인에 사용합니다. |
| 03 | 수집 범위·입력 출처·목록과 상세 기간 대조 | [입력 출처](03_input_sources.csv), [수집 범위](03_collection_coverage.csv) | [목록·상세 기간 비교](03_list_detail_period_comparison.csv), [공식 명칭 충돌](03_official_name_conflicts.csv), [노출 수정 기록](03_exposure_revisions.csv) |
| 04 | 연결·좌표·공간 거리·노출 구성 검증 | [감사 요약](04_audit_summary.json), [검증 항목](04_validation_checks.csv) | [입력 무결성](04_input_integrity.csv), [연결 방법](04_link_methods.csv), [분기별 좌표 누락](04_missing_coordinates_by_quarter.csv), [노출 재구성](04_exposure_reconstruction.csv), [기초 표본 흐름](04_base_model_sample_flow.csv) |
| 05 | 이전 기준 결과 재현 기록 | [이전 기본 분석 재현](05_prior_primary_reproducibility.json) | 기존 기준과의 대조 기록입니다. |
| 06 | RDF 지식그래프 구성·검증·질의 결과 | [지식그래프 요약](06_knowledge_graph_summary.json), [개체 수](06_entity_counts.csv), [검증](06_validation.csv) | [출처 명세](06_source_manifest.csv), [그래프 범위](06_graph_coverage.csv), [분기별 공연 질의](06_q5_area_quarter_performances.csv) |
| 07 | 분석 도구의 입력·출력 규약과 실행 기록 | [도구 준비 상태](07_tool_readiness_summary.json), [도구 규약](07_tool_contracts.json) | [규약 검증](07_contract_checks.csv), [호출 기록](07_tool_call_log.jsonl), [실행 예시](07_example_result.json) |
| 08 | 외식업 10종 범위·입력 품질·공통 표본 | [업종 범위 메타데이터](08_food_scope_metadata.json), [업종별 범위](08_industry_coverage.csv), [검증](08_validation_checks.csv) | [공통 표본 범위](08_common_sample_scope.csv), [입력 품질](08_source_quality.csv), [입력 지문](08_source_fingerprints.csv), [점포 규모·매출 가용률](08_store_size_sales_coverage.csv) |
| 09 | 고정효과 분석의 계수·표본·추론 검증 | [분석 요약](09_analysis_summary.json), [업종별 계수](09_industry_effects.csv) | [모형별 표본](09_model_samples.csv), [포함 관측](09_model_sample_membership.csv), [FWL 검증](09_fwl_validation.csv), [공동 검정](09_omnibus_tests.csv), [정보 집중도](09_information_concentration.csv) |
| 10 | GEE 보조 분석과 고정효과 결과 비교 | [GEE 요약](10_gee_analysis_summary.json), [업종별 계수](10_gee_industry_effects.csv), [고정효과·GEE 비교](10_fe_gee_comparison.csv) | [표본 흐름](10_gee_sample_flow.csv), [포함 관측](10_gee_sample_membership.csv), [진단](10_gee_diagnostics.csv), [구현 검증](10_gee_implementation_checks.csv), [표본 키 대조](10_fe_gee_sample_key_checks.csv) |

## 번호가 없는 공통 기록

- 전처리와 연결: [전처리 요약](preprocessing_summary.json), [연결 분석 요약](linkage_analysis_summary.json), [공연 연결 방법](performance_link_methods.csv), [시설 좌표 가용률](facility_coordinate_coverage.csv).
- 자료 품질: [열별 결측](source_column_missingness.csv), [원자료 품질](source_quality.csv), [패널 결측](panel_missingness.csv), [패널 범위](panel_coverage.csv), [확인 대상 행](flagged_panel_rows.csv).
- 실행과 검증: [실행 기록](execution_manifest.json), [실행 환경](python_environment.json), [최종본 검증](release_validation.json), [수집 CLI 오프라인 검증](cli_offline_validation.json).

## 그림과 관련 폴더

그림 원본은 `figures/`에 있습니다. [외식업 10종 기본 결과](figures/09_외식업10종_기본결과.png), [민감도 분석](figures/09_외식업10종_민감도.png), [고정효과·GEE 계수 비교](figures/10_fe_gee_coefficients.png), [업종별 자료 범위](figures/08_food_industry_coverage.png)를 각 분석의 표·요약과 함께 확인하세요.

- 분석 코드: `../../../notebooks/main/analysis/`
- 본 분석용 파생 자료: `../../../data/analysis/final/`
- 고정 입력과 계획: `../../../metadata/main/`
- 읽기용 보고서: [기준선 보고서](../../../reports/main/baseline/report.html), [보고서 목록](../../../reports/index.html)
- 정리 전 기록: `../../../archive/20261006_before_organization.zip`, [이동 대응표](../../../metadata/organization/20261006_moves.json)

일반·프랜차이즈·전체 점포를 구분합니다. `store_count`가 남아 있으면 일반점포의 호환용 별칭이며, 매출 모집단 확인 전에는 점포당 매출로 해석하지 않습니다. 미제공 매출을 0원으로 채우지 않고, 분기 자료를 일별 자료로 해석하지 않습니다.
