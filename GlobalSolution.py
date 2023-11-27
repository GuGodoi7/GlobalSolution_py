from Connection import *
import re
import requests
from datetime import date
import json

# Valida se o usuario digata algo nos inputs
def validar_informacoes_vazias(*args):
    if not all(args):
        print("Por favor, preencha todas as informações corretamente.")
        return False
    return True

# Verifica se usuario é maior de idade
def validar_data_nascimento(data):
    while True:
        try:
            dia, mes, ano = data.split('/')
            dia = int(dia)
            mes = int(mes)
            ano = int(ano)
            data_nascimento = date(ano, mes, dia)

            if ano <= 1950:
                print("Ano de nascimento deve ser maior que 1950.")
                return None
            # Calcula a data atual
            data_atual = date.today()

            # Calcula a data há 18 anos atrás
            data_limite = data_atual.replace(year=data_atual.year - 12)

            if data_nascimento <= data_limite:
                return data_nascimento
            else:
                print("Você deve ter pelo menos 12 anos para se cadastrar.")
        except ValueError:
            print("Data invalida verifique o Formato Use DD/MM/AAAA e tente novamente.")
        return None

# Verificar se email é valido
def verifica_email(email):
    try:
        padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
        if re.match(padrao, email):
            return True
        else:         
            print("e-mail inválido. Digite Novamente")
            return False
    except Exception as e:
        print(f"Erro: {e}")

# Função para validar formato da data
def validar_data(data):
    try:
        dia, mes, ano = data.split('/')
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
        data_validada = date(ano, mes, dia)
        return data_validada
    except ValueError:
        print("Formato de data inválido. Insira no formato DD/MM/AAAA.")
        return None

# Finção para validar telefoe
def verifica_telefone(telefone):
    try:
        padrao = r"^\(?\d{2}\)?\s\d{4,5}\d{4}$"

        if re.match(padrao, telefone):
            return True
        else:
            print("Número de telefone inválido.")
            return False
    except Exception as e:
        print(f"Erro: {e}")

# Função para validar que usuário digite somente letras e espaços 
def valida_nome(nome):
    try:
        if nome.replace(" ", "").isalpha():
            return nome
        else:
            raise ValueError("Digite um valor válido contendo apenas letras e espaços.")
    except ValueError as e:
        print(f"Erro: {e}")
        return None

# Função que valida a entrada de dados da def eventos
def validar_evento(nm_evento, dt_evento, tp_evento):
    if not all([nm_evento, dt_evento, tp_evento]):
        print("Por favor, preencha todas as informações do evento corretamente.")
        return False
    try:
        dia, mes, ano = dt_evento.split('/')
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
        dt = date(ano, mes, dia)

        if dt < date.today():
            print("A data do evento não pode ser anterior à data atual.")
            return False

    except ValueError:
        print("Formato de data inválido. Use o formato DD/MM/AAAA.")
        return False

    return True

# Obter informações do CEP por meio de uma API
def validar_cep(endereco):
    cep = endereco.replace(".", "").replace("-", "")
    if len(cep) != 8:
        print('CEP inválido. Deve conter 8 dígitos.')
        return False

    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        requisicao = requests.get(url)
        if requisicao.status_code == 200:
            dic_requisicao = requisicao.json()
            if 'erro' in dic_requisicao:
                print('CEP não encontrado ou inválido.')
                return False
            else:
                return True
        else:
            print('Erro na requisição.')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Erro na requisição à API: {e}')
        return False

# Função para validar crm por meio de uma API
def valida_crm(uf, crm):
    try:
        url = f'https://www.consultacrm.com.br/api/index.php?tipo=crm&uf={uf}&q={crm}&chave=8260412133&destino=json'
        requisicao = requests.get(url)
        resultado = requisicao.json()

        if resultado and 'item' in resultado and resultado['item']:
            nome = resultado['item'][0]['nome']
            return nome  
        else:
            return None

    except requests.RequestException as e:
        print(f"Ocorreu um erro de requisição: {e}")
        return None

# Menu para o usuário realizar cadastro e o login
def exibir_menu(opcoes):
    while True:
        print('''
=====================================================''')
        print("Escolha uma opção:")
        for i, opcao in enumerate(opcoes, 1):
            print(f"({i}) {opcao}")

        try:
            escolha = int(input("Digite o número da opção desejada: "))
            if escolha < 1 or escolha > len(opcoes):
                raise ValueError("Opção inválida. Tente novamente.")
            return escolha
        except ValueError as e:
            print(f"Ocorreu um erro: {e}")

