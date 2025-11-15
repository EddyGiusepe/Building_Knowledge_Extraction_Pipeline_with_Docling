#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script 1_extraction.py
======================
Este tutorial está baseado no vídeo de Dave Ebbelaar.

How to get your Data ready for AI Agents (Docs, PDFs, Websites, etc.)
=====================================================================
Aqui começamos com a extração de dados de um PDF usando a biblioteca Docling.

Link de estudo --> https://www.youtube.com/watch?v=9lBTS5dM27c
"""
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions#, RapidOcrOptions
from docling.datamodel.pipeline_options import RapidOcrOptions # EasyOcrOptions
from docling_core.types.doc import ImageRefMode
# from utils.sitemap import get_sitemap_urls  # Para processar múltiplas URLs

# ==============================================================================
# CONFIGURAÇÃO PARA PDF COM IMAGENS ESCANEADAS E TEXTO
# ==============================================================================
# Para PDFs que contêm:
# - Texto nativo (pode ser copiado)
# - Imagens escaneadas com texto (precisa de OCR)
#
# O Docling automaticamente detecta quando usar OCR em cada área do PDF

# ==============================================================================
# OPÇÕES DE EXTRAÇÃO DE TEXTO
# ==============================================================================

# OPÇÃO 1: Extração Inteligente (RECOMENDADO) ⭐
# O Docling detecta automaticamente onde tem texto nativo e onde tem imagem
# Aplica OCR APENAS nas imagens (mais rápido)
pipeline_options = PdfPipelineOptions(
    do_ocr=True,                    # ✅ Habilitar OCR em imagens
    ocr_options=RapidOcrOptions(#EasyOcrOptions( #RapidOcrOptions(
        lang=['pt', 'en'],
        #use_gpu=False,
        text_score=0.7, # 60% de confiança para extrair texto
        print_verbose=True, # Imprimir informações de OCR
        force_full_page_ocr=False,  # Seletivo: OCR apenas em imagens
        bitmap_area_threshold=0.02,  # 5% da área da página
    ),
    do_table_structure=True,        # ✅ Detectar estrutura de tabelas
    generate_picture_images=False,   # ✅ Extrair imagens do PDF
    do_picture_classification=True, # ✅ Classificar imagens
    do_picture_description=False, # ✅ Gerar descrição de imagens
    images_scale=0.5, # 50% da escala da imagem
    do_code_enrichment=True, # ✅ Extrair código
    do_formula_enrichment=True, # ✅ Extrair fórmulas matemáticas
    
)

# OPÇÃO 2: Extração TOTAL (FORÇA OCR EM TUDO) 🔥
# Use se quiser garantir 100% de extração, mesmo que mais lento
# Força OCR em TODA a página, mesmo em áreas com texto nativo
# pipeline_options = PdfPipelineOptions(
#     do_ocr=True,                    # ✅ OCR habilitado
#     ocr_options=RapidOcrOptions(
#         force_full_page_ocr=True,   # 🔥 FORÇA OCR EM TUDO!
#         bitmap_area_threshold=0.01,  # 1% threshold (mais sensível)
#     ),
#     do_table_structure=True,
#     generate_picture_images=True,
# )

# OPÇÃO 3: Usar EasyOCR (Mais preciso, mas mais lento)
# from docling.datamodel.pipeline_options import EasyOcrOptions
# pipeline_options = PdfPipelineOptions(
#     do_ocr=True,
#     ocr_options=EasyOcrOptions(
#         lang=['pt', 'en'],  # Português e Inglês
#         use_gpu=False,       # True se tiver GPU
#     ),
# )

# Criar o conversor com as opções de OCR
pdf_format_option = PdfFormatOption(pipeline_options=pipeline_options)
converter = DocumentConverter(
    format_options={InputFormat.PDF: pdf_format_option}
)

print("📄 Convertendo PDF (isso pode demorar alguns minutos com OCR)...")
print("   - Detectando texto nativo")
print("   - Aplicando OCR em imagens escaneadas")
print("   - Extraindo tabelas e figuras\n")

# Converter o PDF
result = converter.convert(
    "/home/eddygiusepe/2_GitHub/Building_Knowledge_Extraction_Pipeline_with_Docling/data/Data_Science_Eddy_pt.pdf"
)

# ==============================================================================
# GERAR MARKDOWN COM TODO O TEXTO EXTRAÍDO
# ==============================================================================
# IMPORTANTE: O texto extraído das imagens via OCR JÁ ESTÁ INCLUÍDO!
# 
# Exemplo de resultado:
# ┌─────────────────────────────────────────────────────────┐
# │ Página do PDF:                                          │
# │                                                          │
# │  Título do Documento  <-- texto nativo (extrai direto) │
# │                                                          │
# │  Parágrafo com texto normal...                          │
# │                                                          │
# │  ┌───────────────────────────┐                          │
# │  │  [IMAGEM COM TEXTO]       │  <-- aplica OCR aqui!   │
# │  │  "Texto dentro da imagem" │                          │
# │  │  "Segunda linha"          │                          │
# │  └───────────────────────────┘                          │
# │                                                          │
# │  Mais texto normal...                                   │
# └─────────────────────────────────────────────────────────┘
#
# No markdown final, você terá:
# """
# # Título do Documento
# 
# Parágrafo com texto normal...
# 
# Texto dentro da imagem  <-- ✅ EXTRAÍDO VIA OCR!
# Segunda linha           <-- ✅ EXTRAÍDO VIA OCR!
# 
# [🖼️ IMAGEM]  <-- apenas uma marcação de que havia uma figura/foto
# 
# Mais texto normal...
# """

