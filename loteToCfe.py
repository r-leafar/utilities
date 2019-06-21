import re,os

def init():
	#Captura o caminho atual do script
	current = os.getcwd()
	#concatena a string do diretorio atual com a pasta 'xml'
	path = os.path.join(current,'xml')
	#verifica se o caminho formado existe
	if os.path.exists(path):
	#exibe um mensagem se existe
		print ("Diretorio temporario ja existe")
	else:
	#cria o diretorio caso ao existir
		os.mkdir(path)
	
def XmlCfeNome(xml):
	#captura o id do CFe baseado em REGEX 
	m = re.search('Id="(CFe\d{1,})"', xml)
	#retorna o id do CFe
	return m.group(1)
	

def XmlCfe(lote):
	#Verifica se o XML é um arquivo em lotes CFe validos
	if (re.match('^<envCFe xmlns="http://www.fazenda.sp.gov.br/sat" versao="\d{1,}.\d{1,}">',lote)):

		#tag de abertura do cupom
		b1 = '<CFe>'
		#tag de fechamento do cupom
		b2 = '</CFe>'
		#inicio do cupom
		inicio=0
		#final do cupom
		fim=0
		#lista com as informacoes de todos os cupons
		lista=[]	
		#enquanto existe as tags acima faca o loop
		while (inicio>=0) and (fim >=0):
			#
			inicio=lote.find(b1,inicio)
			#
			fim=lote.find(b2,inicio)+6
			
			if inicio >= 0 and fim >= 0:
				lista.append({"ini":inicio,"fim":fim,"nome":XmlCfeNome(lote[inicio:fim])})
				inicio=fim
		return lista
	else:
		# Arquivo Xml de lote invalido
		return None

def PegarArquivos():
	#Captura o caminho atual do script
	current = os.getcwd()
	#variavel responsavel por salvar todos os arquivos xml
	xml=[]
	#loop que salva as informacoes do diretorio atual em variaveis
	for root, dirs, files in os.walk(current):
	#loop que percorrer todos os arquivos
		for f in files:
		#verifica se o arquivo possue a extensao '.xml'
			if f.endswith(".xml"):
		#atribua a variavel do tipo lista responsavel por armazenar todos os xmls da pasta
				xml.append(f)
		# Inibe o for pegar os arquivos de outras pastas de forma recursiva
		break
	for x in xml:
		LerArquivo(x)

def LerArquivo(fname):
	#concatena a string do diretorio atual com a pasta 'xml'
	path = os.path.join(os.getcwd(),'xml')
	#Le arquivo Lote
	file = open(fname,'r') 
	#armazena na string o arquivo
	lote = file.read()
	#pegas as informacoes dos CFes
	listacfes = XmlCfe(lote)
	#Verifica se e um arquivo em lote valido
	if (listacfes != None):
		#percorre a lista de CFes
		for cfe in listacfes:
			#Nome do Xml a ser gravado
			cfefinal = cfe["nome"]+".xml"
			
			newfile = os.path.join(path,cfefinal)
			
			if (os.path.exists(newfile)):
				print ("Arquivo %s ja existente"%cfefinal)
				
			cfexml = open(newfile,"w")
			cfexml.write(lote[cfe["ini"]:cfe["fim"]])
			cfexml.close()
	else:
		#Informa que o arquivo de Lote Cfe nao e valido
		print ("%s arquivo de lote invalido"%fname)
		
		
	
	
	
init()
PegarArquivos()

	

