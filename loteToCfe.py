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

	#Patterns
	pattern = ['^\<\?xml version="1.0" encoding="UTF-8"\?\>\<envCFe versao="\d{1,}.\d{1,}" xmlns="http://www.fazenda.sp.gov.br/sat"\>','^<?xml version="1.0" encoding="UTF-8"?><envCFe xmlns="http://www.fazenda.sp.gov.br/sat" versao="\d{1,}.\d{1,}">','^\<\?xml version="1.0" encoding="UTF-8"\?\>\<envCFe xmlns="http://www.fazenda.sp.gov.br/sat" versao="\d{1,}.\d{1,}"\>','\<envCFe versao="\d{1,}.\d{1,}" xmlns="http://www.fazenda.sp.gov.br/sat"\>']
	
	patternCanc = ['^\<\?xml version="1.0" encoding="UTF-8"\?\>\<cancCFe xmlns="http://www.fazenda.sp.gov.br/sat" versao="\d{1,}.\d{1,}"\>','^\<\?xml version="1.0" encoding="UTF-8"\?\>\<cancCFe versao="\d{1,}.\d{1,}" xmlns="http://www.fazenda.sp.gov.br/sat"\>']
	
	isXMLlote=None
	normal=True
	
	for p in patternCanc:
		if(re.match(p,lote[:150])):
				isXMLlote = True
				normal=False
				break
				
	for p in pattern:
		if(re.match(p,lote[:150])):
			isXMLlote = True
			break
	
	#verifica se e XML lote Normal [TIPOS: NORMAL/CANCELADO]
	if(normal):
		#Verifica se o XML é um arquivo em lotes CFe validos
		if (isXMLlote):
			#processa XML
			return ProcessaXML(lote,'<CFe>','</CFe>')	
		else:
			# Arquivo Xml de lote invalido
			return None
	else:
		if (isXMLlote):
			#processa XML
			return ProcessaXML(lote,'<CFeCanc>','</CFeCanc>','-canc')
		else:
			# Arquivo Xml de lote invalido
			return None
		
def ProcessaXML(lote,start_tag,end_tag,sufix=""):
	'''
	:param str lote: xml de lote
	:param str start_tag: Tag de abertura do cupom
	:param str end_tag: Tag de fechamento do cupom
	:param str sufix: Sufixo adicionado no nome do cupom
	'''
	#incremento
	incremento = len(end_tag)
	#inicio do cupom
	inicio=0
	#final do cupom
	fim=0
	#lista com as informacoes de todos os cupons
	lista=[]	
	#enquanto existe as tags acima faca o loop
	while (inicio>=0) and (fim >=0):
		#
		inicio=lote.find(start_tag,inicio)
		#
		fim=lote.find(end_tag,inicio)+incremento
		
		if inicio >= 0 and fim >= 0:
			lista.append({"ini":inicio,"fim":fim,"nome":XmlCfeNome(lote[inicio:fim])+sufix})
			inicio=fim
	return lista
	

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
