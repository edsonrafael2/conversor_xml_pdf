from tkinter import Tk, filedialog

def selecionar_pasta():
    """
    Abre uma janela para o usuário selecionar uma pasta com o mouse.
    """
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    root.attributes('-topmost', True)  # Garante que a janela fique em primeiro plano
    caminho = filedialog.askdirectory(title="Selecione a pasta com os arquivos XML ou ZIP")
    return caminho

def main():
    campos = {
        "Nome do Emitente": ("emit", "xNome"),
        "CNPJ": ("emit", "CNPJ"),
        "Valor da Nota": ("total", "ICMSTot", "vNF"),
    }

    pasta = selecionar_pasta()

    if not pasta:
        print("Nenhuma pasta foi selecionada. Encerrando...")
        return

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