# Função para o usuário realizar o cadastro
def cadastro():
    dados_cadastro = {}
    
    try:
        while True:
            nome = input("Nome usuário: ")
            if valida_nome(nome):
                break
            
        while True:
            senha = input("Senha: ")
            if validar_informacoes_vazias(senha):
                break
        
        while True:
            endereco = input("CEP: ")
            if validar_cep(endereco):
                break


        while True:
            data_nasc = input("Insira a data de nascimento (DD/MM/AAAA): ")
            if validar_data_nascimento(data_nasc):
                break

        dados_cadastro = {'Nome': nome, 'Senha': senha, 'Endereco': endereco, 'Data de Nascimento': data_nasc }
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    return dados_cadastro

# Usuario escolhe qual tipo de contato prefere email ou telefone
def tipo_contato():
    while True:
        try:
            contato = {}
            tp_contato = input("Qual tipo de contato deseja cadastrar? (Email ou Telefone): ").upper()

            if tp_contato == 'EMAIL':
                email = input("Digite seu e-mail: ")
                if verifica_email(email):
                    contato['tp_contato'] = 'EMAIL'
                    contato['email'] = email
                    return contato

            elif tp_contato == 'TELEFONE':
                tel = input("Digite seu telefone(XX XXXXXXXXX):  ")
                if verifica_telefone(tel):
                    contato['tp_contato'] = 'TELEFONE'
                    contato['telefone'] = tel
                    return contato
            else:
                print("Escolha inválida")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# Função para o usuário realizar o cadastro médico
def cadastro_medico():
    dados_cadastro = {}
    try:
        while True:
            nome = input("Nome do usuário: ")
            if valida_nome(nome):
                break
        
        while True:
            senha = input("Senha: ")
            if validar_informacoes_vazias(senha):
                break

        while True:
            crm_uf = input("Digite o CRM-UF (ex: 1234567-SP): ")
            if '-' in crm_uf:
                crm, uf = crm_uf.split('-')
                
                nome_pessoa = valida_crm(uf, crm)
                if nome_pessoa:
                    print(f"Nome da pessoa associada ao CRM: {nome_pessoa}")
                    dados_cadastro = {'nome': nome, 'senha': senha, 'crm': crm, 'uf': uf}
                    break
                else:
                    print("CRM inválido ou não encontrado. Tente novamente.")
            else:
                print("Formato do CRM-UF incorreto. Digite novamente no formato correto.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    return dados_cadastro

# Função para usuário realizar login 
def login():
    try:
        usuario_login = {}
        tentar_novamente = True

        while tentar_novamente:
            nome = input("Nome de usuário: ")
            senha = input("Senha: ")

            if not validar_informacoes_vazias(nome, senha):
                continue
            
            if autenticar_usuario(nome, senha) or autenticar_especialista(nome, senha):
                print("Autenticação bem-sucedida. Você está logado.")
                id = obter_id_usuario_por_nome_e_senha(nome, senha)
                usuario_login = {'id': id, 'Nome': nome, 'Senha': senha}
                return usuario_login
            else:
                print("Nome de usuário ou senha incorretos.")
                redefinir = input("Deseja redefinir a senha S/N: ")
                if redefinir.upper() == 'S':
                    redefinir_senha(nome)

                reiniciar = input("Deseja tentar novamente? (S/N): ")
                if reiniciar.upper() != 'S':
                    print("Programa finalizado.")
         
    except ValueError:
        print("Erro: Nome de usuário ou senha inválidos.")

# Função para verificar se o usuário já está cadastrado
def autenticar_usuario(nome, senha):
    connection = obter_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM T_MDV_REGISTRO_CLIENTE
            WHERE nm_usuario = :nome AND nm_senha = :senha
        """, {'nome': nome, 'senha': senha})
        resultado = cursor.fetchone()

        if resultado:
            return True  
        else:
            return False
    except oracledb.DatabaseError as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Função para verificar se o usuário já está cadastrado
def autenticar_especialista(nome, senha):
    connection = obter_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM T_MDV_REGISTRO_ESPECIALISTA
            WHERE nm_usuario = :nome AND nm_senha = :senha
        """, {'nome': nome, 'senha': senha})
        resultado = cursor.fetchone()

        if resultado:
            return True  
        else:
            return False
    except oracledb.DatabaseError as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        close_connection(connection)

