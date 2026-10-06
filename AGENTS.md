# 졸업프로젝트 작업 규칙

## 작업 위치와 연구 범위

- 현재 프로젝트 루트는 `C:\Coding\graduation-project`이다. 아래 경로는 별도 표시가 없으면 이 루트 기준이다. 이전 `C:\Coding\졸업프로젝트` 폴더를 현재 작업 대상으로 사용하지 않는다.
- 기본 연구 범위는 종로구·마포구, 공개 상권자료의 외식업 10종 전체, 2023~2025년 분기 자료이다. 분석 단위는 상권 × 업종 × 분기이다.
- 현재 분석은 `jupyter-notebook/20261006/`, 독립 실험은 `jupyter-notebook/sandbox/`에서 관리한다. 실험 폴더에서는 해당 폴더의 `AGENTS.md`도 따른다.
- `jupyter-notebook/20261005/`와 `reports/20261005/`는 이전 작업 보관본이다. 보관본을 수정하거나 이전 `scripts/`의 `.py` 파일을 확장하지 않는다.

## 코드와 실행 순서

- 새 분석·전처리·시각화·데이터 수집 코드는 모두 Jupyter Notebook(`.ipynb`)으로 저장한다. 별도 `.py` 분석 소스를 새로 만들지 않는다.
- 한국어 Markdown 설명 → 짧은 코드 셀 → 표·그래프 → 해석 순서로 작성한다. 새 커널에서 위에서 아래로 실행 가능해야 한다.
- 분석 코드는 `jupyter-notebook/20261006/notebooks/`, 보고서·진단 코드는 `jupyter-notebook/20261006/report-notebooks/`, 수집 관련 코드는 `jupyter-notebook/20261006/data-collection/`에서 관리한다.
- 분석 전체 실행에는 수집을 포함하지 않는다. 분석 노트북은 네트워크 요청 없이 고정된 로컬 입력으로 실행한다.

| 용도 | 실행 노트북 | 실행 순서 |
|---|---|---|
| 기초 입력·기존 기준선 | `jupyter-notebook/20261006/00_전체실행.ipynb` | `notebooks/`의 01 → 08 |
| 시간창 확장 | `jupyter-notebook/20261006/01_시간대확장_실행.ipynb` | `notebooks/`의 09 → 11 |
| 현재 분기 수정 분석 | `jupyter-notebook/20261006/02_수정분석_실행.ipynb` | `notebooks/`의 12 데이터셋 → 13 분석 → `report-notebooks/`의 09 표본 진단 → 08 보고서 |
| 독립 실험 | `jupyter-notebook/sandbox/00_전체실행.ipynb` | 01 → 02 → 03 → 05 → 06 → 07 → 04 |
| 기존 결과 보존·재현 검증 | `environment/verify_reproduction.ipynb` | 별도 검증 작업 폴더에서 실행·수치 대조 |

## 입력·결과와 경로 관리

- `dataset/raw/`는 원본 보관용이며 기존 파일을 수정하지 않는다. 최종 분석의 파생 자료는 `dataset/analysis/final/`, 결과는 `reports/20261006/`에 저장한다. 읽기용 보고서는 `documents/reports/`에 있다.
- 기존 기준선·시간창 결과와 이전 결과는 보존한다. 일반 실행 노트북은 해당 분석의 파생 자료·결과를 다시 쓰므로, 재현 점검은 `environment/verify_reproduction.ipynb`의 별도 작업 폴더에서 수행한다. 새 분석 결과는 기존 결과를 덮어쓰지 않는 별도 경로로 구분한다.
- 최종 분석은 `jupyter-notebook/20261006/metadata/`의 검증된 고정 입력 명세와 사전 분석 계획을 사용한다. 공용 최신 수집 정보로 자동 교체하거나 수집 중인 CSV를 직접 읽지 않는다.
- 이전 두 업종 기준선의 계산 검증에는 `dataset/analysis/baseline_two_industry/`의 고정 입력을 사용한다.
- 2026-10-06 이관에서 기존 노트북의 경로와 환경 연결을 수정했다. 과거 입력 명세·결과 파일에 남은 경로는 기록 그대로 보존하고 `environment/project_paths.ipynb`와 `environment/path_aliases.json`으로 현재 위치에 대응시킨다.
- 새 코드에 이전 루트, 개인 캐시 또는 사용자별 절대 경로를 넣지 않는다. 기존 노트북의 공통 경로 초기화를 따르고 `PROJECT_ROOT` 및 `project_path(...)`를 사용한다. 과거 경로가 담긴 JSON은 공통 `project_json_loads(...)`로 읽는다.
- 경로 변경 기록은 `environment/path_migration.json`, 이관 전 소스는 `environment/before_path_migration.zip`에 있다. 검증 실패를 없애기 위해 원본 해시를 일괄 갱신하지 않는다. 의도한 소스·문서 변경만 검토 후 변경 후 해시에 반영하며, 변경 전 해시와 데이터·통계 결과 해시는 유지한다.
- `environment/validation-workspace/`, `environment/initialization-workspace/`, `environment/verification-output/`은 검증용 복사본·산출물이다. 현재 분석 입력이나 편집 대상으로 사용하지 않는다.

