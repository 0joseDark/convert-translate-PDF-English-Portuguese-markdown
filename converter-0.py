import pdfplumber  # Para ler texto de ficheiros PDF
from markdownify import markdownify as md  # Para converter texto em Markdown
from googletrans import Translator  # Para traduzir texto usando Google Translate
import os  # Para operações de sistema de ficheiros
from tkinter import Tk, filedialog, Toplevel, Label, Button, StringVar, ttk  # Para GUI

# Função para traduzir o PDF com barra de progresso
def traduzir_pdf_com_progresso():
    """
    Traduz um ficheiro PDF do inglês para português e mostra uma barra de progresso.
    """
    # Seleção do ficheiro PDF
    pdf_path = filedialog.askopenfilename(title="Selecione o ficheiro PDF",
                                          filetypes=[("Ficheiros PDF", "*.pdf")])
    if not pdf_path:
        print("Nenhum ficheiro selecionado.")
        return

    # Criar a janela de progresso
    janela_progresso = Toplevel()
    janela_progresso.title("Progresso da Tradução")
    janela_progresso.geometry("400x200")

    label_status = Label(janela_progresso, text="A processar o ficheiro...", font=("Arial", 12))
    label_status.pack(pady=10)

    progresso_var = StringVar()
    progresso_var.set("0%")
    label_progresso = Label(janela_progresso, textvariable=progresso_var, font=("Arial", 10))
    label_progresso.pack()

    barra_progresso = ttk.Progressbar(janela_progresso, orient="horizontal", length=300, mode="determinate")
    barra_progresso.pack(pady=20)

    botao_fechar = Button(janela_progresso, text="Fechar", state="disabled", command=janela_progresso.destroy)
    botao_fechar.pack(pady=10)

    # Abrir o PDF e contar as páginas
    try:
        with pdfplumber.open(pdf_path) as pdf:
            texto_traduzido = ""
            total_paginas = len(pdf.pages)
            barra_progresso["maximum"] = total_paginas

            translator = Translator()
            for i, pagina in enumerate(pdf.pages):
                texto_pagina = pagina.extract_text()
                texto_traduzido += translator.translate(texto_pagina, src="en", dest="pt").text
                barra_progresso["value"] = i + 1
                progresso_var.set(f"{int(((i + 1) / total_paginas) * 100)}%")
                janela_progresso.update_idletasks()
    except Exception as e:
        label_status.config(text=f"Erro: {e}")
        return

    # Converter para Markdown
    texto_markdown = md(texto_traduzido)

    # Salvar o ficheiro Markdown
    diretorio_saida = os.path.dirname(pdf_path)
    nome_ficheiro = os.path.splitext(os.path.basename(pdf_path))[0]
    caminho_markdown = os.path.join(diretorio_saida, f"{nome_ficheiro}_traduzido.md")

    try:
        with open(caminho_markdown, "w", encoding="utf-8") as ficheiro_md:
            ficheiro_md.write(texto_markdown)
        label_status.config(text=f"Tradução concluída! Ficheiro salvo em:\n{caminho_markdown}")
    except Exception as e:
        label_status.config(text=f"Erro ao salvar o ficheiro: {e}")

    # Ativar o botão de fechar
    botao_fechar.config(state="normal")

# Janela principal
def janela_principal():
    """
    Cria a janela principal da aplicação.
    """
    root = Tk()
    root.title("Tradutor de PDF para Markdown")
    root.geometry("400x200")

    label_titulo = Label(root, text="Tradutor de PDF para Markdown", font=("Arial", 14))
    label_titulo.pack(pady=20)

    botao_traduzir = Button(root, text="Selecionar e Traduzir PDF", font=("Arial", 12), command=traduzir_pdf_com_progresso)
    botao_traduzir.pack(pady=20)

    botao_sair = Button(root, text="Sair", font=("Arial", 12), command=root.quit)
    botao_sair.pack(pady=10)

    root.mainloop()

# Executar a janela principal
if __name__ == "__main__":
    janela_principal()