# Função para redefinir senha
def redefinir_senha(nome_usuario):
    while True:
        try:
            nova_senha = input("Digite a nova senha: ")
            if validar_informacoes_vazias(nova_senha):
                continue
            
            conn = obter_connection()  #
            cursor = conn.cursor()

            cursor.execute("UPDATE T_MDV_REGISTRO_CLIENTE SET nm_senha = :nova_senha WHERE nm_usuario = :nome", {'nova_senha': nova_senha, 'nome': nome_usuario})
            
            conn.commit()
            cursor.close()
            conn.close()

            print("Senha redefinida com sucesso.")
        except oracledb.DatabaseError as e:
            print(f"Erro ao redefinir senha: {e}")

# Função onde o medico pode informar novas doenças que estão surgindo
def novas_doencas():
    while True:
        try:
            doenca = input("Insira o nome da doença: ")

            tp_doenca = input(f"Qual tipo de doença é '{doenca}': ")
            ds_doenca = input(f"Descrição da doença '{doenca}': ")
            faixa_etaria = input(f"Faixa etária para '{doenca}': ")

            if not validar_informacoes_vazias(tp_doenca, ds_doenca, faixa_etaria):
                continue  

            info_doenca = {'Nome': doenca, 'Tipo Doença': tp_doenca, 'Faixa Etária': faixa_etaria, 'Descrição': ds_doenca}
            break 

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    return info_doenca

# Medico informa a prevencoes das novas doenças
def prevencao(dados_doencas):
    while True:
        try:
            previnir = input("A doença já conta com algum tipo de prevenção? S/N: ") 
            if previnir.lower() == 's':
                confima_doenca = dados_doencas["Nome"]
                nm_vacina = input(f"Qual a vacina ajuda na prevenção da {confima_doenca}: ")
                nm_remedio = input(f"Qual o remédio ajuda na prevenção da {confima_doenca}: ")
                ds_medida = input(f"Descrição da prevenção: ")

                if not validar_informacoes_vazias(nm_vacina, nm_remedio, ds_medida):
                    continue

                dict_prevencao = {'nm_vacina': nm_vacina, 'ds_medida': ds_medida, 'nm_remedio': nm_remedio}
                return dict_prevencao
            elif previnir.lower() == 'n':
                print("OK, por favor insira informações de prevenção assim que descobertas!")
                dict_prevencao = {'nm_vacina': '-', 'ds_medida': '-', 'nm_remedio': '-'}
                return dict_prevencao  
        except ValueError as e:
            print(f"Ocorreu um erro: {e}")

# Função para edico inserir eventos (exames, vacinas,  etc.)
def eventos():
    lista_eventos = []

    while True:
        try:
            nm_evento = input("Inserir nome de evento ou digite 'sair' para terminar: ")
            if nm_evento.lower() == 'sair':
                break
            while True:
                dt_evento = input("Inserir data do evento: ")
                data_evento = validar_data(dt_evento)
                if data_evento is not None:
                    break
            tp_evento = input("Qual tipo de evento (Exames, vacinas, etc.): ")

            if not validar_informacoes_vazias(nm_evento, dt_evento, tp_evento):
               continue
            
            evento = {'Nome_evento': nm_evento, 'Data': dt_evento, 'Tipo_evento': tp_evento}
            lista_eventos.append(evento)

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            continue

    return lista_eventos

# Função para o medico atualizar os eventos
def atualizar_evento_medico(conn, id_evento):

    cursor = conn.cursor()
    try:
        while True:
            novo_nome_evento = input("Novo nome do evento: ")
            nova_data_evento = input("Nova data do evento (DD/MM/AAAA): ")
            novo_tipo_evento = input("Novo tipo do evento: ")

            if validar_informacoes_vazias(novo_nome_evento, nova_data_evento, novo_tipo_evento):
                continue
            cursor.execute('''UPDATE T_MDV_EVENTOS 
                              SET nm_evento = :novo_nome, 
                                  tp_evento = :novo_tipo, 
                                  dt_marcada = TO_DATE(:nova_data, 'DD/MM/YYYY')
                              WHERE id_evento = :id''',
                           {'novo_nome': novo_nome_evento, 'novo_tipo': novo_tipo_evento, 'nova_data': nova_data_evento, 'id': id_evento})
            conn.commit()

            print("Evento do médico atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao atualizar evento do médico: {e}")
    finally:
        cursor.close()

