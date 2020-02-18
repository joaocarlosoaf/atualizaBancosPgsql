# Atualiza Bancos Pgsql
Script para replicar Querys em diversos bancos postgres

Necessário:
* python3
* psycopg2

Observações:
Preencher todas as variaveis antes de rodar!
# Endereço de onde está o banco de dados
_HOST_BD = ''
# Porta do banco
_PORT_BD = ''
# SQL para capturar todos os nomes dos bancos. Obs: Deve-se colocar where caso algun banco nao precise passar pela atualizacao
_SQL_GET_NAMES_DB = "SELECT datname FROM pg_database;"
# Arquivo que contenha a QUERY. Pode estar em qualquer formato
_QUERY_FILE = ''

Uso:
python3 atualizaBDs.py seuusuariobd
