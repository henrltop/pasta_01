from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import json


#para não abrir o browser
options = Options()
options.headless = True
navegador = webdriver.Firefox(options=options)


#Abrir o navegador
navegador.get(
    'https://www.gp.srv.br/transparencia_barradogarcas/servlet/contrato_servidor_v3?1')
print("navegador")


#Clicar o botão pesquisar
pesquisar = navegador.find_element(By.ID , 'DIV_BTN_PESQUISAR')
pesquisar.click()
print("pesquisar")


#Clicar em exibir e selecionar a opção '150'
exibir = WebDriverWait(navegador, 40).until(
    EC.element_to_be_clickable((By.ID, 'vQTD_POR_PAGINA')))
exibir_paginas = Select(exibir)
exibir_paginas.select_by_value('150')
print("exibir")


#Botão Próximo
#Não funcionou apenas clicar, então foi necessário executar no console da inspeção do site
proximo = "document.querySelector('#TB_PROXIMO_ENABLED').querySelector('a').click()"
print("proximo")


#O programa tem q ter tempo p raciocinar
sleep(5)


#Criando um dicionário
map = {}


#Lendo a quantidade de registros ou de páginas.
total_registros_loc = (By.ID, 'span_vTOTAL_REGISTROS')
total_registros_e = WebDriverWait(navegador, 30).until(
    EC.visibility_of_element_located(total_registros_loc))
total_registros = total_registros_e.text
registros = int(total_registros_e.text)


#Como o meu não tinha a quantidade de páginas, eu tive que calcular
if (registros % 150 != 0):
    quantidade_paginas = registros//150 + 1
else:
    quantidade_paginas = registros//150


#Lê a tabela com os dados
def ler_tabela():
    table = navegador.find_element(By.ID , 'TB_GRID') #encontra a tabela
    tbody = table.find_element(By.TAG_NAME, 'tbody') #encontra o corpo do texto
    tr = tbody.find_elements(By.TAG_NAME, 'tr') #encontra 'tr' que é a linha
    for current in tr:
        td = current.find_elements(By.TAG_NAME, 'td') #encontra os setores de 'tr'
        matricula = td[0].get_property('innerText') #matricula recebe o texto do primeiro setor
        nome = td[1].get_property('innerText') #nome recebe o texto do segundo setor
        map[matricula] = nome #no dicionário, matricula recebe o nome. caso o servidor aparecessa mais de uma vez, ele sobrescreve


ler_tabela()

count = 1 #desnecessário. só para eu saber em que página está
i = 0
while i <= quantidade_paginas:
    i += 1
    ler_tabela()
    print("lido") 
    navegador.execute_script(proximo) #clica em o botão 'próximo'
    count += 1
    print("pag", count)
    sleep(3) #ele leva um tempo p raciocinar, liga não


ler_tabela()

print(map)


#Cria um arquivo com os dados :)
file = open('dados.json', 'w')
json.dump(map, file, ensure_ascii=False)
file.close()

#Fecha o navegador
navegador.close()