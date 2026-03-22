@echo off
chcp 65001 >nul

REM ============================================
REM Deleting folders starting with "2-"
REM ============================================
echo Searching for folders starting with "2-"...
echo.

setlocal enabledelayedexpansion
set "folder_count=0"
set "folder_list="

for /d %%d in (2-*) do (
    set /a folder_count+=1
    set "folder_list=!folder_list!  - %%~nxd\r\n"
)

if %folder_count% equ 0 (
    echo No folders starting with "2-" were found.
    echo.
) else (
    echo Folders found: %folder_count%
    echo.
    echo List:
    for /d %%d in (2-*) do (
        echo   - %%~nxd
    )
    echo.
    set /p confirm="Delete these folders? (y/n): "
    if /i "!confirm!"=="y" (
        echo.
        echo Deleting...
        for /d %%d in (2-*) do (
            echo Removing: %%~nxd
            rmdir /s /q "%%d"
        )
        echo Done.
    ) else (
        echo.
        echo Skipped.
    )
    echo.
)

endlocal

REM ============================================
REM Main builder script
REM ============================================

python parse_questions.py
python make_summary.py

set RUST_LOG=debug
mdbook-epub-windows-amd64.exe --standalone
