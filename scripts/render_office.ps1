# Renders the course's Office files to PDF with Microsoft Office, so each PDF comes
# from the same file as the editable source. Also writes a JSON overflow report.
#   powershell -ExecutionPolicy Bypass -File scripts\render_office.ps1 [-Only pattern] [-Png dir]
param([string]$Only = "", [string]$Png = "")
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$mat = Join-Path $root "materials"
$report = @()

$pptx = Get-ChildItem $mat -Recurse -Filter *.pptx | Where-Object { $_.Name -notlike "~*" -and $_.FullName -match $Only }
if ($pptx) {
  $pp = New-Object -ComObject PowerPoint.Application
  foreach ($f in $pptx) {
    $pres = $pp.Presentations.Open($f.FullName, -1, 0, 0)
    $pdf = [IO.Path]::ChangeExtension($f.FullName, ".pdf")
    $pres.SaveAs($pdf, 32)
    foreach ($sl in $pres.Slides) {
      foreach ($sh in $sl.Shapes) {
        if ($sh.HasTextFrame -and $sh.TextFrame.HasText) {
          $tr = $sh.TextFrame.TextRange
          $need = $tr.BoundHeight + $sh.TextFrame.MarginTop + $sh.TextFrame.MarginBottom
          $needW = $tr.BoundWidth + $sh.TextFrame.MarginLeft + $sh.TextFrame.MarginRight
          $bottom = $sh.Top + [Math]::Max($need, $sh.Height)
          if ($need -gt ($sh.Height + 1.5) -or $needW -gt ($sh.Width + 8) -or $bottom -gt 540 -or ($sh.Left + $sh.Width) -gt 960) {
            $report += [pscustomobject]@{ file = $f.Name; slide = $sl.SlideIndex; shape = $sh.Name; need = [math]::Round($need); have = [math]::Round($sh.Height); needW = [math]::Round($needW); haveW = [math]::Round($sh.Width); text = $tr.Text.Substring(0, [Math]::Min(50, $tr.Text.Length)) }
          }
        }
      }
    }
    if ($Png) {
      $dir = Join-Path $Png $f.BaseName
      New-Item -ItemType Directory -Force $dir | Out-Null
      $pres.Export($dir, "PNG", 1280, 720)
    }
    $pres.Close()
    Write-Host "pptx ok: $($f.Name)"
  }
  $pp.Quit()
}

$docx = Get-ChildItem $mat -Recurse -Filter *.docx | Where-Object { $_.Name -notlike "~*" -and $_.FullName -match $Only }
if ($docx) {
  foreach ($f in $docx) {
    # A fresh Word per file: long automation sessions are less stable
    $wd = New-Object -ComObject Word.Application
    $wd.Visible = $false
    $wd.DisplayAlerts = 0
    $doc = $wd.Documents.Open($f.FullName)
    foreach ($t in $doc.TablesOfContents) { $t.Update() }
    $null = $doc.Fields.Update()
    $doc.Save()
    $pdf = [IO.Path]::ChangeExtension($f.FullName, ".pdf")
    $doc.ExportAsFixedFormat($pdf, 17)
    $pages = $doc.ComputeStatistics(2)
    $doc.Close(0)
    try { $wd.Quit() } catch {}
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wd)
    Start-Sleep -Milliseconds 800
    Write-Host "docx ok: $($f.Name) ($pages pages)"
  }
}

if ($Png) { $report | ConvertTo-Json -Depth 3 | Out-File (Join-Path $Png "overflow.json") -Encoding utf8 }
Write-Host "overflow flags: $($report.Count)"
$report | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
