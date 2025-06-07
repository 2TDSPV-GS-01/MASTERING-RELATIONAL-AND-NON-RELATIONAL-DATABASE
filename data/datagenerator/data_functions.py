import random
import re
import string
import sys
import os
import unicodedata
from faker import Faker

fake = Faker("pt_br")


def remover_acentuacao(string: str) -> str:
    # Normalize a string para decompor acentos e caracteres especiais
    nfkd_form = unicodedata.normalize("NFKD", string)
    # Filtra apenas os caracteres que não sejam diacríticos (acentos)
    return "".join([char for char in nfkd_form if not unicodedata.combining(char)])


def remover_caracteres_especiais(string: str) -> str:
    # Remove caracteres especiais que não sejam letras, números ou espaços
    return re.sub(r"[^A-Za-z0-9 ]+", "", string)


def gerar_data_hora():
    return fake.date_time_this_year()


def gerador_data_horas(quantidade_data_horas: int):
    lst_data_horas = list()

    while len(lst_data_horas) < quantidade_data_horas:
        data_hora = gerar_data_hora()
        if data_hora not in lst_data_horas:
            lst_data_horas.append(data_hora)
    return (item for item in lst_data_horas)


def gerar_numero():
    return fake.cellphone_number()


def gerador_numeros(quantidade_numeros: int):
    lst_numeros = list()

    while len(lst_numeros) < quantidade_numeros:
        numero = gerar_numero()
        if numero not in lst_numeros:
            lst_numeros.append(numero)
    return (item for item in lst_numeros)


def gerar_endereco():
    endereco = fake.street_address()
    endereco = remover_acentuacao(endereco)
    endereco = remover_caracteres_especiais(endereco)
    return endereco


def gerador_enderecos(quantidade_enderecos: int):
    lst_enderecos = list()

    while len(lst_enderecos) < quantidade_enderecos:
        endereco = gerar_endereco()
        if endereco not in lst_enderecos:
            lst_enderecos.append(endereco)
    return (item for item in lst_enderecos)


def digito_verificador_1(cpf: list):
    soma = 0
    peso = 10
    for n in cpf:
        soma += n * peso
        peso -= 1
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        return 0
    else:
        return resto


def digito_verificador_2(cpf: list):
    soma = 0
    peso = 11
    for n in cpf:
        soma += n * peso
        peso -= 1
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        return 0
    else:
        return resto


# Gerador
def gerar_cpf():
    lista_numeros = [random.randint(0, 9) for i in range(9)]
    lista_numeros.append(digito_verificador_1(lista_numeros))
    lista_numeros.append(digito_verificador_2(lista_numeros))
    map_lista_numeros = map(str, lista_numeros)
    cpf = "".join(map_lista_numeros)
    return cpf


def gerador_cpf(quantidade_cpf: int):
    lst_cpf = list()

    while len(lst_cpf) < quantidade_cpf:
        lista_numeros = [random.randint(0, 9) for i in range(9)]
        lista_numeros.append(digito_verificador_1(lista_numeros))
        lista_numeros.append(digito_verificador_2(lista_numeros))
        map_lista_numeros = map(str, lista_numeros)

        cpf = "".join(map_lista_numeros)
        if cpf not in lst_cpf:
            lst_cpf.append(cpf)
    return (novo_cpf for novo_cpf in lst_cpf)


def gerar_nome():
    nome = fake.name()
    sobrenome = fake.last_name()
    nome_completo = f"{nome} {sobrenome}"
    nome_completo = remover_acentuacao(nome_completo)
    nome_completo = remover_caracteres_especiais(nome_completo)
    return nome_completo


def gerador_nomes(quantidade_nomes: int):
    lst_nomes = list()

    while len(lst_nomes) < quantidade_nomes:
        nome = gerar_nome()
        if nome not in lst_nomes:
            lst_nomes.append(nome)
    return (name for name in lst_nomes)


def gerar_email():
    return fake.free_email()


def gerador_emails(quantidade_emails: int):
    lst_emails = list()

    while len(lst_emails) < quantidade_emails:
        email = gerar_email()
        if email not in lst_emails:
            lst_emails.append(email)
    return (item for item in lst_emails)


def gerar_endereco():
    endereco = fake.street_address()
    endereco = remover_acentuacao(endereco)
    endereco = remover_caracteres_especiais(endereco)
    return endereco


def gerador_enderecos(quantidade_enderecos: int):
    lst_enderecos = list()

    while len(lst_enderecos) < quantidade_enderecos:
        endereco = gerar_endereco()
        if endereco not in lst_enderecos:
            lst_enderecos.append(endereco)
    return (item for item in lst_enderecos)


