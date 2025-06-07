from data_functions import insert_fornecedor, insert_stacao


with open("inserts.sql", "w", encoding="UTF-8") as arquivo:
    arquivo.write("BEGIN" + "\n")
    for linhas in insert_fornecedor():
        arquivo.write("    " + linhas + "\n")
    for linhas in insert_stacao(50):
        arquivo.write("    " + linhas + "\n")
    arquivo.write("    " + "COMMIT;" + "\n")
    arquivo.write("EXCEPTION " + "\n")
    arquivo.write("    " + "WHEN OTHERS THEN" + "\n")
    arquivo.write("        " + "ROLLBACK;" + "\n")
    arquivo.write("END;" + "\n")
    arquivo.write("/" + "\n")
