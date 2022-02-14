import Validator
import pandas as pd
from csv import writer
import xlsxwriter


# Function to write data into a "CSV" file
def appendDataIntoCSV(fileName, data):
    # Append the data into a list to write it correctly
    dataList = []
    dataList.append(data)
    # Open the existing file
    with open(f"C:\\Scripts\\separadorCPFCNPJ\\Retorno\\{fileName}.csv", 'a', newline='') as objectFile:
        # Pass this file object to csv.writer()
        objectWriter = writer(objectFile)
        # Pass the list as an argument into the writerow()
        objectWriter.writerow(dataList)
        # Close the file object
        objectFile.close()


# Function to write data into a "XLSX" file
def writeDataIntoXLSX(fileName, documentList):
    # Create an excel file to store the data
    workbook = xlsxwriter.Workbook(f"C:\\Scripts\\separadorCPFCNPJ\\Retorno\\{fileName}.xlsx")
    worksheet = workbook.add_worksheet("Planilha1")

    # Loop to fill the file with data
    for g in range(len(documentList)):
        # Store the data
        worksheet.write(f'A{g}', documentList[g])

    # Close the excel file
    workbook.close()


# Variable to control the CNPJ Raiz
formatCNPJ = 45


# Catch the file name
print("=-=" * 9)
fileName = str(input("Digite o nome do(s) arquivo(s) de retorno: "))

# See if the return will be "CSV" or "XLSX"
print("=-=" * 9)
returnType = int(input("""[0]CSV
[1]XLSX
Selecione o tipo de retorno: """))

# Declare the quantity of files that will return
print("=-=" * 9)
nFiles = int(input("Digite o número de arquivos que devem ser gerados: "))

# Create dataframe from excel and format it
df = pd.read_excel('C:\\Scripts\\separadorCPFCNPJ\\Entrada\\Documentos.xlsx', 'Planilha1')

if nFiles > 1:
    # Slice the dataframe
    nDocuments = len(df) // nFiles
    missingDocuments = len(df) % nFiles

    # Dict list to store the data of each file
    sliceList = df['DOCUMENTOS'].to_list()
    sliceDict = {}
    nSlice = 0
    for i in range(nFiles):
        if i == nFiles - 1:
            sliceSize = len(df)
        else:
            sliceSize = nSlice + nDocuments
        sliceDict[f'FATIA{i + 1}'] = sliceList[nSlice:sliceSize]
        nSlice += nDocuments
    for s in sliceDict:
        # Create a list to store CPF's and other to store CNPJ's
        listCPF = []
        listCNPJ = []
        for d in sliceDict[s]:
            # Call a function to see if it's a CPF or CNPJ
            validator = Validator.isCPF(str(d))

            # Format the respective document
            if validator:
                # Complete the CPF till it get's 11 digits
                formatedDocument = Validator.completeCPF(str(d))

                # Store the CPF's
                listCPF.append(formatedDocument)

            elif not validator:

                # Complete the CNPJ till it get's 14 digits
                formatedDocument = Validator.completeCNPJ(str(d))

                # Store the CNPJ's
                listCNPJ.append(formatedDocument)

            # Check the type of the return
            if returnType == 0:
                # Check if it has CPF into the entry file
                if len(listCPF) != 0:
                    for p in range(len(listCPF)):
                        appendDataIntoCSV(fileName + "CPF-" + s, listCPF[p])

                # Check if it has CNPJ into the entry file
                if len(listCNPJ) != 0:
                    for m in range(len(listCNPJ)):
                        appendDataIntoCSV(fileName + "CPNJ-" + s, listCNPJ[m])

            elif returnType == 1:
                # Check if it has CPF into the entry file
                if len(listCPF) != 0:
                    writeDataIntoXLSX(fileName + "CPF-" + s, listCPF)

                # Check if it has CNPJ into the entry file
                if len(listCNPJ) != 0:
                    # See the format of the CNPJ that will be returned
                    if formatCNPJ == 45:
                        print("=-=" * 9)
                        formatCNPJ = int(input("""[0]Não
[1]Sim
Deseja extrair apenas a raiz dos CNPJ: """))
                if formatCNPJ == 0:
                    writeDataIntoXLSX(fileName + "CPNJ-" + s, listCNPJ)
                elif formatCNPJ == 1:
                    fixedListCNPJ = []
                    for f in range(len(listCNPJ)):
                        fixedListCNPJ.append(listCNPJ[f][:8])
                    writeDataIntoXLSX(fileName + "RaizCPNJ-" + s, fixedListCNPJ)

elif nFiles == 1:
    # Create a list to store CPF's and other to store CNPJ's
    listCPF = []
    listCNPJ = []
    # Loop to check each document
    for h in range(len(df)):
        # Call a function to see if it's a CPF or CNPJ
        validator = Validator.isCPF(str(df.iloc[h]['DOCUMENTOS']))

        # Format the respective document
        if validator:
            # Complete the CPF till it get's 11 digits
            formatedDocument = Validator.completeCPF(str(df.iloc[h]['DOCUMENTOS']))

            # Store the CPF's
            listCPF.append(formatedDocument)

        elif not validator:
            # Complete the CNPJ till it get's 14 digits
            formatedDocument = Validator.completeCNPJ(str(df.iloc[h]['DOCUMENTOS']))

            # Store the CNPJ's
            listCNPJ.append(formatedDocument)

    # Check the type of the return
    if returnType == 0:
        # Check if it has CPF into the entry file
        if len(listCPF) != 0:
            for p in range(len(listCPF)):
                appendDataIntoCSV(fileName + "CPF", listCPF[p])

        # Check if it has CNPJ into the entry file
        if len(listCNPJ) != 0:
            for m in range(len(listCNPJ)):
                appendDataIntoCSV(fileName + "CPNJ", listCNPJ[m])

    elif returnType == 1:
        # Check if it has CPF into the entry file
        if len(listCPF) != 0:
            writeDataIntoXLSX(fileName + "CPF", listCPF)

        # Check if it has CNPJ into the entry file
        if len(listCNPJ) != 0:
            # See the format of the CNPJ that will be returned
            if formatCNPJ == 45:
                print("=-=" * 9)
                formatCNPJ = int(input("""[0]Não
[1]Sim
Deseja extrair apenas a raiz dos CNPJ: """))
            if formatCNPJ == 0:
                writeDataIntoXLSX(fileName + "CPNJ", listCNPJ)
            elif formatCNPJ == 1:
                fixedListCNPJ = []
                for f in range(len(listCNPJ)):
                    fixedListCNPJ.append(listCNPJ[f][:8])
                writeDataIntoXLSX(fileName + "RaizCPNJ", fixedListCNPJ)