def insert_enderecos(qtd_enderecos: int):
    lst_insert_enderecos = []
    enderecos = gerador_enderecos(qtd_enderecos)
    for endereco in enderecos:
        str_insert = f"INSERT INTO T_FV_ENDERECO (ID_ENDERECO, DS_PAIS, DS_ESTADO, DS_CIDADE, DS_RUA) VALUES (SEQ_ID_ENDERECO.NEXTVAL, 'BRASIL', '{fake.state()}', '{fake.city()}', '{endereco}');"
        lst_insert_enderecos.append(str_insert)
    return lst_insert_enderecos


def insert_fornecedor():
    lst_insert_fornecedor = []
    end = 0
    lst_enderecos = insert_enderecos(len(dict_fornecedores))
    for fornecedor in dict_fornecedores:
        lst_insert_fornecedor.append(lst_enderecos[end])
        end += 1
        cnpj_limpo = fake.cnpj().replace(".", "").replace("-", "").replace("/", "")
        nome_fornecedor = fornecedor["NM_FORNECEDOR"].replace("'", "''")
        str_insert_fornecedor = f"INSERT INTO T_FV_FORNECEDOR (DS_CNPJ, NM_FORNECEDOR, ID_ENDERECO) VALUES ('{cnpj_limpo}', '{nome_fornecedor}', SEQ_ID_ENDERECO.CURRVAL);"
        lst_insert_fornecedor.append(str_insert_fornecedor)
        str_insert_contato_fornecedor = f"INSERT INTO T_FV_CONTATO (ID_CONTATO, DS_TELEFONE, DS_EMAIL, DS_CNPJ) VALUES (SEQ_ID_CONTATO.NEXTVAL, '{re.sub(r"\D", "", fake.phone_number())[:11]}', '{fake.email()}', '{cnpj_limpo}');"
        lst_insert_fornecedor.append(str_insert_contato_fornecedor)
        for material in fornecedor.get("MATERIAL"):
            str_insert_material = f"INSERT INTO T_FV_MATERIAL (ID_MATERIAL, NM_MATERIAL, TP_MATERIAL, NR_QUANT_ESTOQUE, NR_PRECO_UNIDADE, DS_CNPJ) VALUES (SEQ_ID_MATERIAL.NEXTVAL, '{material.get('NM_MATERIAL').replace("'", "''")}', '{material.get('TP_MATERIAL').replace("'", "''")}', {material.get('NR_QUANT_ESTOQUE')}, {material.get('NR_PRECO_UNIDADE'):.2F},'{cnpj_limpo}');"
            lst_insert_fornecedor.append(str_insert_material)
    return lst_insert_fornecedor


