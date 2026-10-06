# 공연 활동과 주변 외식업 매출 분석

현재 사용할 코드는 **[final/README.md](final/README.md)**에 정리했다.

- **전체 실행:** [final/00_전체실행.ipynb](final/00_전체실행.ipynb)
- **분석 코드:** [final/notebooks/](final/notebooks/)
- **최종 결과:** [reports/final/](reports/final/)
- **원자료:** `data/raw/` — 원본 보존
- **최종 분석 데이터:** `data/analysis/final/`
- **이전 코드:** [archive/20261005_before_final/](archive/20261005_before_final/)
- **추가 검토 기록:** [reports/audit_20261005/report.html](reports/audit_20261005/report.html)

연구 범위는 종로구·마포구의 공개 외식업 10종, 2023~2025년 분기 자료다. 공연 ID 수와 총매출·야간 매출 비중의 관련성을 분석한다. 분기 자료로 관람 전후 소비나 인과효과를 직접 확인하는 연구는 아니다.

이전 코드는 이동 전후 파일 해시를 대조해 보관했다. 기존 파생 자료와 보고서는 남겨 두고 현재 결과는 별도 `final` 출력 경로에 저장한다. 수집 도구는 [final/KOPIS_수집기.cmd](final/KOPIS_수집기.cmd)에서 열 수 있으며, 분석 실행에는 인증키와 네트워크 요청이 필요하지 않다.
