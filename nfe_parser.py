import xmltodict
import pandas as pd

def parse_nfe_xml(xml_file_path):
    with open(xml_file_path, 'rb') as arquivo_xml:
        dic_xml = xmltodict.parse(arquivo_xml)

    nfe_data = {}

    # Acessando o nó principal nfeProc
    nfe_proc = dic_xml.get('nfeProc')
    if not nfe_proc:
        print("Erro: Nó 'nfeProc' não encontrado no XML.")
        return None

    # Acessando o nó NFe
    nfe = nfe_proc.get('NFe')
    if not nfe:
        print("Erro: Nó 'NFe' não encontrado no XML.")
        return None

    # Acessando infNFe
    inf_nfe = nfe.get('infNFe')
    if not inf_nfe:
        print("Erro: Nó 'infNFe' não encontrado no XML.")
        return None

    # Extraindo dados do emitente
    emit = inf_nfe.get('emit')
    if emit:
        nfe_data['emit_xNome'] = emit.get('xNome')
        nfe_data['emit_CNPJ'] = emit.get('CNPJ')
    else:
        print("Aviso: Nó 'emit' não encontrado.")

    # Extraindo valor total da nota
    total = inf_nfe.get('total')
    if total:
        icms_tot = total.get('ICMSTot')
        if icms_tot:
            nfe_data['vNF'] = icms_tot.get('vNF')
        else:
            print("Aviso: Nó 'ICMSTot' não encontrado.")
    else:
        print("Aviso: Nó 'total' não encontrado.")

    # Verificando dados do recebedor (geralmente ausente em NFC-e)
    dest = inf_nfe.get('dest')
    if dest:
        nfe_data['dest_xNome'] = dest.get('xNome')
        nfe_data['dest_CNPJ'] = dest.get('CNPJ')
    else:
        nfe_data['dest_xNome'] = "Não informado (NFC-e)"
        nfe_data['dest_CNPJ'] = "Não informado (NFC-e)"
        print("Aviso: Nó 'dest' (destinatário) não encontrado. Isso é comum em NFC-e (modelo 65).")

    return nfe_data

def save_to_excel(data, output_file_path):
    df = pd.DataFrame([data])
    df.to_excel(output_file_path, index=False)
    print(f"Dados salvos com sucesso em {output_file_path}")

if __name__ == '__main__':
    xml_file = '/home/ubuntu/upload/1-nfe.xml'
    dados_extraidos = parse_nfe_xml(xml_file)

    if dados_extraidos:
        print("\nDados extraídos da NFe:")
        for key, value in dados_extraidos.items():
            print(f"{key}: {value}")
        
        output_excel_file = '/home/ubuntu/nfe_data.xlsx'
        save_to_excel(dados_extraidos, output_excel_file)


