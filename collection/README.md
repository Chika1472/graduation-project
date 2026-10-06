# 원자료 수집과 검증

분석 전체 실행과 분리한 수집 도구다. 노트북은 프로젝트 루트 또는 이 폴더에서 실행한다. 수집을 켜지 않은 기본 실행과 실제 API 수집을 구분한다.

| 도구 | 용도와 실행 조건 |
| --- | --- |
| `01_KOPIS_상세수집.ipynb` | KOPIS CLI 런타임. `KOPIS_수집기.cmd`를 더블클릭하면 메뉴가 열린다. |
| `02_서울시_원자료수집.ipynb` | 기본은 기존 수집 기록의 오프라인 검증. 새 수집은 커널 시작 전 `SEOUL_COLLECT=1` 설정. |
| `03_KOPIS_스냅샷검증.ipynb` | 종료한 수집 회차를 검증하고 불변 스냅샷 및 공용 입력 명세를 등록한다. 네트워크 요청은 없다. |
| `04_KOPIS_CLI_오프라인검증.ipynb` | 가짜 응답과 시계로 CLI 동작을 검증한다. 실제 API 요청은 없다. |
| `05_일자시간대매출_자료확보.ipynb` | 기본은 저장 원문의 오프라인 검증. 새 수집은 커널 시작 전 `TIME_SALES_FETCH=1` 설정. |

프로젝트 루트의 PowerShell에서 다음 명령을 사용한다.

```powershell
.\collection\kopis.cmd status
.\collection\kopis.cmd run
.\collection\kopis.cmd watch
.\collection\kopis.cmd stop
```

KOPIS 정상 호출 간격은 1초이며 HTTP 400은 같은 ID로 3초 뒤 재시도한다. 그 외 차단 응답은 중단한다. 인증키는 외부 설정 또는 환경변수에서 읽는다.

| 내용 | 저장 위치 |
| --- | --- |
| 새 수집 원문 | `data/raw/` 아래 새 회차 폴더 |
| 공용 수집 명세 | `metadata/collection/` |
| KOPIS 수집 상태·검증 결과 | `results/collection/kopis/` |
| 서울시 재수집 검증 결과 | `results/collection/seoul/` |
| 일자·시간대 자료 확보 표·상태 | `results/main/data_access/` |
| 일자·시간대 검토 HTML 보관본 | `reports/main/data_access/` |
| 신청·문의 초안 | `docs/data_requests/` |

현재 분석의 고정 입력은 `metadata/main/`에 있다. 공용 수집 명세가 갱신되어도 현재 분석 입력은 자동으로 바뀌지 않는다. 05번은 자료 접근성 명세 `metadata/main/time_sales_access_sources.json`을 사용하며, 이 명세는 기존 매출 분석의 입력과 구분한다. 분석에는 수집 중인 CSV를 직접 사용하지 않는다.

폴더 정리 후에는 04번 오프라인 검증만 실행했다. 다른 수집 노트북은 경로와 구문만 확인했으며 새 수집이나 스냅샷 등록은 실행하지 않았다.
