# Rebuilds every material from source, exports PDFs, builds the website and runs the checks.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location (Join-Path $root "src")
python build_workshop.py; python build_talk.py; python build_examples.py; python build_docs.py; python build_guide.py
Set-Location $root
powershell -ExecutionPolicy Bypass -File scripts\render_office.ps1
python src\build_site.py
python scripts\check_numbers.py
python scripts\check_materials.py
python scripts\check_links.py
