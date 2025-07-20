import xmltodict

class ExtratoNfce:
    def __init__(self):
        pass

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




data = ExtratoNfce()
def main():
    # Dicionário com os campos que quero extrair e o caminho até eles
    campos = {
        "Nome do Emitente": ("emit", "xNome"),
        "CNPJ":( 'emit', 'CNPJ'),
        "Valor da Nota": ("total", "ICMSTot", "vNF"),
        
    }

    dados = data.extrair_campos_nfe("1 - nfe.xml", campos)
    total_nfe = 0

    # Exibindo os dados
    print()
    for chave, valor in dados.items():
        if chave in "Valor da Nota":
            total_nfe += float(valor)
        print(f"{chave}: {valor}")


    print()
    print(f"Valor total {total_nfe:.2f}")


main()