# Função para o medico excluir os eventos
def excluir_evento_medico(conn, id_evento):
    cursor = conn.cursor()

    try:
        print(f"Tentando excluir evento com ID {id_evento}")
        cursor.execute('''DELETE FROM T_MDV_EVENTOS 
                          WHERE id_evento = :id''',
                       {'id': id_evento})
        conn.commit()

        print("Evento do médico excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir evento do médico: {e}")
    finally:
        cursor.close()

#Seleciona atraves do id o evento que deseja atualizar ou excluir 
def selecionar_evento_para_crud():
    while True:
        try:
            id_escolhido = int(input("Escolha o ID do evento que deseja atualizar (ou 0 para sair): "))
            if id_escolhido == 0:
                print("Saindo...")
                return 0
            elif id_escolhido > 0:
                return id_escolhido
            else:
                print("Por favor, insira um número válido.")
        except ValueError as e:
            print(f"Ocorreu um erro: {e}")

# Função para usuário favoritar as vacinas que deseja
def calendario_eventos():
    lista_eventos = []
    
    while True:
        try:
            inserir = input("Deseja adicionar algum evento no seu calendario S/N: ")
            if inserir.lower() == 's':
                print("Informe os seguintes dados para adicionar ao seu calendário:")
                nome_evento = input("Inserir nome de evento ou digite 'sair' para terminar: ")
                if nome_evento.lower() == 'sair':
                    break
                
                while True:
                    data_evt = input("Inserir data do evento (DD/MM/AAAA): ")
                    data_evento = validar_data(data_evt)
                    if data_evento is not None:
                        break
                tipo_evento = input("Qual tipo de evento (Exames, vacinas, etc.): ")
                
                evento = {'Nome_evento': nome_evento, 'Data': data_evento, 'Tipo_evento': tipo_evento}
                lista_eventos.append(evento)

            else:
                break

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    return lista_eventos

# Função onde o usuario pode ver as doenças de cada epoca do ano 
def doenca_epoca_ano():
    try:
        opcoes_menu_principal = ["Verão", "Inverno", "Outono", "Primavera"]
        epoca = exibir_menu(opcoes_menu_principal)
        
        opcoes_menu_idade = ["Criança/Adolescente", "Adulto", "Idoso"]
        idade = exibir_menu(opcoes_menu_idade)
        
        doencas = textos()

        chave = ''
        if idade == 1:
            chave += 'crianca_'
        elif idade == 2:
            chave += 'adulto_'
        elif idade == 3:
            chave += 'idoso_'
        
        if epoca == 1:
            chave += 'verao'
        elif epoca == 2:
            chave += 'inverno'
        elif epoca == 3:
            chave += 'outono'
        elif epoca == 4:
            chave += 'primavera'
        
        if chave in doencas:  
            descricao = doencas[chave]['Doenças']
            prevencao = doencas[chave]['prevencao']
            print(f"\nDescrição: {descricao}")
            print(f"Prevenção: {prevencao}")
        else:
            print("\nInformações não encontradas para esta combinação de época e idade.")
    except Exception as e:
        print(f"Ocorreu um erro:{e}")

