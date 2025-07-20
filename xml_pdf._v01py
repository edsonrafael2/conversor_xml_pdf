import xmltodict

def extrair_campos_nfe(caminho_arquivo, campos_para_extrair):
    """
    Extrai campos específicos de um arquivo XML de NFe, usando os caminhos definidos.

    :param caminho_arquivo: str - caminho do arquivo XML
    :param campos_para_extrair: dict - chave (nome amigável) e valor (tupla de caminho no dicionário)
    :return: dict com os dados extraídos
    """
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




# Dicionário com os campos que quero extrair e o caminho até eles
campos = {
    "Nome do Emitente": ("emit", "xNome"),
    "CNPJ":( 'emit', 'CNPJ'),
    "Valor da Nota": ("total", "ICMSTot", "vNF"),
    "Número da Nota": ("ide", "nNF"),
    "Data de Emissão": ("ide", "dhEmi"),
    "Município de Destino": ("ide", "cMunFG"),
    "Nome Fantasia": ("emit", "xFant")
}

# Chamada da função
dados = extrair_campos_nfe("1 - nfe.xml", campos)

# Exibindo os dados
for chave, valor in dados.items():
    print(f"{chave}: {valor}")
