
function init {

$path = Split-Path $script:MyInvocation.MyCommand.Path
$tmp = $path+"\xml"

if (Test-Path -Path $tmp){
    Write-Host "Diretorio temporario ja existe"
}else{
    New-Item -ItemType "directory" -Path $tmp
    Write-Host "Diretorio temporario criado"
}

}

function PegarArquivos {
$path = Split-Path $script:MyInvocation.MyCommand.Path
$xml = Get-ChildItem -Path $path -Filter "*.xml"
foreach ($row in $xml)
{
  LerArquivos($row.Name)
  
}

}
function LerArquivos($fname){
$path = Split-Path $script:MyInvocation.MyCommand.Path
$tmp = $path+"\xml\"
$lote = [IO.File]::ReadAllText($path+"\"+$fname)

if($lote -match '^<envCFe xmlns="http://www.fazenda.sp.gov.br/sat" versao="\d{1,}.\d{1,}">'){
    Write-Host "Lendo $fname"
    $listacfes =XmlCfe($lote)
    
    foreach ($cfe in $listacfes) {
    	
        $c = ([string]$cfe["nome"])
		
        $cfefinal= $tmp+$c+'.xml'
        $cfefinal= $cfefinal.Replace("True ",'')
        
        
        if (Test-Path -Path $cfefinal -PathType Leaf){
            Write-Host "Arquivo $c ja existente"
        }else{
            $lote.substring($cfe["ini"],$cfe["fim"]-$cfe["ini"])|Out-File $cfefinal
        }     
    
    }
    
}else{
    Write-Host ($fname+" arquivo de lote invalido")
}

}
function XmlCfeNome($xml){
$xml -Match('Id="(CFe\d{1,})"')
$rs = $matches[1]
return $rs


}

function XmlCfe($lote){
#tag de abertura do cupom
$b1 = '<CFe>'
#tag de fechamento do cupom
$b2 = '</CFe>'
#inicio do cupom
$inicio=0
#final do cupom
$fim=0
#lista com as informacoes de todos os cupons
$lista=@()

while (($inicio -ge 0) -And ($fim -ge 0)){
    Try{	
        
        $inicio = $lote.IndexOf($b1,$inicio)   
        $fim=$lote.IndexOf($b2,$inicio)+6
        
        if(($inicio -ge 0) -And ($fim -ge 0)){
        
        $nome = XmlCfeNome($lote.substring($inicio,$fim-$inicio))
    
        $cfe = @{
          "ini"=$inicio
          "fim"=$fim
          "nome"=$nome
         }
           
         $lista += ,$cfe
           
         #Write-Host "$inicio - $fim [$nome "
         #Write-Host $cfe["nome"]
         $inicio=$fim
         }
        

    } Catch
    {   
       # Write-Host $_.Exception.Message
       # Write-Host "$inicio - $fim [$nome "
        $inicio=-1
    }
}
return $lista

}

init

PegarArquivos