# Função com a doenças de cada epoca do ano 
def textos():
    doenças = {
        'crianca_verao': {
            'Doenças': 'Queimaduras Solares e Insolação',
            'prevencao': 'Use protetor solar, roupas leves, evite exposição direta ao sol durante as horas mais quentes e hidrate-se regularmente.',
            'Doenças2': 'Dengue',
            'prevencao2': 'Elimine locais de reprodução do mosquito, use repelentes, mantenha-se dentro de casa durante o amanhecer e entardecer.'
        },
        'crianca_inverno': {
            'Doenças': 'Gripes, Resfriados, Asma e Problemas de Pele ',
            'prevencao': 'Lave as mãos frequentemente, evite contato próximo com pessoas doentes, mantenha vacinação atualizada e use um umidificador para evitar o ar seco.',
            'Doenças2': 'Bronquite',
            'prevencao2': 'Evite fumar e ambientes com fumaça, mantenha-se aquecido, evite exposição ao ar frio e úmido.'
        },
        'crianca_outono': {
            'Doenças': 'Alergias Sazonais, Resfriados e Asma ',
            'prevencao': 'Evite contato com alérgenos conhecidos, mantenha a higiene pessoal, evite ambientes com poluição do ar e siga o tratamento prescrito para asma, se aplicável.'
        },
        'crianca_primavera': {
            'Doenças': 'Alergias Sazonais, Asma e Conjuntivite ',
            'prevencao': 'Evite exposição a alérgenos como pólen, mantenha as janelas fechadas em dias de alta contagem de pólen, use óculos de sol e siga as orientações do médico para alergias.'
        },
        'adulto_verao': {
            'Doenças': 'Insolação, Desidratação e Infecções Gastrointestinais ',
            'prevencao': 'Beba bastante água, evite exposição prolongada ao sol, use roupas leves, mantenha a higiene alimentar e evite alimentos perecíveis em condições inadequadas.',
            'Doenças2': 'Doenças Transmitidas por Alimentos',
            'prevencao2': 'Mantenha a higiene ao cozinhar, evite alimentos crus ou mal cozidos, lave bem os alimentos e mantenha-os armazenados corretamente.'
        },
        'adulto_inverno': {
            'Doenças': 'Gripes, Resfriados e Infecções Respiratórias',
            'prevencao': 'Mantenha-se aquecido, evite contato próximo com pessoas doentes, vacine-se contra a gripe e mantenha a higiene pessoal.',
            'Doenças2': 'Doença Pulmonar Obstrutiva Crônica (DPOC)',
            'prevencao2': 'Evite fumar e ambientes com fumaça, mantenha-se longe de poluentes do ar e siga o plano de tratamento prescrito.'
        },
        'adulto_outono': {
            'Doenças': 'Alergias Sazonais, Resfriados, Gripe e Asma',
            'prevencao': 'Evite contato com alérgenos conhecidos, mantenha a higiene pessoal, evite ambientes com poluição do ar e siga o tratamento prescrito para asma, se aplicável.'
        },
        'adulto_primavera': {
            'Doenças': 'Alergias Sazonais, Asma, Sinusite e Rinite',
            'prevencao': 'Evite exposição a alérgenos como pólen, mantenha as janelas fechadas em dias de alta contagem de pólen, use óculos de sol e siga as orientações do médico para alergias.'
        },
        'idoso_verao': {
            'Doenças': 'Golpes de Calor, Desidratação e Insolação ',
            'prevencao': 'Mantenha-se hidratado, evite exposição prolongada ao sol, use roupas frescas, procure ambientes com ar condicionado e mantenha acompanhamento médico regular.',
            'Doenças2': 'Hipertermia',
            'prevencao2': 'Evite ambientes muito quentes, mantenha-se hidratado, use roupas leves e fique em locais frescos durante os períodos de calor extremo.'
        },
        'idoso_inverno': {
            'Doenças': 'Complicações de Saúde Crônicas e Quedas/Lesões ',
            'prevencao': 'Mantenha acompanhamento médico regular, siga o plano de tratamento e tenha cuidado ao caminhar em superfícies escorregadias.',
            'Doenças2': 'Hipotermia',
            'prevencao2': 'Mantenha-se aquecido, use roupas adequadas, evite ambientes muito frios por períodos prolongados e mantenha a casa aquecida.'
        },
        'idoso_outono': {
            'Doenças': 'Alergias Sazonais, Gripe, Asma e Condições Cardiorrespiratórias ',
            'prevencao': 'Evite contato com alérgenos conhecidos, mantenha a higiene pessoal, evite ambientes com poluição do ar e siga o tratamento prescrito para asma, se aplicável.'
        },
        'idoso_primavera': {
            'Doenças': 'Alergias Sazonais, Problemas Respiratórios e Reações Alérgicas ',
            'prevencao': 'Evite exposição a alérgenos como pólen, mantenha as janelas fechadas em dias de alta contagem de pólen, use óculos de sol e siga as orientações do médico para alergias.'
        }
    }

    return doenças

