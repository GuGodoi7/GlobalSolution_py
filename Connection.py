import oracledb

# Abre conexão com banco de dados 
def obter_connection():
    try:
        connection = oracledb.connect(user="RM99585", password="210305", dsn="oracle.fiap.com.br/orcl")
        return connection
    except Exception as e:
        print(f"Erro ao obter conexão: {e}")
        return None

# Fecha conexão com o banco de dados
def close_connection(connection):
    try:
        if connection:
            connection.close()
    except Exception as e:
        print(f"Erro ao fechar conexão: {e}")

# Inserir dados no banco
def inserir_dados_registro(conn, dados_cadastro):
    cursor = conn.cursor()
    try:
        # Insere T_MDV_REGISTRO
        cursor.execute('''INSERT INTO T_MDV_REGISTRO (id_usuario, nm_usuario, nm_senha) 
                           VALUES (seq_id_usuario.NEXTVAL, :nome, :senha)''',
                       {'nome': dados_cadastro['Nome'], 'senha': dados_cadastro['Senha']})
        conn.commit()

        # Obtém o valor atual da sequência
        cursor.execute("SELECT seq_id_usuario.CURRVAL FROM DUAL")
        id_usuario = cursor.fetchone()[0]

        # Insere dados na T_MDV_REGISTRO_CLIENTE
        sql_query_cliente = '''
            INSERT INTO T_MDV_REGISTRO_CLIENTE 
            (id_usuario, dt_nascimento, nm_usuario, nm_senha, nr_cep) 
            VALUES (:id, TO_DATE(:nascimento, 'DD/MM/YYYY'), :nome, :senha, :cep)
        '''

        cursor.execute(sql_query_cliente, {
            'id': id_usuario,
            'nome': dados_cadastro['Nome'],
            'senha': dados_cadastro['Senha'],
            'cep': dados_cadastro['Endereco'],
            'nascimento': dados_cadastro['Data de Nascimento']
        })

        conn.commit()


        print("Dados inseridos com sucesso.")
        return id_usuario  
    
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Erro ao inserir dados: {error.message}")
    finally:
        cursor.close()

# Inserir dados no banco
def inserir_dados_calendario(conn, id_usuario, lista_eventos):
    cursor = conn.cursor()
    
    try:
        sql_query = ('''
            INSERT INTO T_MDV_CALENDARIO 
            (dt_marcada, nm_evento, tp_evento, id_calendario, id_usuario) 
            VALUES (TO_DATE(:data_evento, 'DD-MM-YYYY'), :nome_evento, :tipo_evento, seq_id_calendario.NEXTVAL, :id_usuario)
        ''')
        
        for evento in lista_eventos:
            cursor.execute(sql_query, {
                'id_usuario': id_usuario,
                'data_evento': evento['Data'],
                'nome_evento': evento['Nome_evento'],
                'tipo_evento': evento['Tipo_evento'],
            })
        conn.commit()
        print("Dados inseridos com sucesso")
    except oracledb.DatabaseError as e:
        print(f"Erro ao inserir dados na tabela T_MDV_CALENDARIO: {e}")

# Inserir dados no banco
def inserir_dados_contato(conn, id_usuario, contato):
    cursor = conn.cursor()
    try:
        sql_query = ('''INSERT INTO T_MDV_CONTATO 
                          (tp_contato, nr_telefone, nm_email, id_usuario) 
                          VALUES (:tipo_contato, :telefone, :email, :id_usuario)''')
                          
        cursor.execute(sql_query, {
            'tipo_contato': contato['tp_contato'], 
            'telefone': contato.get('telefone'), 
            'email': contato.get('email'), 
            'id_usuario': id_usuario})
        
        conn.commit()

        print("Dados de contato inseridos com sucesso.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Erro ao inserir dados de contato: {error.message}")
    finally:
        cursor.close()

