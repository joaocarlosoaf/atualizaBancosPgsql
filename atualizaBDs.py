import sys
import time
import psycopg2
import getpass

# Endereço de onde está o banco de dados
_HOST_BD = ''
# Porta do banco
_PORT_BD = ''
# SQL para capturar todos os nomes dos bancos. Obs: Deve-se colocar where caso algun banco nao precise passar pela atualizacao
_SQL_GET_NAMES_DB = "SELECT datname FROM pg_database;"
# Arquivo que contenha a QUERY. Pode estar em qualquer formato
_QUERY_FILE = ''

f = open(_QUERY_FILE, "r")
_SQL_TO_REPLY = f.read()

user_bd = sys.argv[1]
pass_bd = getpass.getpass("Insira a senha do usuário " + user_bd + ": ")

_log = ''

def _registerLog(msg):
    global _log
    _log += msg + "\n"
    print(msg)

try:

    _registerLog('Conectando a base ' + user_bd + '\n')

    connection = psycopg2.connect(user = user_bd,
                                  password = pass_bd,
                                  host = _HOST_BD,
                                  port = _PORT_BD,
                                  database = user_bd)

    cursor = connection.cursor()
    cursor.execute(_SQL_GET_NAMES_DB)
    records = cursor.fetchall()

    _registerLog('Conexão com a base ' + user_bd + ' realizada com sucesso!\n\n')

    for row in records:

        _registerLog('*********************************************************')
        _registerLog("Conectando ao banco " + row[0])
        try:
            connbd_filial = psycopg2.connect(user = user_bd,
                                    password = pass_bd,
                                    host = _HOST_BD,
                                    port = _PORT_BD,
                                    database = str(row[0]))
            cursor = connbd_filial.cursor()
            cursor.execute(_SQL_TO_REPLY)
            connbd_filial.commit()
            _registerLog("Banco " + str(row[0]) + " Atualizado com sucesso!")

        except (Exception, psycopg2.Error) as error :
            _registerLog("Erro ao conectar no banco " + str(row[0]) + " Razão:" + str(error))

        finally:
            if(connbd_filial):
                cursor.close()
                connbd_filial.close()
                _registerLog("Conexão com o banco " + str(row[0]) + " fechada!")
        _registerLog('*********************************************************')
        
        time.sleep(5)

except (Exception, psycopg2.Error) as error :
    _registerLog("Erro ao conectar no banco " + user_bd + "\nRazão:" + str(error) + "\n\n")
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            _registerLog("Conexão com o banco " + user_bd + " fechada!\n")

f= open(time.strftime("%d%m%Y") + "_atualizacaoBDs.log","w+")
f.write(_log)
f.close()