## 재현 환경

- 프로젝트의 `.venv/Scripts/python.exe`와 `graduation-project (Python 3.12)` 커널을 사용한다. JupyterLab은 루트의 `start-jupyter.cmd`로 실행한다.
- Windows x64용 Python 3.12.14, Node 24.12.0, 패키지 설치 파일과 보고서 생성기가 `environment/`에 포함되어 있다. 보고서 생성은 `environment/node/node.exe`와 `environment/report-builder/`를 사용하며 개인 Codex 캐시에 의존하지 않는다.
- 프로젝트를 옮겼거나 환경을 재생성할 때는 폴더 전체를 보존한 뒤 루트에서 `powershell -ExecutionPolicy Bypass -File environment/setup.ps1`를 실행한다. `.venv`와 커널에 절대 경로가 있으므로 이동 후 설정을 다시 실행한다.
- 루트 `requirements.txt`가 직접 의존성의 기준이고, `environment/requirements-lock.txt`가 전이 의존성까지 고정한다. `jupyter-notebook/20261006/requirements.txt`는 루트 파일을 참조한다.
- 의존성을 변경하면 직접 의존성·잠금 파일·오프라인 설치 파일의 일치를 확인하고 영향을 받는 분석을 검증한다. 재현에 사용한 통계 패키지를 이유 없이 최신 버전으로 올리지 않는다.
- 포함된 런타임·보고서 생성기 원본은 분석 코드와 구분한다. 교체가 필요하면 관련 출처·해시 기록도 갱신한다. 상세 설치·검증 방법은 `environment/README.md`를 따른다.
- 변경 범위에 맞춰 노트북 구조·문법, 영향받는 셀 또는 실행 진입점과 결과를 확인한다. 문서만 바뀐 경우 경로·안내의 일관성을 확인하며 전체 분석을 다시 실행할 필요는 없다.

## 수집과 인증 정보

- 사용자 확인에 따라 KOPIS 다운로드는 완료되었고 관련 다운로드 실행 파일은 삭제되었다. 삭제된 실행기를 누락 파일로 취급하거나 자동 복구하지 않는다. 남은 수집 노트북을 분석·환경 점검 과정에서 실행하지 않는다.
- 새 수집은 사용자가 요청한 경우에만 수행한다. 재수집 원문은 `dataset/raw/`의 새 회차 폴더에 추가하고 기존 고정 입력은 자동 교체하지 않는다.
- 새 KOPIS 수집을 명시적으로 요청받으면 기존 사용자 지정 호출 규칙을 유지한다. 정상 호출 간격은 1초, HTTP 400은 3초 뒤 같은 ID로 재시도하며 성공 또는 사용자 중지까지 반복한다. 그 외 API 접근 차단 응답이 발생하면 요청을 중단한다.
- 인증키는 프로젝트 외부 설정 또는 환경변수에서 읽고, 노트북 소스·출력·공유 파일에 포함하지 않는다.

## 분석과 해석 원칙

- 미제공 매출을 0원으로 채우지 않는다. 실제 제공된 0원과 결측을 구분한다. 분기 자료를 일별 자료로 해석하지 않는다.
- 공연·시설의 공식 ID 연결과 시설명 임시 연결을 구분한다. 좌표 미수집과 현재 경계 사용의 한계를 결과에 표시한다.
- 점포는 일반·프랜차이즈·전체로 구분한다. `store_count`가 남아 있으면 일반점포의 호환용 별칭이다. 일반점포 0·프랜차이즈 양수인 행을 점포 부재나 오류로 해석하지 않는다. 매출 모집단 확인 전에는 점포당 매출을 해석하지 않는다.
- 예정 시작회차·시간창 노출을 실제 회차나 관객 수로 해석하지 않는다. 관측된 관련성을 인과효과로 단정하지 않는다.
- 사전 고정한 분석 계획을 유지하고 p값에 따라 사양을 선택하지 않는다. 비유의·미추정 결과, 표본 제외 사유와 다중검정 범위를 함께 보고한다. 독립 실험 결과를 본 연구의 검증 결과로 자동 반영하지 않는다.
