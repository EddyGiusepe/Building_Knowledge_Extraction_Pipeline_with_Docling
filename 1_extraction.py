#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Este tutorial está baseado no vídeo de Dave Ebbelaar.

How to get your Data ready for AI Agents (Docs, PDFs, Websites, etc.)
=====================================================================
Aqui começamos com a extração de dados de um PDF usando a biblioteca Docling.

Link de estudo --> https://www.youtube.com/watch?v=9lBTS5dM27c
"""
from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls

converter = DocumentConverter()

# --------------------------------------------------------------
# Basic PDF extraction
# --------------------------------------------------------------

result = converter.convert(
    "/home/eddygiusepe/1_github/Building_Knowledge_Extraction_Pipeline_with_Docling/data/Docling_Technical_Report.pdf"
)

document = result.document
markdown_output = document.export_to_markdown()
print(markdown_output)
json_output = document.export_to_dict()
print(json_output)

# --------------------------------------------------------------
# Basic HTML extraction
# --------------------------------------------------------------

result = converter.convert("https://github.com/docling-project/docling")

document = result.document
markdown_output = document.export_to_markdown()
print(markdown_output)

# --------------------------------------------------------------
# Scrape multiple pages using the sitemap
# --------------------------------------------------------------

sitemap_urls = get_sitemap_urls("https://github.com/docling-project/docling")
conv_results_iter = converter.convert_all(sitemap_urls)

docs = []
for result in conv_results_iter:
    if result.document:
        document = result.document
        docs.append(document)

print(docs)
