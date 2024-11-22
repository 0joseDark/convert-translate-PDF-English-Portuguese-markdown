# Importação das bibliotecas necessárias
import pdfplumber  # Para ler texto de ficheiros PDF
from markdownify import markdownify as md  # Para converter texto em Markdown
from googletrans import Translator  # Para traduzir texto usando Google Translate
import os  # Para operações de sistema de ficheiros
from tkinter import Tk, filedialog  # Para selecionar ficheiros através de uma interface gráfica

# Função principal
def traduzir_pdf_para_markdown():
    """
    Traduz um ficheiro PDF do inglês para português e salva no formato Markdown.
    """

    # Inicializar interface gráfica para selecionar ficheiro PDF
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    pdf_path = filedialog.askopenfilename(title="Selecione o ficheiro PDF", 
                                          filetypes=[("Ficheiros PDF", "*.pdf")])
    
    if not pdf_path:
        print("Nenhum ficheiro selecionado. Encerrando...")
        return

    # Abrir e extrair texto do PDF
    try:
        with pdfplumber.open(pdf_path) as pdf:
            texto_pdf = ""
            for pagina in pdf.pages:
                texto_pdf += pagina.extract_text()
    except Exception as e:
        print(f"Erro ao abrir o ficheiro PDF: {e}")
        return

    if not texto_pdf.strip():
        print("O ficheiro PDF está vazio ou o texto não pode ser extraído.")
        return

    # Inicializar o tradutor do Google
    translator = Translator()

    # Traduzir o texto extraído do inglês para português
    try:
        print("A traduzir o texto...")
        texto_traduzido = translator.translate(texto_pdf, src="en", dest="pt").text
    except Exception as e:
        print(f"Erro ao traduzir o texto: {e}")
        return

    # Converter texto traduzido para formato Markdown
    texto_markdown = md(texto_traduzido)

    # Salvar o texto em formato Markdown
    diretorio_saida = os.path.dirname(pdf_path)
    nome_ficheiro = os.path.splitext(os.path.basename(pdf_path))[0]
    caminho_markdown = os.path.join(diretorio_saida, f"{nome_ficheiro}_traduzido.md")

    try:
        with open(caminho_markdown, "w", encoding="utf-8") as ficheiro_md:
            ficheiro_md.write(texto_markdown)
        print(f"Ficheiro traduzido e salvo como: {caminho_markdown}")
    except Exception as e:
        print(f"Erro ao salvar o ficheiro Markdown: {e}")

# Executar a função principal
if __name__ == "__main__":
    traduzir_pdf_para_markdown()
