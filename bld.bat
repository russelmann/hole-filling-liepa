REM set "CXXFLAGS=%CXXFLAGS:-GL=%"
REM set "CXXFLAGS= -MD"

REM set "CMAKE_GENERATOR=NMake Makefiles JOM"
set "CMAKE_GENERATOR=Visual Studio 15 2017"
"%PYTHON%" --version
"%PYTHON%" -m pip install . --no-deps -vv

if errorlevel 1 exit 1
