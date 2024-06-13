import re

def ReadDoc(filename:str):
    if not ".txt" in filename:
        filename = f"{filename}.txt"

    arq = open(f"..\\v1.0.1\\data\\{filename}", "r", encoding="utf-8")
    arqReadLines = arq.readlines()
    arq.close()

    all_data = []

    #;pk=[colum=valor,colum,valor....]
    for readLine in arqReadLines:
        parts = re.split(r'[\[\];{},]+', readLine)
        parts = list(filter(None,  parts))

        if len(parts) > 1:
            pk = parts[0]
            column_values = parts[1:]

            columns = []
            values = []

            for col_val in column_values:
                if ":" in col_val:
                    col, val = col_val.split(":")
                    columns.append(col)
                    values.append(val)

            all_data.append((pk, columns, values))
    return all_data

def AddDoc(filename:str, id, data):
    if not ".txt" in filename:
        filename = f"{filename}.txt"

    if type(data) is not dict:
        return False

    # ;[pk]={colum:valor,colum:valor,colum:valor,colum:valor,colum:valor,colum:valor}
    col_val_str = ",".join([f"{col}:{val}" for col, val in data.items()])

    final_str = f";[{id}]={{{col_val_str}}}\n"

    arq = open(f"..\\v1.0.1\\data\\{filename}", "a", encoding="utf-8")
    arq.write(final_str)
    arq.close()

    return True

def RemoveDoc(filename:str, id):
    if not ".txt" in filename:
        filename = f"{filename}.txt"

    arqRead = open(f"..\\v1.0.1\\data\\{filename}", "r", encoding="utf-8")
    removeRead = arqRead.readlines()
    arqRead.close()

    arqRewriteString = ""

    for verify_id in removeRead:
        parts = re.split(r'[\[\];{},\s]+', verify_id)
        parts = list(filter(None, parts))

        pk = parts[0]

        if str(pk) != str(id):
            arqRewriteString += verify_id

    arqRewrite = open(f"..\\v1.0.1\\data\\{filename}", "w", encoding="utf-8")
    arqRewrite.write(arqRewriteString)
    arqRewrite.close()

def UpdateDoc(filename:str, id, new_data):
    if not ".txt" in filename:
        filename = f"{filename}.txt"

    if type(new_data) is not dict:
        return False
    
    arq = open(f"..\\v1.0.1\\data\\{filename}", "r", encoding="utf-8")
    arqReadLines = arq.readlines()
    arq.close()

    updated_lines = ""

    for readLine in arqReadLines:
        parts = re.split(r'[\[\];{},\s]+', readLine)
        parts = list(filter(None, parts))

        if parts and str(parts[0]) == str(id):
            pk = parts[0]
            columns_values = [f"{col}:{val}" for col, val in new_data.items()]
            new_line = f";[{pk}]={{" + ",".join(columns_values) + "}\n"
            updated_lines += new_line
        else:
            updated_lines += readLine

        if str(parts[0]) != str(id):
            arq = open(f"..\\v1.0.1\\data\\{filename}", "w", encoding="utf-8")
            arq.write(readLine)
            arq.close()
    
    arq = open(f"..\\v1.0.1\\data\\{filename}", "w", encoding="utf-8")
    arq.write(updated_lines)
    arq.close()

    return True