# Inserir dados no banco
def inserir_dados_medico(conn, dados_medico):
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO T_MDV_REGISTRO (id_usuario, nm_usuario, nm_senha) 
                           VALUES (seq_id_usuario.NEXTVAL, :nome, :senha)''',
                       {'nome': dados_medico['nome'], 'senha': dados_medico['senha']})
        conn.commit()

    
        cursor.execute("SELECT seq_id_usuario.CURRVAL FROM DUAL")
        id_usuario = cursor.fetchone()[0]

        sql_query = ('''INSERT INTO T_MDV_REGISTRO_ESPECIALISTA 
                            (id_usuario, nm_usuario, nm_senha, nr_crm) 
                            VALUES (:id, :nome, :senha, :crm)''')
        cursor.execute(sql_query,{
        'id': id_usuario, 
        'nome': dados_medico['nome'],
        'senha': dados_medico['senha'], 
        'crm': dados_medico['crm']})
        conn.commit()

        print("Dados do médico inseridos com sucesso.")
        return id_usuario 
    except oracledb.Error as e:
        print(f"Erro ao inserir dados do médico: {e}")
    finally:
        cursor.close()

# Inserir dados no banco
def inserir_eventos_medico(conn, id_usuario, lista_eventos):
    cursor = conn.cursor()

    try:
        for evento in lista_eventos:
            sql_query = ('''INSERT INTO T_MDV_EVENTOS 
            (id_evento, id_usuario, nm_evento, tp_evento, dt_marcada) 
            VALUES (seq_id_evento.NEXTVAL, :id_usuario, :nm_evento, :tp_evento, TO_DATE(:dt_evento, 'DD/MM/YYYY'))''')
            cursor.execute(sql_query,
            {'id_usuario': id_usuario, 
             'nm_evento': evento['Nome_evento'], 
             'tp_evento': evento['Tipo_evento'], 
             'dt_evento': evento['Data']})
            conn.commit()

        print("Eventos do médico inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir eventos do médico: {e}")
    finally:
        cursor.close()  

# Inserir dados no banco
def inserir_prevencao(conn, dados_prevenca, nome):
    id_doenca = obter_id_doenca_por_nome(nome)

    cursor = conn.cursor()
    try:
        sql_query  = ('''
        INSERT INTO T_MDV_MEDIDAS
        (id_vacina, nm_vacina, ds_medida, nm_remedio, id_doenca) 
        VALUES (seq_id_vacina.NEXTVAL, :nm_vacina, :ds_medida, :nm_remedio,  :id_doenca)
            ''')
        cursor.execute(sql_query, {
        'nm_vacina': dados_prevenca['nm_vacina'],
        'ds_medida': dados_prevenca['ds_medida'],
        'nm_remedio': dados_prevenca['nm_remedio'],
        'id_doenca': id_doenca 
            })
        conn.commit()

        print("Dados prevenção inseridos com sucesso.")
    except oracledb.Error as error:
        print(f"Erro ao inserir dados das prevenções: {error}")
    finally:
        cursor.close()

# Inserir dados no banco
def inserir_novas_doencas(conn, info_doenca, crm):
    id_usuario = obter_id_usuario_por_crm(crm) 

    if id_usuario is None:
        print("CRM não encontrado ou usuário não existe.")
        return

    cursor = conn.cursor()
    try:
        sql_query = ('''
                INSERT INTO T_MDV_DOENCAS 
                (nm_doenca, tp_doenca, fx_etaria, ds_doenca, id_usuario, id_doenca) 
                VALUES (:nome_doenca, :tipo_doenca, :faixa_etaria, :descricao_doenca, :id_usuario, seq_id_doenca.NEXTVAL)
            ''')
        cursor.execute(sql_query,{
                'nome_doenca': info_doenca['Nome'],
                'tipo_doenca': info_doenca['Tipo Doença'],
                'faixa_etaria': info_doenca['Faixa Etária'],
                'descricao_doenca': info_doenca['Descrição'],
                'id_usuario': id_usuario 
            })
        conn.commit()

        print("Dados das novas doenças inseridos com sucesso.")
    except oracledb.Error as e:
        print(f"Erro ao inserir dados das novas doenças: {e}")
    finally:
        cursor.close()

# pega o id do medico pelo crm
def obter_id_usuario_por_crm(crm):
    conn = obter_connection()
    cursor = conn.cursor()

    id_usuario = None

    try:
        consulta_sql = "SELECT id_usuario FROM T_MDV_REGISTRO_ESPECIALISTA WHERE nr_crm = :crm"
        cursor.execute(consulta_sql, {'crm': crm})  
        resultado = cursor.fetchone()

        if resultado:
            id_usuario = resultado[0]

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")

    finally:
        cursor.close()
        close_connection(conn)

    return id_usuario

# pega id do usuario pelo nome senha 
def obter_id_usuario_por_nome_e_senha(nome_usuario, senha_usuario):
    conn = obter_connection()
    cursor = conn.cursor()

    id_usuario = None

    try:
        consulta_sql = "SELECT id_usuario FROM T_MDV_REGISTRO_CLIENTE  WHERE nm_usuario = :nome_usuario AND nm_senha = :senha_usuario"
        cursor.execute(consulta_sql, {'nome_usuario': nome_usuario, 'senha_usuario': senha_usuario})
        resultado = cursor.fetchone()

        if resultado:
            id_usuario = resultado[0]

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")

    finally:
        cursor.close()
        close_connection(conn)

    return id_usuario

# pega id do medico pelo nome senha 
def obter_id_medico_por_nome_e_senha(nome_usuario, senha_usuario):
    conn = obter_connection()
    cursor = conn.cursor()

    id_usuario = None

    try:
        consulta_sql = "SELECT id_usuario FROM T_MDV_REGISTRO  WHERE nm_usuario = :nome_usuario AND nm_senha = :senha_usuario"
        cursor.execute(consulta_sql, {'nome_usuario': nome_usuario, 'senha_usuario': senha_usuario})
        resultado = cursor.fetchone()

        if resultado:
            id_usuario = resultado[0]

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")

    finally:
        cursor.close()
        close_connection(conn)

    return id_usuario

#pegar o id da doença pelo nome dela
def obter_id_doenca_por_nome(nm_doenca):
    conn = obter_connection()
    cursor = conn.cursor()

    id_doenca = None

    try:
        consulta_sql = "SELECT id_doenca FROM T_MDV_DOENCAS WHERE nm_doenca = :nm_doenca"
        cursor.execute(consulta_sql, {'nm_doenca': nm_doenca})  
        resultado = cursor.fetchone()

        if resultado:
            id_doenca = resultado[0]

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")

    finally:
        cursor.close()
        close_connection(conn)

    return id_doenca

# pegar o id do calendario pelo usario logado
def obter_id_calendario_por_usuario(usuario_logado):
    conn = obter_connection()
    cursor = conn.cursor()
    
    id_usuario = usuario_logado['id']

    try:
        sql_query = ('''
            SELECT id_calendario
            FROM T_MDV_CALENDARIO 
            WHERE id_usuario = :id_usuario
        ''')
        
        cursor.execute(sql_query, {'id_usuario': id_usuario})
        
        rows = cursor.fetchall()
        if rows:
            id_calendarios = [row[0] for row in rows]  # Lista de id_calendario do usuário
            return id_calendarios
        else:
            print("Nenhum evento encontrado para este usuário.")
            return []
    except oracledb.DatabaseError as e:
        print(f"Erro ao buscar id_calendario por usuário: {e}")
        return []
    finally:
        cursor.close()
        close_connection(conn)

# pegar o crm pelo nome e senha do medico
def obter_nr_crm_por_nome_e_senha(nome_medico, senha_medico):
    conn = obter_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT nr_crm FROM T_MDV_REGISTRO_ESPECIALISTA 
                           WHERE nm_usuario = :nome_medico AND nm_senha = :senha_medico''',
                       {'nome_medico': nome_medico, 'senha_medico': senha_medico})
        nr_crm = cursor.fetchone()

        if nr_crm:
            return nr_crm[0]  
        else:
            print("Médico não encontrado ou credenciais incorretas.")
            return None

    except oracledb.Error as e:
        print(f"Erro ao obter número do CRM: {e}")
        return None

    finally:
        cursor.close()
        close_connection(conn)

# Verificar se o crm é do usuario
def verificar_crm_usuario(nome_usuario, crm_fornecido):
    conn = obter_connection()
    cursor = conn.cursor()

    valido = False

    try:
        consulta_sql = """
        SELECT COUNT(*) 
        FROM T_MDV_REGISTRO_ESPECIALISTA E
        INNER JOIN T_MDV_REGISTRO U ON E.id_usuario = U.id_usuario
        WHERE U.nm_usuario = :nome_usuario AND E.nr_crm = :crm
        """
        cursor.execute(consulta_sql, {'nome_usuario': nome_usuario, 'crm': crm_fornecido})
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            valido = True

    except oracledb.Error as e:
        print(f"Erro ao executar consulta: {e}")

    finally:
        cursor.close()
        close_connection(conn)

    return valido
