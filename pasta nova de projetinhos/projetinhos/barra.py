from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

navegador = webdriver.Firefox()

navegador.get(
    'https://www.gp.srv.br/transparencia_barradogarcas/servlet/contrato_servidor_v3?1')
print("navegador")


pesquisar = navegador.find_element_by_id('DIV_BTN_PESQUISAR')
pesquisar.click()
print("pesquisar")

exibir = WebDriverWait(navegador, 40).until(
    EC.element_to_be_clickable((By.ID, 'vQTD_POR_PAGINA')))
exibir_paginas = Select(exibir)
exibir_paginas.select_by_value('150')
print("exibir")


proximo = "document.querySelector('#TB_PROXIMO_ENABLED').querySelector('a').click()"
print("proximo")

sleep(5)

map = {}


total_registros_loc = (By.ID, 'span_vTOTAL_REGISTROS')
total_registros_e = WebDriverWait(navegador, 30).until(
    EC.visibility_of_element_located(total_registros_loc))
total_registros = total_registros_e.text
registros = int(total_registros_e.text)


if (registros % 150 != 0):
    quantidade_paginas = registros//150 + 1
else:
    quantidade_paginas = registros//150


def ler_tabela():
    table = navegador.find_element_by_id('TB_GRID')
    tbody = table.find_element_by_tag_name('tbody')
    tr = tbody.find_elements_by_tag_name('tr')
    for current in tr:
        td = current.find_elements_by_tag_name('td')
        matricula = td[0].get_property('innerText')
        nome = td[1].get_property('innerText')
        map[matricula] = nome


ler_tabela()

count = 1
i = 0
while i <= quantidade_paginas:
    i += 1
    ler_tabela()
    print("lido")
    navegador.execute_script(proximo)
    count += 1
    print("pag", count)
    sleep(3)


ler_tabela()

print(map)

navegador.close()
