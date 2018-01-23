@echo off

if "%1" == ""				goto usage

if /i %1 == init     		goto init
if /i %1 == active     		goto activate
if /i %1 == deactive		goto deactivate
if /i %1 == prepare 		goto prepare
if /i %1 == build   		goto build
if /i %1 == fmt     		goto fmt
if /i %1 == clean			goto clean
goto usage

:init
virtualenv .env
goto :eof

:activate
if not exist "%~dp0.env\Scripts\activate.bat" call :init
%~dp0.env\Scripts\activate.bat
goto :eof

:deactivate
if exist "%~dp0.env\Scripts\deactivate.bat" (
	%~dp0.env\Scripts\deactivate.bat
)
goto :eof

:prepare
if not exist "%~dp0.env\Scripts\pip.exe" call :activate
%~dp0.env\Scripts\pip.exe install -r requirements.txt
goto :eof

:build
if not exist "%~dp0.env\Scripts\pyinstaller.exe" call :prepare
%~dp0.env\Scripts\pyinstaller.exe app.spec
goto :eof

:fmt
if not exist "%~dp0.env\Scripts\yapf.exe" call :prepare
for %%d in (*.py) do (
	echo formating... %%d
	%~dp0.env\Scripts\yapf.exe -i %%d
)
goto :eof

:clean
if exist "%~dp0\build" rmdir/s/q build
if exist "%~dp0\dist" rmdir/s/q dist
goto :eof

:usage
set space_2=  
set space_4=	
echo.
echo Usage cmd [command]
echo.
echo where [command] is one of:
echo %space_2%init		%space_4%create new virtual env
echo %space_2%active	%space_4%active virtual env
echo %space_2%deactive	%space_4%deactive virtual env
echo %space_2%prepare	%space_4%install all dependencies
echo %space_2%build		%space_4%package exe file
echo %space_2%fmt		%space_4%format all py files
echo %space_2%clean		%space_4%clean
