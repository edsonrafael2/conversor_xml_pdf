import flet as ft
from main import ExtratoNfce, selecionar_pasta

def main(page: ft.Page):
    page.title = "Leitor de Notas Fiscais XML"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    titulo = ft.Text("Extrator de XML/ZIP - NFC-e", size=24, weight="bold")
    resultado_view = ft.Column()
    total_text = ft.Text("")
    itens_text = ft.Text("")

    def selecionar_e_processar(e):
        resultado_view.controls.clear()
        total_text.value = ""
        itens_text.value = ""

        pasta = selecionar_pasta()
        if not pasta:
            resultado_view.controls.append(ft.Text("Nenhuma pasta selecionada.", color="red"))
            page.update()
            return

        campos = {
            "Nome do Emitente": ("emit", "xNome"),
            "CNPJ": ("emit", "CNPJ"),
            "Valor da Nota": ("total", "ICMSTot", "vNF"),
        }

        extrator = ExtratoNfce()
        resultados = extrator.processar_pasta(pasta, campos)

        total_nfe = 0
        total_itens = 0

        for item in resultados:
            total_itens += 1
            campos_formatados = "\n".join([f"{k}: {v}" for k, v in item.items()])
            resultado_view.controls.append(ft.Text(campos_formatados, selectable=True))
            resultado_view.controls.append(ft.Divider())

            try:
                total_nfe += float(item.get("Valor da Nota", 0))
            except ValueError:
                pass

        total_text.value = f"Valor Total: R$ {total_nfe:.2f}"
        itens_text.value = f"Total de Itens: {total_itens}"
        page.update()

    botao = ft.ElevatedButton("Selecionar Pasta e Processar", on_click=selecionar_e_processar)

    page.add(
        titulo,
        botao,
        ft.Divider(),
        resultado_view,
        itens_text,
        total_text,
    )

ft.app(target=main)
