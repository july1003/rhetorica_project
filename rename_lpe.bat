@echo off
move docs\dockers\realtime_ai docs\dockers\Logos
move docs\dockers\vision_analysis docs\dockers\Pathos
move docs\dockers\central_data docs\dockers\Ethos
mkdir src\Logos
mkdir src\Pathos
mkdir src\Ethos
type nul > src\Logos\__init__.py
type nul > src\Pathos\__init__.py
type nul > src\Ethos\__init__.py