markdown_output = result.document.export_to_markdown(
    image_placeholder="[🖼️ IMAGEM]",  # Marcação para figuras/fotos (não texto)
    escape_html=True,
    escape_underscores=True,
    #indent=4,
    enable_chart_tables=True,
    image_mode=ImageRefMode.PLACEHOLDER,
    include_annotations=False,
    mark_annotations=False,
    page_break_placeholder=None
)

# Salvar o markdown em arquivo
output_path = "/home/eddygiusepe/2_GitHub/Building_Knowledge_Extraction_Pipeline_with_Docling/data/Eddy_Data_Science_pt.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(markdown_output)

# Mostrar estatísticas
print("\n" + "="*60)
print("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
print("="*60)
print("📄 Arquivo markdown salvo em:")
print(f"   {output_path}")
print("\n📊 Estatísticas do documento:")
print(f"   • Total de páginas: {len(result.document.pages)}")
print(f"   • Status: {result.status}")
if hasattr(result.document, 'pictures'):
    print(f"   • Imagens detectadas: {len(result.document.pictures)}")
if hasattr(result.document, 'tables'):
    print(f"   • Tabelas detectadas: {len(result.document.tables)}")
print(f"   • Tamanho do markdown: {len(markdown_output):,} caracteres")
print("="*60 + "\n")

# ==============================================================================
# 📚 EXPLICAÇÃO: Como o OCR Funciona com o Docling
# ==============================================================================
#
# O Docling é INTELIGENTE! Ele:
#
# 1️⃣ Analisa o PDF página por página
# 2️⃣ Detecta automaticamente áreas com:
#    • Texto nativo (extrai diretamente, sem OCR)
#    • Imagens escaneadas (aplica OCR apenas nessas áreas)
#    • Tabelas (reconhece estrutura)
#    • Figuras (extrai)
#
# 3️⃣ Aplica OCR APENAS onde necessário (economiza tempo!)
#
# Tipos de OCR disponíveis:
# -------------------------
# • RapidOCR   → Rápido, leve, boa precisão (RECOMENDADO) ⭐
# • EasyOCR    → Mais preciso, suporta GPU, mais lento
# • Tesseract  → Tradicional, muito configurável
#
# ==============================================================================
# 📦 OUTRAS OPÇÕES DE EXPORT (Opcional)
# ==============================================================================

# Exportar para JSON (estrutura completa do documento)
# json_output = result.document.export_to_dict()
# import json
# with open("output.json", "w") as f:
#     json.dump(json_output, f, indent=2, ensure_ascii=False)

# Exportar para HTML
# html_output = result.document.export_to_html()
# with open("output.html", "w") as f:
#     f.write(html_output)

# Exportar para DocTags (formato estruturado)
# doctags_output = result.document.export_to_doctags()

# ==============================================================================
# 🌐 OUTRAS FUNCIONALIDADES DO DOCLING (Exemplos Comentados)
# ==============================================================================
# O Docling não funciona apenas com PDFs! Veja outros exemplos:

# --------------------------------------------------------------
# Extrair conteúdo de HTML/Websites
# --------------------------------------------------------------
# result_html = converter.convert("https://github.com/docling-project/docling")
# markdown_html = result_html.document.export_to_markdown()
# print(markdown_html)

# --------------------------------------------------------------
# Processar múltiplas páginas usando sitemap
# --------------------------------------------------------------
# sitemap_urls = get_sitemap_urls("https://example.com")
# results = converter.convert_all(sitemap_urls)
# 
# documentos = []
# for res in results:
#     if res.document:
#         documentos.append(res.document)
# 
# print(f"Total de documentos processados: {len(documentos)}")

# ==============================================================================
# 📖 GUIA RÁPIDO DE USO
# ==============================================================================
#
# CENÁRIO 1: PDF com texto nativo (pode copiar texto)
# ----------------------------------------------------
# converter = DocumentConverter()
# result = converter.convert("documento.pdf")
# markdown = result.document.export_to_markdown()
#
#
# CENÁRIO 2: PDF escaneado (precisa OCR) ⭐ ESTE ARQUIVO
# -------------------------------------------------------
# pipeline_options = PdfPipelineOptions(
#     do_ocr=True,
#     ocr_options=RapidOcrOptions()  # ou EasyOcrOptions()
# )
# pdf_format_option = PdfFormatOption(pipeline_options=pipeline_options)
# converter = DocumentConverter(
#     format_options={InputFormat.PDF: pdf_format_option}
# )
# result = converter.convert("documento_escaneado.pdf")
# markdown = result.document.export_to_markdown()
#
#
# CENÁRIO 3: Customizar placeholder de imagens
# ---------------------------------------------
# markdown = result.document.export_to_markdown(
#     image_placeholder="[FIGURA REMOVIDA]"
# )
#
# ==============================================================================
