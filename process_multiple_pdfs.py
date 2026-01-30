"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script process_multiple_pdfs.py
================================
Script para processar múltiplos PDFs e convertê-los em Markdown
usando Docling para depois usar em sistema RAG.
"""
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling_core.types.doc import ImageRefMode
from pathlib import Path
from typing import List
import time

# ====== CONFIGURAÇÃO ======

# Diretório com os PDFs
PDF_DIR = Path("/home/eddygiusepe/2_GitHub/Building_Knowledge_Extraction_Pipeline_with_Docling/data")

# Diretório de saída para os Markdowns
OUTPUT_DIR = Path("/home/eddygiusepe/2_GitHub/Building_Knowledge_Extraction_Pipeline_with_Docling/data/processed")
OUTPUT_DIR.mkdir(exist_ok=True)

# Lista de PDFs específicos (ou use glob para pegar todos)
PDFS_TO_PROCESS = [
    "Data_Science_Eddy_pt.pdf",
    "Docling_Technical_Report.pdf",
]

# ====== CONFIGURAÇÃO DO DOCLING ======

# Configurar pipeline com OCR
pipeline_options = PdfPipelineOptions(
    do_ocr=True,
    ocr_options=RapidOcrOptions(
        lang=['pt', 'en'],
        text_score=0.60,
        print_verbose=False,  # False para não poluir output
        force_full_page_ocr=False,
        bitmap_area_threshold=0.02,
    ),
    do_table_structure=True,
    generate_picture_images=True,
    do_picture_classification=True,
    do_picture_description=True,
    images_scale=0.5,
    do_code_enrichment=True,
    do_formula_enrichment=True,
)

pdf_format_option = PdfFormatOption(pipeline_options=pipeline_options)
converter = DocumentConverter(
    format_options={
        "pdf": pdf_format_option,
    }
)


# ====== FUNÇÃO PARA PROCESSAR UM PDF ======

def processar_pdf(pdf_path: Path) -> dict:
    """
    Processa um único PDF e salva como Markdown.
    
    Args:
        pdf_path: Caminho para o arquivo PDF
    
    Returns:
        dict com informações do processamento
    """
    print(f"\n📄 Processando: {pdf_path.name}")
    inicio = time.time()
    
    try:
        # Converter PDF
        result = converter.convert(str(pdf_path))
        
        # Nome do arquivo de saída (substitui .pdf por .md)
        output_file = OUTPUT_DIR / f"{pdf_path.stem}.md"
        
        # Salvar como Markdown
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.document.export_to_markdown(
                image_placeholder="[🖼️ IMAGEM]",  # Marcação para figuras/fotos (não texto)
                escape_html=True, # Escapa caracteres HTML especiais (ex: <, >, &, etc.)
                escape_underscores=True, # Escapa underscores (ex: _)
                #indent=4, # Indenta o markdown
                enable_chart_tables=True, # Habilita a geração de tabelas
                image_mode=ImageRefMode.PLACEHOLDER, # Usa a marcação para figuras/fotos (não texto)
                include_annotations=True, # Inclui as anotações
                mark_annotations=False, # Não marca as anotações
                page_break_placeholder=None # Não usa placeholder para quebras de página
            ))
        
        tempo_decorrido = time.time() - inicio
        
        print(f"   ✅ Sucesso! Salvo em: {output_file.name}")
        print(f"   ⏱️  Tempo: {tempo_decorrido:.2f}s")
        
        return {
            "status": "sucesso",
            "pdf": pdf_path.name,
            "output": output_file,
            "tempo": tempo_decorrido
        }
        
    except Exception as e:
        tempo_decorrido = time.time() - inicio
        print(f"   ❌ Erro ao processar: {e}")
        return {
            "status": "erro",
            "pdf": pdf_path.name,
            "erro": str(e),
            "tempo": tempo_decorrido
        }


# ====== FUNÇÃO PARA PROCESSAR MÚLTIPLOS PDFs ======

def processar_multiplos_pdfs(pdf_files: List[str]) -> List[dict]:
    """
    Processa uma lista de PDFs.
    
    Args:
        pdf_files: Lista de nomes de arquivos PDF
    
    Returns:
        Lista de resultados do processamento
    """
    resultados = []
    
    print("="*60)
    print("🚀 INICIANDO PROCESSAMENTO DE MÚLTIPLOS PDFs")
    print("="*60)
    
    for pdf_name in pdf_files:
        pdf_path = PDF_DIR / pdf_name
        
        # Verificar se o arquivo existe
        if not pdf_path.exists():
            print(f"\n⚠️  Arquivo não encontrado: {pdf_name}")
            resultados.append({
                "status": "não encontrado",
                "pdf": pdf_name,
                "erro": "Arquivo não existe"
            })
            continue
        
        # Processar PDF
        resultado = processar_pdf(pdf_path)
        resultados.append(resultado)
    
    return resultados


# ====== FUNÇÃO PARA PROCESSAR TODOS OS PDFs DE UM DIRETÓRIO ======

def processar_todos_pdfs_do_diretorio(diretorio: Path) -> List[dict]:
    """
    Processa TODOS os PDFs encontrados em um diretório.
    
    Args:
        diretorio: Caminho do diretório
    
    Returns:
        Lista de resultados
    """
    # Buscar todos os PDFs
    pdfs = list(diretorio.glob("*.pdf"))
    
    if not pdfs:
        print(f"⚠️  Nenhum PDF encontrado em: {diretorio}")
        return []
    
    print(f"\n📁 Encontrados {len(pdfs)} PDFs no diretório")
    
    resultados = []
    for pdf_path in pdfs:
        resultado = processar_pdf(pdf_path)
        resultados.append(resultado)
    
    return resultados


# ====== RELATÓRIO DE PROCESSAMENTO ======

def gerar_relatorio(resultados: List[dict]):
    """Gera relatório do processamento."""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE PROCESSAMENTO")
    print("="*60)
    
    sucessos = [r for r in resultados if r["status"] == "sucesso"]
    erros = [r for r in resultados if r["status"] == "erro"]
    nao_encontrados = [r for r in resultados if r["status"] == "não encontrado"]
    
    print(f"\n✅ Sucessos: {len(sucessos)}")
    print(f"❌ Erros: {len(erros)}")
    print(f"⚠️  Não encontrados: {len(nao_encontrados)}")
    
    if sucessos:
        tempo_total = sum(r["tempo"] for r in sucessos)
        tempo_medio = tempo_total / len(sucessos)
        print(f"\n⏱️  Tempo total: {tempo_total:.2f}s")
        print(f"⏱️  Tempo médio: {tempo_medio:.2f}s por PDF")
    
    if sucessos:
        print("\n📝 Arquivos gerados:")
        for resultado in sucessos:
            print(f"   • {resultado['output'].name}")
    
    if erros:
        print("\n❌ Erros encontrados:")
        for resultado in erros:
            print(f"   • {resultado['pdf']}: {resultado['erro']}")


# ====== EXECUTAR ======

if __name__ == "__main__":
    # OPÇÃO 1: Processar lista específica de PDFs
    print("\n🎯 OPÇÃO 1: Processando PDFs específicos...")
    resultados = processar_multiplos_pdfs(PDFS_TO_PROCESS)
    
    # OPÇÃO 2: Processar TODOS os PDFs do diretório (descomente para usar)
    # print("\n🎯 OPÇÃO 2: Processando TODOS os PDFs do diretório...")
    # resultados = processar_todos_pdfs_do_diretorio(PDF_DIR)
    
    # Gerar relatório
    gerar_relatorio(resultados)
    
    print("\n" + "="*60)
    print("✅ PROCESSAMENTO CONCLUÍDO!")
    print("="*60)
    print(f"\n📂 Arquivos salvos em: {OUTPUT_DIR}")

