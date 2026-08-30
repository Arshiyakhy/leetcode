# Usage: .\new_problem.ps1 <number> <slug> <topic> <difficulty>
# Example: .\new_problem.ps1 1 two-sum arrays Easy

param(
    [Parameter(Mandatory=$true)][int]$Number,
    [Parameter(Mandatory=$true)][string]$Slug,
    [Parameter(Mandatory=$true)][string]$Topic,
    [Parameter(Mandatory=$true)][string]$Difficulty
)

$Padded = "{0:D4}" -f $Number
$Dir = Join-Path $Topic "$Padded-$Slug"
$Title = (Get-Culture).TextInfo.ToTitleCase($Slug -replace '-', ' ')
$Url = "https://leetcode.com/problems/$Slug/"

New-Item -ItemType Directory -Path $Dir -Force | Out-Null

$readmeContent = Get-Content "_template/README.md" -Raw
$readmeContent = $readmeContent -replace '\{NUMBER\}', $Number
$readmeContent = $readmeContent -replace '\{TITLE\}', $Title
$readmeContent = $readmeContent -replace '\{LEETCODE_URL\}', $Url
$readmeContent = $readmeContent -replace '\{DIFFICULTY\}', $Difficulty
$readmeContent = $readmeContent -replace '\{TOPIC\}', $Topic
Set-Content -Path (Join-Path $Dir "README.md") -Value $readmeContent -NoNewline

$solutionContent = Get-Content "_template/solution.py" -Raw
$solutionContent = $solutionContent -replace '\{NUMBER\}', $Number
$solutionContent = $solutionContent -replace '\{TITLE\}', $Title
$solutionContent = $solutionContent -replace '\{LEETCODE_URL\}', $Url
Set-Content -Path (Join-Path $Dir "solution.py") -Value $solutionContent -NoNewline

Write-Host "Created $Dir/"
Write-Host ""
Write-Host "Add this row to the index table in README.md:"
Write-Host "| $Number | $Title | $Difficulty | $Topic | [link]($($Dir -replace '\\','/')) |"
