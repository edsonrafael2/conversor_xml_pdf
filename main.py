from time import sleep
import xmltodict


with open("1 - nfe.xml", 'rb') as arquivo_xml:
    dic_xml = xmltodict.parse(arquivo_xml)

arquivo = (dic_xml['nfeProc'])
print(arquivo)

# for data in arquivo:
#     if 'xNome' in data:
#         print(data['xNome'])