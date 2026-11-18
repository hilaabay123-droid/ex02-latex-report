param([string]$name,[switch]$bib)
$env:TEXINPUTS='C:/biu/02;'
function Run($c,$a){ $p=Start-Process $c -ArgumentList $a -NoNewWindow -PassThru -RedirectStandardOutput "o_$name.txt"; if(-not $p.WaitForExit(240000)){Stop-Process $p -Force;'TIMEOUT'} }
$lt='--disable-installer','-interaction=nonstopmode',$name
Run lualatex $lt; if($bib){ Run biber $name; Run lualatex $lt; Run lualatex $lt }
Select-String "$name.log" -Pattern '^!|Warning|Overfull|Missing char' | Select -First 12 | % Line
pdfinfo "$name.pdf" | Select-String Pages
(pdffonts "$name.pdf" | Select -Skip 2 | % { ($_ -split '\s+')[0] }) -join ', '
Remove-Item "${name}img*.png" -ErrorAction SilentlyContinue
pdftoppm -r 80 -png "$name.pdf" "${name}img"