# Função para exibir as novas doenças e suas prevenções 
def exibir_doencas_prevencao():
    try:
        conn = obter_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.*, m.nm_vacina, m.ds_medida, m.nm_remedio
            FROM T_MDV_DOENCAS d
            LEFT JOIN T_MDV_MEDIDAS m ON d.id_doenca = m.id_doenca
            ORDER BY d.id_doenca
        ''')
        doencas_prevencoes = cursor.fetchall()

        if doencas_prevencoes:
            id_doenca_atual = None
            for i in doencas_prevencoes:
                if i[0] != id_doenca_atual:
                    id_doenca_atual = i[0]
                    print("")
                    print(f"Nome: {i[0]}, Tipo: {i[1]}, Faixa Etária: {i[2]}, Descrição: {i[3]}")
                    print("Prevenções associadas:")

                if i[5]:
                    print(f"Vacina: {i[6]}, Descrição: {i[7]}, Remédio: {i[8]}")
                else:
                    print("Sem informações de prevenção disponíveis.")

                print("")  

            exportar = input("Deseja exportar essas informações NOVAS DOENÇAS para um arquivo JSON? (S/N): ")
            if exportar.lower() == 's':
                exportar_doencas_para_json()
            else:
                print("Exportação para JSON cancelada.")
        else:
            print("Não há informações de doenças cadastradas ou de prevenções associadas.")
    except Exception as e:
        print(f"Erro ao buscar informações de doenças e prevenções: {e}")
    finally:
        cursor.close()
        close_connection(conn)

# Função para o usuario deletar os eventos
def excluir_evento_calendario(usuario_logado):
    conn = obter_connection()
    cursor = conn.cursor()

    try:
        id_usuario = usuario_logado['id'] 

        exibir_calendario(usuario_logado)

        id_evento_para_deletar = selecionar_evento_para_crud()
        if id_evento_para_deletar == 0:
            return

        sql_query = ('''
            DELETE FROM T_MDV_CALENDARIO 
            WHERE id_calendario = :id_calendario AND id_usuario = :id_usuario
        ''')

        cursor.execute(sql_query, {'id_calendario': id_evento_para_deletar, 'id_usuario': id_usuario})
        conn.commit()
        print("Evento deletado com sucesso.")
    except oracledb.DatabaseError as e:
        print(f"Erro ao deletar evento do calendário: {e}")
    finally:
        cursor.close()
        close_connection(conn)

# Exibe eventos na area da saúde 
def exibir_eventos_medico(conn):
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT id_evento, nm_evento, tp_evento, TO_CHAR(dt_marcada, 'DD/MM/YYYY') FROM T_MDV_EVENTOS''')
        eventos = cursor.fetchall()

        if eventos:
            print("Eventos do médico:")
            for evento in eventos:
                print(f"ID: {evento[0]}, Nome: {evento[1]}, Tipo: {evento[2]}, Data: {evento[3]}")
            exportar = input("Deseja exportar esses eventos para um arquivo JSON? (S/N): ")
            if exportar.lower() == 's':
                exportar_eventos_para_json(conn)
            else:
                print("Exportação para JSON cancelada.")
        else:
            print("Não há eventos cadastrados ")
    except Exception as e:
        print(f"Erro ao buscar eventos do médico: {e}")
    finally:
        cursor.close()

# Exibe os eentos adicionados com favoritos
def exibir_calendario(usuario_logado):
    conn = obter_connection()
    cursor = conn.cursor()
    
    try:
        id_usuario = usuario_logado['id']
        sql_query = ('''
            SELECT id_calendario, dt_marcada, nm_evento, tp_evento 
            FROM T_MDV_CALENDARIO 
            WHERE id_usuario = :id_usuario
        ''')
        
        cursor.execute(sql_query, {'id_usuario': id_usuario})
        
        calendario = cursor.fetchall()
        if calendario:
            for i in calendario:
                id_calendario, dt_marcada, nm_evento, tp_evento = i
                formatted_date = dt_marcada.strftime('%d-%m-%Y')
                print(f"ID: {id_calendario}, Data: {formatted_date}, Evento: {nm_evento}, Tipo: {tp_evento}")
        else:
            print("Nenhum evento encontrado para este usuário.")
    except oracledb.DatabaseError as e:
        print(f"Erro ao ler dados da tabela T_MDV_CALENDARIO: {e}")

# Definição da função exportar_para_json
def exportar_para_json(nome_arquivo, dados):
    try:
        try:
            with open(nome_arquivo, 'r') as json_file:
                # Carrega os dados existentes do arquivo JSON 
                dados_existentes = json.load(json_file)
        except FileNotFoundError:
            dados_existentes = []
    except Exception as e:
        print(f"Ocorreu um erro {e}")
        return

    dados_existentes.extend(dados)

    # Abre o arquivo JSON no modo de escrita ('w')
    with open(nome_arquivo, 'w') as json_file:
        json.dump(dados_existentes, json_file, indent=4)
        
    print(f"Dados exportados para '{nome_arquivo}'")

