#Requires -Version 5.1
param(
  [Parameter(Mandatory = $true)][string]$InputVideo,
  [Parameter(Mandatory = $true)][string]$Srt,
  [Parameter(Mandatory = $true)][string]$OutputVideo,
  [string]$FontName = "Microsoft JhengHei",
  [int]$FontSize = 20
)
# 燒錄硬字幕：中文路徑先複製到英文暫存再燒，避免 subtitles 濾鏡跳脫問題
$ErrorActionPreference = "Stop"
$tmp = Join-Path $env:TEMP "opencode"
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
$tmpSrt = Join-Path $tmp "burn.srt"
Copy-Item -LiteralPath $Srt -Destination $tmpSrt -Force
$esc = ($tmpSrt -replace "\\", "/") -replace ":", "\:"
# TEMP 路徑含 C:，libass 需寫成 C\:/... 形式
$esc = $esc -replace "^C\\:", "C\:/"
$vf = "subtitles='${esc}':fontsdir='C\:/Windows/Fonts':force_style='FontName=${FontName},FontSize=${FontSize},PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=40'"
& ffmpeg -y -i $InputVideo -vf $vf -c:v libx264 -preset veryfast -crf 20 -c:a copy $OutputVideo
