#!/usr/bin/python3
import os,re
import argparse

clear = lambda : os.system('cls' if os.name=='nt' else 'clear')

clear()

def CalculaDigV(chave,verbose,mes,ano):
	
	#numero de digitos
	num_dig=43
	#Verifica se a chave e menor que 43
	flag1=True
	#verifica se a chave tem somente numero
	flag2=True
	
	size=len(chave)

	if size < num_dig:
		flag1=False
	elif size > num_dig:
		
		print ("Valor maior que o necessario, somente sera usado os %i primeiros digitos."%num_dig)
		chave=chave[:43]

	for c in chave:
		if not c.isnumeric():
			flag2=False
			break

	if not flag1:
		print ("Tamanho da chave menor que o necessario.")
		return
	if not flag2:
		print("Caracteres invalidos na chave use somente numeros.")
		return
		
	soma=0
	multiplicador=2
	
	# Verificar se parametro mes esta preenchido entao fazer a alteracao
	if mes != -1:
		#altera o mes da chave
		chave = re.sub('^'+chave[:6],chave[:4]+str(mes).zfill(2),chave)

	if ano != -1:
	#altera o ano da chave
		chave = re.sub('^'+chave[:4],chave[:2]+str(ano).zfill(2),chave)
		

	if(verbose):
		print ("A chave a ser utilizada sera: %s."%chave)
			
	#Multiplica do 43° até o 1° caractere da chave
	for c in reversed(chave):
		soma+= int(c)*multiplicador
		multiplicador+=1
		if multiplicador > 9 :
			multiplicador=2

	resto = soma % 11

	digito_verificador= 11 - resto

	if digito_verificador>= 10:
		digito_verificador = 0
	
	if(verbose):
		m = re.search('(\d{2})(\d{2})(\d{2})(\d{14})(\d{2})(\d{3})(\d{9})(\d{9})', chave)#(\d{2})(\d{2})(\d{2})(\d{14})(\d{2})(\d{3})(\d{9})(\d{9})
		print("\nCodigo do estado: %s"%m.group(1))
		print("Ano: %i"%(int(m.group(2))+2000))
		print("Mes: %s"%m.group(3))
		print("CNPJ emitente: %s"%m.group(4))
		print("Modelo Nfe: %s"%m.group(5))
		print("Serie Nfe: %s"%m.group(6))
		print("Numero Nfe: %s"%m.group(7))
		print("Codido Nfe: %s"%m.group(8))
		print ("Digito verificador e %i."%digito_verificador)
	else:
		#Resultado do calculo do digito verificador	
		print (digito_verificador)

'''parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max,help='sum the integers (default: find the max)')
args = parser.parse_args()

print(args.accumulate(args.integers))'''

parser = argparse.ArgumentParser()
parser.add_argument("chave", help="chave de acesso da Nfe")
parser.add_argument("-v", "--verbosity", action="store_true",help="Exibe mais informacoes sobre a chave")
parser.add_argument("-m", "--mes",type=int,default=-1,help="Muda o mes para o especificado")
parser.add_argument("-ano", "--ano",type=int,default=-1,help="Muda o ano para o especificado")
args = parser.parse_args()

CalculaDigV(args.chave,args.verbosity,args.mes,args.ano)
	 
	 
