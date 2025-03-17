import xml.etree.ElementTree as ET
from typing import List
from urllib.parse import urljoin

import requests


def get_sitemap_urls(base_url: str, sitemap_filename: str = "sitemap.xml") -> List[str]:
    """Busca e analisa um arquivo XML de sitemap para extrair URLs.

    Args:
        base_url: A URL base do site
        sitemap_filename: O nome do arquivo de sitemap (padrão: sitemap.xml)

    Returns:
        Uma lista de URLs encontradas no sitemap. Se o sitemap não for encontrado, retorna uma lista
        contendo apenas a URL base.

    Raises:
        ValueError: Se houver um erro ao buscar (exceto 404) ou analisar o sitemap
    """
    try:
        sitemap_url = urljoin(base_url, sitemap_filename)

        # Busca a URL do sitemap:
        response = requests.get(sitemap_url, timeout=10)

        # Retorna apenas a URL base se o sitemap não for encontrado:
        if response.status_code == 404:
            return [base_url.rstrip("/")]

        response.raise_for_status()

        # Analisa o conteúdo XML:
        root = ET.fromstring(response.content)

        # Lida com diferentes namespaces XML que os sitemaps podem usar:
        namespaces = (
            {"ns": root.tag.split("}")[0].strip("{")} if "}" in root.tag else ""
        )

        # Extrai URLs usando o namespace se presente:
        if namespaces:
            urls = [elem.text for elem in root.findall(".//ns:loc", namespaces)]
        else:
            urls = [elem.text for elem in root.findall(".//loc")]

        return urls

    except requests.RequestException as e:
        raise ValueError(f"Falha ao buscar o sitemap: {str(e)}")
    except ET.ParseError as e:
        raise ValueError(f"Falha ao analisar o XML do sitemap: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erro inesperado ao processar o sitemap: {str(e)}")


if __name__ == "__main__":
    print(get_sitemap_urls("https://github.com/docling-project/docling"))