from time import sleep
import xmltodict
import pandas as pd


with open("1 - nfe.xml", 'rb') as arquivo_xml:
    dic_xml = xmltodict.parse(arquivo_xml)


    print(dic_xml)
    # xml = dic_xml['nfeProc']
    # print(xml)
    # for k, v in xml:
    #     if k == 'xBairro':
    #         print(v)