# Exportar informação pra um arquivo json
def exportar_eventos_para_json(conn):
    conn = obter_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT id_evento, nm_evento, tp_evento, TO_CHAR(dt_marcada, 'DD/MM/YYYY') FROM T_MDV_EVENTOS''')
        eventos = cursor.fetchall()

        if eventos:
            json_eventos = []
            for evento in eventos:
                evento_dict = {
                    'TITULO': 'EVENTOS',
                    'Nome': evento[1],
                    'Tipo': evento[2],
                    'Data': evento[3]
                }
                json_eventos.append(evento_dict)

            exportar_para_json('informacoes.json', json_eventos)
        else:
            print("Não há eventos cadastrados")
    except Exception as e:
        print(f"Erro ao exportar eventos para JSON: {e}")

        cursor.close()
        close_connection(conn)

# Exportar informação pra um arquivo json
def exportar_calendario_para_json():
    conn = obter_connection()
    cursor = conn.cursor()
    
    try:
       
        sql_query = ('''
            SELECT id_calendario, dt_marcada, nm_evento, tp_evento FROM T_MDV_CALENDARIO WHERE id_usuario = :id_usuario
        ''')
        
        calendario = cursor.fetchall()
        if calendario:
            json_calendario = []
            for evento in calendario:
                dt_marcada, nm_evento, tp_evento = evento
                formatted_date = dt_marcada.strftime('%d-%m-%Y')

                evento_dict = {
                    'TITULO': 'CALENDARIO',
                    'Data': formatted_date,
                    'Evento': nm_evento,
                    'Tipo': tp_evento
                }
                json_calendario.append(evento_dict)

            exportar_para_json('informacoes.json', json_calendario)
        else:
            print("Nenhum evento encontrado para este usuário.")
    except oracledb.DatabaseError as e:
        print(f"Erro ao exportar dados do calendário do usuário para JSON: {e}")
    finally:
        cursor.close()
        close_connection(conn)

# Exportar informação pra um arquivo json
def exportar_doencas_para_json():
    try:
        conn = obter_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id_doenca, nm_doenca, tp_doenca, fx_etaria, ds_doenca
            FROM T_MDV_DOENCAS
            ORDER BY id_doenca
        ''')
        doencas_prevencoes = cursor.fetchall()

        doencas_info = []  # Agora estamos usando uma lista de dicionários

        if doencas_prevencoes:
            for i in doencas_prevencoes:
                id_doenca, nome, tipo, faixa_etaria, descricao = i

                doenca = {
                    'TITULO': 'NOVAS DOENAS',
                    'Nome': nome,
                    'Tipo': tipo,
                    'Faixa Etária': faixa_etaria,
                    'Descrição': descricao,
                }
                doencas_info.append(doenca)  # Adicionando o dicionário à lista

            with open('informacoes.json', 'w') as json_file:
                json.dump(doencas_info, json_file, indent=4)

            print("As informações das doenças foram exportadas para 'informacoes.json' com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# DEFS UTIZADO PARA PROGRAMA PRINCIPAL
def realizar_operacoes_usuario():
    usuario_logado = login()
    while True:
        opcoes_menu_principal = ["Donenças em Determinadas épocas", "Novas Doenças", "Eventos(Vacinas, exames)", "Visualizar Calendário de eventos", "deletar evento do calendario", "Sair"]
        menu_pri = exibir_menu(opcoes_menu_principal)

        if menu_pri == 1: 
            doenca_epoca_ano()
        elif menu_pri == 2:
            exibir_doencas_prevencao()
        elif menu_pri == 3:
            operacoes_calendario(usuario_logado)
        elif menu_pri == 4:
            exibir_calendario(usuario_logado)
        elif menu_pri == 5:
            excluir_evento_calendario(usuario_logado)
        else:
            exit_program()

def operacoes_calendario(usuario_logado):
    try:
        conn = obter_connection()
        if conn:
            exibir_eventos_medico(conn)
            evento = calendario_eventos()
            id_usuario = usuario_logado['id']
            inserir_dados_calendario(conn, id_usuario, evento)
            close_connection(conn)
        else:
            print("Erro ao conectar ao banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def cadastrar_usuario():
    dados_cadastro = cadastro()
    conn = obter_connection()
    if conn:
        id_usuario = inserir_dados_registro(conn, dados_cadastro)
        contato = tipo_contato()

        if id_usuario:
            inserir_dados_contato(conn, id_usuario, contato)
        close_connection(conn)
    else:
        print("Erro ao conectar ao banco de dados.")

def cadastrar_medico():
    dados_medico = cadastro_medico()
    conn = obter_connection()
    if conn:
        try:
            inserir_dados_medico(conn, dados_medico)
        finally:
            close_connection(conn)
    else:
        print("Erro ao conectar ao banco de dados.")

def operacoes_medico():
    dados_login = login()
    while True:
        opcoes_menu_medico = ["Inserir Eventos", "Excluir Eventos", "Atualizar Eventos", "Informar novas doenças", "Sair"]
        medico = exibir_menu(opcoes_menu_medico)

        if medico == 1:
            operacoes_medico_1()
        elif medico == 2:
            operacoes_medico_2()
        elif medico == 3:
            operacoes_medico_3()
        elif medico == 4:
            operacoes_medico_4(dados_login)
        elif medico == 5:
            exit_program()

def obter_nome_e_senha(crm):
    conn = obter_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT nm_usuario , nm_senha FROM T_MDV_REGISTRO_ESPECIALISTA WHERE nr_crm = :crm", {'crm': crm})
        
        # Obtendo os resultados
        resultado = cursor.fetchone()
        
        if resultado:
            nome_usuario = resultado[0]
            senha_usuario = resultado[1]
            return nome_usuario, senha_usuario
        else:
            print("Nome de usuário e senha não encontrados para o CRM fornecido.")
            return None, None

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")
        return None, None
    finally:
        cursor.close()
        close_connection(conn)
    
def operacoes_medico_1():
    while True:
        crm = input("Confirme seu CRM: ")
        nome_usuario, senha_usuario = obter_nome_e_senha(crm)

        if verificar_crm_usuario(nome_usuario, crm):
            id_usuario = obter_id_medico_por_nome_e_senha(nome_usuario, senha_usuario)

            if id_usuario is not None:
                eventos_do_medico = eventos()
                conn = obter_connection()

                if conn:
                    try:
                        inserir_eventos_medico(conn, id_usuario, eventos_do_medico)
                    finally:
                        close_connection(conn)
                else:
                    print("Erro ao conectar ao banco de dados.")
            else:
                print("ID do usuário do especialista não encontrado ou é None.")
            break  # Sair do loop se tudo ocorrer bem
        else:
            print("CRM inválido para o usuário. Por favor, digite novamente.")

def operacoes_medico_2():
    try:
        conn = obter_connection()
        exibir_eventos_medico(conn)
        
        id_evento_para_excluir = selecionar_evento_para_crud()

        confirmacao = input("Tem certeza que deseja excluir o evento? (S/N): ")

        if confirmacao.upper() == 'S':
            excluir_evento_medico(conn, id_evento_para_excluir)
        else:
                print("Operação de exclusão cancelada.")
        close_connection(conn)
    except oracledb.Error as e:
        print(f"Erro ao excluir evento : {e}")

def operacoes_medico_3():
    try:
        conn = obter_connection()
        exibir_eventos_medico(conn)
        id_evento_para_atualizar = selecionar_evento_para_crud()
        if id_evento_para_atualizar == 0:
            return
        atualizar_evento_medico(conn, id_evento_para_atualizar)
            
        close_connection(conn)
    except oracledb.Error as e:
        print(f"Erro durante a atualização do evento médico: {e}")
            
def operacoes_medico_4(dados_login):
    while True:
        try:
            conn = obter_connection()
            crm = input("Confirme seu CRM: ")
            nome_usuario_logado = dados_login.get('Nome')

            if verificar_crm_usuario(nome_usuario_logado, crm):
                dados_doencas = novas_doencas()
                dados_prevencao = prevencao(dados_doencas)
                nome_doenca = dados_doencas["Nome"]
                inserir_novas_doencas(conn, dados_doencas, crm)
                inserir_prevencao(conn, dados_prevencao, nome_doenca)
                break  
            else:
                print("CRM inválido. Por favor, digite novamente.")
        except oracledb.Error as e:
            print(f"Erro ao inserir prevençoes/novas doenças: {e}")
        finally:
            close_connection(conn)

def exit_program():
    exit(print("Programa finalizado"))

def main():
    while True:
        opcoes_menu_principal = ["Login Usuário", "Cadastrar usuário", "Cadastrar médico", "Login médico", "Sair"]
        escolha = exibir_menu(opcoes_menu_principal)

        if escolha == 1:
            realizar_operacoes_usuario()
        elif escolha == 2:
            cadastrar_usuario()
        elif escolha == 3:
            cadastrar_medico()
        elif escolha == 4:
            operacoes_medico()
        elif escolha == 5:
            exit_program()

# principal
main()
