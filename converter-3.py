import pdfplumber
from googletrans import Translator
from markdownify import markdownify as md
import os
from tkinter import Tk, filedialog
from PIL import Image


def traduzir_pdf_para_markdown():
    """
    Extrai texto e imagens de um PDF, traduz o texto do inglês para português,
    e cria um ficheiro Markdown formatado, combinando texto traduzido e imagens.
    """
    # Selecionar o ficheiro PDF
    Tk().withdraw()
    pdf_path = filedialog.askopenfilename(title="Selecione o ficheiro PDF",
                                          filetypes=[("Ficheiros PDF", "*.pdf")])
    if not pdf_path:
        print("Nenhum ficheiro selecionado. Encerrando...")
        return

    # Configuração de diretórios
    diretorio_base = os.path.dirname(pdf_path)
    nome_ficheiro = os.path.splitext(os.path.basename(pdf_path))[0]
    pasta_imagens = os.path.join(diretorio_base, f"{nome_ficheiro}_imagens")
    os.makedirs(pasta_imagens, exist_ok=True)

    # Abrir o PDF e inicializar o tradutor
    translator = Translator()
    texto_markdown = f"# Tradução do PDF: {nome_ficheiro}\n\n"

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_paginas = len(pdf.pages)

            for i, pagina in enumerate(pdf.pages):
                # Início da seção da página
                texto_markdown += f"## Página {i + 1}\n\n"

                # Extrair texto da página
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    print(f"Traduzindo texto da página {i + 1}/{total_paginas}...")
                    texto_traduzido = translator.translate(texto_pagina, src="en", dest="pt").text
                    texto_markdown += md(texto_traduzido) + "\n\n"

                # Extrair imagens da página
                for j, imagem in enumerate(pagina.images):
                    try:
                        # Extrair a imagem como um objeto PIL
                        img_stream = pdf.streams.get(imagem["object_number"])
                        if img_stream:
                            caminho_imagem = os.path.join(pasta_imagens, f"pagina_{i + 1}_imagem_{j + 1}.png")
                            with open(caminho_imagem, "wb") as img_file:
                                img_file.write(img_stream)
                            print(f"Imagem extraída: {caminho_imagem}")

                            # Adicionar referência à imagem no Markdown
                            texto_markdown += f"![Imagem Página {i + 1}](./{os.path.basename(pasta_imagens)}/{os.path.basename(caminho_imagem)})\n\n"
                    except Exception as img_error:
                        print(f"Erro ao processar imagem na página {i + 1}: {img_error}")

    except Exception as e:
        print(f"Erro ao processar o ficheiro PDF: {e}")
        return

    # Salvar o Markdown
    caminho_markdown = os.path.join(diretorio_base, f"{nome_ficheiro}_traduzido.md")
    try:
        with open(caminho_markdown, "w", encoding="utf-8") as ficheiro_md:
            ficheiro_md.write(texto_markdown)
        print(f"Markdown criado com sucesso: {caminho_markdown}")
    except Exception as e:
        print(f"Erro ao salvar o ficheiro Markdown: {e}")


# Executar a função principal
if __name__ == "__main__":
    traduzir_pdf_para_markdown()
