@echo off
set ACTION=%~1

if "init" == "%ACTION%" (
goto:init
) else if "active" == "%ACTION%" (
goto:activate
) else if "deactive" == "%ACTION%" (
goto:deactivate
) else if "prepare" == "%ACTION%" (
goto:prepare
) else if "build" == "%ACTION%" (
goto:build
) else if "fmt" == "%ACTION%" (
goto:fmt
) else if "clean" == "%ACTION%" (
goto:clean
) else (
goto:usage
)

:init
virtualenv .env
goto :eof

:activate
if not exist "%~dp0.env\Scripts\activate.bat" call:init
call %~dp0.env\Scripts\activate.bat
goto :eof

:deactivate
if exist "%~dp0.env\Scripts\deactivate.bat" (
call %~dp0.env\Scripts\deactivate.bat
)
goto :eof

:prepare
if not exist "%~dp0.env\Scripts\pip.exe" call:activate
call %~dp0.env\Scripts\pip.exe install -r requirements.txt
goto :eof

:build
if not exist "%~dp0.env\Scripts\pyinstaller.exe" call:prepare
call %~dp0.env\Scripts\pyinstaller.exe app.spec
goto :eof

:fmt
if not exist "%~dp0.env\Scripts\yapf.exe" call:prepare
for %%d in (*.py) do (
	echo formating... %%d
	call %~dp0.env\Scripts\yapf.exe -i %%d
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
