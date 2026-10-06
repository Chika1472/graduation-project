# 재현 환경

이 프로젝트는 Windows x64, Python 3.12.14 환경을 사용한다. 프로젝트 루트의 `.venv/`에 필요한 패키지를 설치했다. Python 기본 실행 환경, 보고서 생성용 Node 24.12.0, 보고서 생성기·HTML 자산과 재설치용 패키지 파일 111개를 이 폴더에 포함했다. 개인 Codex 캐시 경로에 의존하지 않는다.

## 실행

프로젝트 루트의 `start-jupyter.cmd`를 실행하고 `graduation-project (Python 3.12)` 커널을 사용한다.

- 기준선: `jupyter-notebook/20261006/00_전체실행.ipynb`
- 시간창: `jupyter-notebook/20261006/01_시간대확장_실행.ipynb`
- 현재 수정 분석: `jupyter-notebook/20261006/02_수정분석_실행.ipynb`
- 보조 실험: `jupyter-notebook/sandbox/00_전체실행.ipynb`
- 기존 결과를 보존하며 검증: `environment/verify_reproduction.ipynb`

일반 분석 실행은 해당 분석의 파생 자료와 결과를 다시 생성한다. 검증 노트북은 별도 `environment/validation-workspace/`에서 실행하며 원래 결과에 쓰지 않는다. 수집 노트북은 분석 전체 실행에 포함하지 않는다.

## 환경 재설치

다른 Windows x64 PC에서는 프로젝트 폴더 전체를 옮긴 후 루트에서 실행한다. 포함된 Python과 패키지 설치 파일을 사용하며 네트워크가 필요하지 않다.

```powershell
powershell -ExecutionPolicy Bypass -File environment/setup.ps1
```

Python 실행 파일을 직접 지정할 수도 있다.

```powershell
powershell -ExecutionPolicy Bypass -File environment/setup.ps1 -Python C:\Python312\python.exe
```

가상환경에는 절대 경로가 들어간다. 다른 위치로 프로젝트를 옮긴 경우 반드시 `setup.ps1`를 다시 실행해 포함된 Python 기준으로 `.venv`와 커널 경로를 재생성한다. 기존 패키지 파일은 유지한다. 별도 Python 설치는 필요하지 않다.

최상위 `requirements.txt`는 모든 노트북의 직접 의존성을 고정한다. `requirements-lock.txt`는 검증한 전이 의존성까지 고정한다. `nbconvert`, IPython, BeautifulSoup, requests를 직접 의존성에 추가했다. 통계 결과의 재현을 위해 검증된 버전을 유지한다. `wheels/`가 있으면 설치도 오프라인으로 수행하며, 이 폴더를 제외한 경우에만 패키지 저장소를 사용한다.

## 경로와 고정 명세

`project_paths.ipynb`는 현재 프로젝트 루트를 찾고 역사적 JSON·CSV에 적힌 경로를 해석한다. `path_aliases.json`은 이전·현재 경로 대응표다. 노트북 소스의 직접 경로는 현재 구조로 수정했다. 입력 원문, 사전 계획과 과거 결과는 수정하지 않았다.

`before_path_migration.zip`에는 수정 전 노트북과 안내 파일이 있다. `path_migration.json`은 변경 전후 해시 및 승인된 노트북 소스 해시를 기록한다. 원래 해시가 기록과 일치하는 경로 수정에만 호환 처리를 적용한다. 노트북의 실행 출력 변경은 허용하지만, 승인되지 않은 코드·설명 변경은 차단한다. 데이터·통계 결과의 해시는 대체하지 않는다. 사용자가 삭제한 KOPIS 실행기 2개는 과거 sandbox 보호 목록에서 명시적으로 제외한다.

## 보고서 생성

`report-builder/`는 기존 OpenAI Data Analytics 0.2.10-13ceeea1f599 보고서 생성기의 실행 파일과 필수 자산을 원본 그대로 포함한다. 파일별 출처와 해시는 `report-builder-provenance.json`에 있다. npm 설치는 필요하지 않다. `node/node.exe`를 노트북에서 직접 사용한다.

HTML 생성과 구조 검증은 로컬에서 수행한다. 브라우저 시각 검증은 설치된 Chromium headless shell이 있을 때 추가 수행하며, 없으면 생성기가 시각 검증 미수행을 결과에 기록한다. Chromium을 자동 다운로드하지 않는다.

## 이번 검증 결과

2026-10-06: 노트북 56개 구조·문법·초기화 검사, 실행 진입점 4개, 결과표 8개 수치 대조, 추가 보고서 7개 실행을 통과했다. 원자료·기존 결과 32,556개 파일은 변경하지 않았다. 상세 결과는 `verification-output/summary.json`에 있다.

`validation-workspace/` 및 `initialization-workspace/`는 검증용 복사본이다. 자동 승인 정책이 삭제를 차단하여 보관했다. 이 폴더는 일반 분석 입력이 아니며 Git 추적에서 제외한다. 실제 분석은 루트의 `jupyter-notebook/`를 사용한다.