def insert_stacao(qtd_estacao: int):
    lst_insert_estacao = []
    gen_cpf = gerador_cpf(qtd_estacao + 1)
    gen_nomes = gerador_nomes(qtd_estacao + 1)
    responsavel = [next(gen_cpf), next(gen_nomes), re.sub(r"\D", "", fake.phone_number())[:11], fake.email()]
    str_insert_responsavel = f"INSERT INTO T_FV_RESPONSAVEL (DS_CPF, NM_RESPONSAVEL) VALUES ('{responsavel[0]}', '{responsavel[1]}');"
    lst_insert_estacao.append(str_insert_responsavel)
    for estacao in range(qtd_estacao):
        opcao = random.choice(["a", "b", "c"])
        match opcao:
            case "a":
                str_insert_contato_responsavel = f"INSERT INTO T_FV_CONTATO (ID_CONTATO, DS_TELEFONE, DS_EMAIL, DS_CPF) VALUES (SEQ_ID_CONTATO.NEXTVAL, '{responsavel[2]}', '{responsavel[3]}', '{responsavel[0]}');"
                lst_insert_estacao.append(str_insert_contato_responsavel)
                str_insert_estacao = f"INSERT INTO T_FV_ESTACAO_TRATAMENTO (ID_ESTACAO_TRATAMENTO, DT_INSTALACAO, ST_ESTACAO, DS_CPF) VALUES (SEQ_ID_ESTACAO.NEXTVAL, TO_DATE('{fake.date_this_month()}', 'YYYY-MM-DD'), 'A', '{responsavel[0]}');"
                lst_insert_estacao.append(str_insert_estacao)
                str_insert_sensor_ph = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'PH', 'PH', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_ntu = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TURBIDEZ', 'NTU', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_temperatura = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TEMPERATURA', 'CELSIUS', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_nivel = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'NIVEL', 'CM', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_vazao = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'VAZAO', 'LPM', SEQ_ID_ESTACAO.CURRVAL);"
                lst_insert_estacao.extend(
                    [
                        str_insert_sensor_ph,
                        str_insert_sensor_ntu,
                        str_insert_sensor_temperatura,
                        str_insert_sensor_nivel,
                        str_insert_sensor_vazao,
                    ]
                )
            case "b":
                responsavel = [
                    next(gen_cpf),
                    next(gen_nomes),
                    re.sub(r"\D", "", fake.phone_number())[:11],
                    fake.email(),
                ]
                str_insert_responsavel = f"INSERT INTO T_FV_RESPONSAVEL (DS_CPF, NM_RESPONSAVEL) VALUES ('{responsavel[0]}', '{responsavel[1]}');"
                lst_insert_estacao.append(str_insert_responsavel)
                str_insert_contato_responsavel = f"INSERT INTO T_FV_CONTATO (ID_CONTATO, DS_TELEFONE, DS_EMAIL, DS_CPF) VALUES (SEQ_ID_CONTATO.NEXTVAL, '{responsavel[2]}', '{responsavel[3]}', '{responsavel[0]}');"
                lst_insert_estacao.append(str_insert_contato_responsavel)
                str_insert_estacao = f"INSERT INTO T_FV_ESTACAO_TRATAMENTO (ID_ESTACAO_TRATAMENTO, DT_INSTALACAO, ST_ESTACAO, DS_CPF) VALUES (SEQ_ID_ESTACAO.NEXTVAL, TO_DATE('{fake.date_this_month()}', 'YYYY-MM-DD'), 'A', '{responsavel[0]}');"
                lst_insert_estacao.append(str_insert_estacao)
                str_insert_sensor_ph = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'PH', 'PH', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_ntu = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TURBIDEZ', 'NTU', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_temperatura = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TEMPERATURA', 'CELSIUS', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_nivel = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'NIVEL', 'CM', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_vazao = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'VAZAO', 'LPM', SEQ_ID_ESTACAO.CURRVAL);"
                lst_insert_estacao.extend(
                    [
                        str_insert_sensor_ph,
                        str_insert_sensor_ntu,
                        str_insert_sensor_temperatura,
                        str_insert_sensor_nivel,
                        str_insert_sensor_vazao,
                    ]
                )
            case "c":
                str_insert_estacao = f"INSERT INTO T_FV_ESTACAO_TRATAMENTO (ID_ESTACAO_TRATAMENTO, DT_INSTALACAO, ST_ESTACAO) VALUES (SEQ_ID_ESTACAO.NEXTVAL, TO_DATE('{fake.date_this_month()}', 'YYYY-MM-DD'), 'I');"
                lst_insert_estacao.append(str_insert_estacao)
                str_insert_sensor_ph = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'PH', 'PH', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_ntu = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TURBIDEZ', 'NTU', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_temperatura = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'TEMPERATURA', 'CELSIUS', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_nivel = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'NIVEL', 'CM', SEQ_ID_ESTACAO.CURRVAL);"
                str_insert_sensor_vazao = f"INSERT INTO T_FV_SENSOR (ID_SENSOR, TP_SENSOR, TP_MEDIDA, ID_ESTACAO_TRATAMENTO) VALUES (SEQ_ID_SENSOR.NEXTVAL, 'VAZAO', 'LPM', SEQ_ID_ESTACAO.CURRVAL);"
                lst_insert_estacao.extend(
                    [
                        str_insert_sensor_ph,
                        str_insert_sensor_ntu,
                        str_insert_sensor_temperatura,
                        str_insert_sensor_nivel,
                        str_insert_sensor_vazao,
                    ]
                )

    return lst_insert_estacao

lst_fornecedores = [
    "HidroTec Ambiental LTDA",
    "SolarFix Energia Renovável",
    "BioÁgua Soluções Sustentáveis",
    "ÁguaPura Equipamentos",
    "EcoReservas Brasil",
    "FiltroMax Industrial",
    "UVClean Tecnologia",
    "TecnoFluidez Sistemas",
    "SensorVille Equipamentos IoT",
    "GreenPipe Engenharia",
]

lst_tp_material = ["ELETRONICO", "FILTRO", "RESERVATORIO", "SENSOR"]

lst_tp_sensor = ["PH", "TURBIDEZ", "TEMPERATURA", "NIVEL", "VAZAO"]
lst_unidade_media = ["PH", "NTU", "CELSIUS", "CM", "LPM"]


