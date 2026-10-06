@echo off
setlocal
title KOPIS Collection
call "%~dp0kopis.cmd" menu
set "KOPIS_EXIT=%errorlevel%"
if not "%KOPIS_EXIT%"=="0" pause
exit /b %KOPIS_EXIT%
