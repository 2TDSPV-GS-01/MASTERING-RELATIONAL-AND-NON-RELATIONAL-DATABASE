from sqlalchemy import create_engine
import cx_Oracle
import os

# Inicializa o Oracle Client (se necessário)
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\instantclient_23_5")
except cx_Oracle.ProgrammingError:
    pass  # já inicializado

def get_engine():
    user = "francesco"
    password = "rm557313"
    host = "74.163.240.0"
    port = "1521"
    service_name = "XEPDB1"

    dsn = cx_Oracle.makedsn(
    host="74.163.240.0",
    port=1521,
    service_name="XEPDB1"
    )

    return create_engine(
        f"oracle+cx_oracle://francesco:rm557313@{dsn}"
    )

    # return create_engine(
    #     f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{service_name}"
    # )