import xmltodict
import os
import zipfile
from tkinter import Tk, filedialog

class ExtratoNfce:
    def __init__(self):
        ...

    

    def extrair_campos_nfe(self,caminho_arquivo, campos_para_extrair):
        
        # Abrir e carregar o XML como dicionário
        with open(caminho_arquivo, 'rb') as arquivo_xml:
            dic_xml = xmltodict.parse(arquivo_xml)

        # Acessar a parte relevante da NFe
        inf_nfe = dic_xml.get("nfeProc", {}).get("NFe", {}).get("infNFe", {})

        # Dicionário para armazenar os dados extraídos
        dados_extraidos = {}

        # Iterar sobre os campos desejados
        for rotulo, caminho in campos_para_extrair.items():
            dado = inf_nfe
            try:
                # Percorre o caminho até o campo desejado
                for chave in caminho:
                    dado = dado.get(chave)
                dados_extraidos[rotulo] = dado
            except AttributeError:
                dados_extraidos[rotulo] = None  # ou "[Não encontrado]"

        return dados_extraidos

    def processar_pasta(self, caminho_pasta, campos_para_extrair):
            """
            Percorre a pasta informada, descompacta arquivos ZIP e processa todos os XML encontrados.
            """
            resultados = []
            for raiz, dirs, arquivos in os.walk(caminho_pasta):
                for nome_arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, nome_arquivo)

                    # Se for ZIP, descompactar
                    if nome_arquivo.lower().endswith('.zip'):
                        with zipfile.ZipFile(caminho_completo, 'r') as zip_ref:
                            zip_ref.extractall(raiz)  # Extrai na mesma pasta
                        print(f"Arquivo ZIP extraído: {nome_arquivo}")

                    # Se for XML, processar
                    elif nome_arquivo.lower().endswith('.xml'):
                        dados = self.extrair_campos_nfe(caminho_completo, campos_para_extrair)
                        if dados:
                            dados['Arquivo'] = nome_arquivo
                            resultados.append(dados)

            return resultados



#data = ExtratoNfce()

def main():
    # Dicionário com os campos que quero extrair e o caminho até eles
    campos = {
        "Nome do Emitente": ("emit", "xNome"),
        "CNPJ":( 'emit', 'CNPJ'),
        "Valor da Nota": ("total", "ICMSTot", "vNF"),
        
    }

    pasta = input("Digite o caminho da pasta com os XMLs (e ZIPs): ").strip()

    data = ExtratoNfce()
    resultado = data.processar_pasta(pasta, campos)

    total_nfe = 0
    print("\n=== Resultados ===\n")
    for item in resultado:
        for chave, valor in item.items():
            print(f"{chave}: {valor}")
        print("-" * 40)

        try:
            total_nfe += float(item.get("Valor da Nota", 0))
        except ValueError:
            pass

    print(f"\nValor Total de Todas as Notas: R$ {total_nfe:.2f}")

    # dados = data.extrair_campos_nfe("1 - nfe.xml", campos)
    # total_nfe = 0

    # # Exibindo os dados
    # print()
    # for chave, valor in dados.items():
    #     if chave in "Valor da Nota":
    #         total_nfe += float(valor)
    #     print(f"{chave}: {valor}")


    # print()
    # print(f"Valor total {total_nfe:.2f}")


main()