dict_fornecedores = [
    {
        "NM_FORNECEDOR": "HidroTec Ambiental LTDA",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Filtro de Areia Camada Grossa",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 39,
                "NR_PRECO_UNIDADE": 72.56,
            },
            {
                "NM_MATERIAL": "Filtro de Carvão Ativado Premium",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 10,
                "NR_PRECO_UNIDADE": 137.87,
            },
            {
                "NM_MATERIAL": "Reservatório 40L em PVC",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 39,
                "NR_PRECO_UNIDADE": 60.53,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "SolarFix Energia Renovável",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Painel Solar 10W",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 47,
                "NR_PRECO_UNIDADE": 142.99,
            },
            {
                "NM_MATERIAL": "Controlador de Carga Solar",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 40,
                "NR_PRECO_UNIDADE": 123.39,
            },
            {
                "NM_MATERIAL": "Bateria de Lítio 12V",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 15,
                "NR_PRECO_UNIDADE": 37.55,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "BioÁgua Soluções Sustentáveis",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Caixa de Água 60L",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 10,
                "NR_PRECO_UNIDADE": 114.93,
            },
            {
                "NM_MATERIAL": "Filtro Multicamadas Compacto",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 37,
                "NR_PRECO_UNIDADE": 126.79,
            },
            {
                "NM_MATERIAL": "Kit Conector de Entrada",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 34,
                "NR_PRECO_UNIDADE": 69.78,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "ÁguaPura Equipamentos",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Filtro UV Padrão",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 35,
                "NR_PRECO_UNIDADE": 23.66,
            },
            {
                "NM_MATERIAL": "Tanque de Decantação",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 9,
                "NR_PRECO_UNIDADE": 65.71,
            },
            {
                "NM_MATERIAL": "Filtro de Sedimentos",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 20,
                "NR_PRECO_UNIDADE": 20.17,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "EcoReservas Brasil",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Tanque Modular 100L",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 8,
                "NR_PRECO_UNIDADE": 24.46,
            },
            {
                "NM_MATERIAL": "Tampa Selada de Reservatório",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 38,
                "NR_PRECO_UNIDADE": 112.47,
            },
            {
                "NM_MATERIAL": "Base de Apoio em Plástico",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 22,
                "NR_PRECO_UNIDADE": 142.43,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "FiltroMax Industrial",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Filtro Industrial de Areia",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 46,
                "NR_PRECO_UNIDADE": 147.37,
            },
            {
                "NM_MATERIAL": "Filtro de Alta Pressão",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 15,
                "NR_PRECO_UNIDADE": 103.55,
            },
            {
                "NM_MATERIAL": "Elemento Filtrante Substituível",
                "TP_MATERIAL": "FILTRO",
                "NR_QUANT_ESTOQUE": 49,
                "NR_PRECO_UNIDADE": 115.46,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "UVClean Tecnologia",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Lâmpada UV-C 15W",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 41,
                "NR_PRECO_UNIDADE": 58.55,
            },
            {
                "NM_MATERIAL": "Reator Eletrônico UV",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 12,
                "NR_PRECO_UNIDADE": 118.19,
            },
            {
                "NM_MATERIAL": "Kit UV Clean Pro",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 43,
                "NR_PRECO_UNIDADE": 65.7,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "TecnoFluidez Sistemas",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Sensor de Nível Ultrassônico",
                "TP_MATERIAL": "SENSOR",
                "NR_QUANT_ESTOQUE": 32,
                "NR_PRECO_UNIDADE": 92.93,
            },
            {
                "NM_MATERIAL": "Controlador de Vazão Digital",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 22,
                "NR_PRECO_UNIDADE": 120.36,
            },
            {
                "NM_MATERIAL": "Placa de Comando IoT",
                "TP_MATERIAL": "ELETRONICO",
                "NR_QUANT_ESTOQUE": 47,
                "NR_PRECO_UNIDADE": 92.93,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "SensorVille Equipamentos IoT",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Sensor de pH Modelo A1",
                "TP_MATERIAL": "SENSOR",
                "NR_QUANT_ESTOQUE": 41,
                "NR_PRECO_UNIDADE": 104.79,
            },
            {
                "NM_MATERIAL": "Sensor de Turbidez T-200",
                "TP_MATERIAL": "SENSOR",
                "NR_QUANT_ESTOQUE": 6,
                "NR_PRECO_UNIDADE": 42.45,
            },
            {
                "NM_MATERIAL": "Sensor de Temperatura Aquática",
                "TP_MATERIAL": "SENSOR",
                "NR_QUANT_ESTOQUE": 23,
                "NR_PRECO_UNIDADE": 124.65,
            },
        ],
    },
    {
        "NM_FORNECEDOR": "GreenPipe Engenharia",
        "MATERIAL": [
            {
                "NM_MATERIAL": "Tubo Conexão Rápida 3/4",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 50,
                "NR_PRECO_UNIDADE": 87.16,
            },
            {
                "NM_MATERIAL": "Joelho PVC 90°",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 49,
                "NR_PRECO_UNIDADE": 88.94,
            },
            {
                "NM_MATERIAL": "Válvula de Escoamento",
                "TP_MATERIAL": "RESERVATORIO",
                "NR_QUANT_ESTOQUE": 40,
                "NR_PRECO_UNIDADE": 122.56,
            },
        ],
    },
]

