@echo off
setlocal ENABLEEXTENSIONS

del /q /s vspice_test_result.xml

echo "TestCase","TestContent","TestResult","Details" > vspice_test_result.csv