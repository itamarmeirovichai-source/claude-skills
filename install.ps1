# Installs the "minds" and "skill-prompt-architect" Claude Code skills (Windows).
# Usage: irm https://raw.githubusercontent.com/itamarmeirovichai-source/claude-skills/main/install.ps1 | iex
$ErrorActionPreference = "Stop"

$repo = "itamarmeirovichai-source/claude-skills"
$skills = @("minds", "skill-prompt-architect")
$dest = Join-Path $env:USERPROFILE ".claude/skills"

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("claude-skills-" + [System.Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

try {
    Write-Host "Downloading skills from github.com/$repo ..."
    $zip = Join-Path $tmp "repo.zip"
    Invoke-WebRequest -Uri "https://github.com/$repo/archive/refs/heads/main.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $tmp
    $root = Get-ChildItem -Path $tmp -Directory | Where-Object { $_.Name -like "claude-skills-*" } | Select-Object -First 1

    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    foreach ($s in $skills) {
        $target = Join-Path $dest $s
        if (Test-Path $target) {
            Move-Item $target "$target.bak.$PID"
            Write-Host "  (existing $s backed up to $s.bak.$PID)"
        }
        Copy-Item -Recurse (Join-Path $root.FullName "skills/$s") $target
        Write-Host "installed $s"
    }
}
finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Done! Open a NEW Claude Code session and type /minds or /skill-prompt-architect"
