# <h1 align="center"><font color="red">Building_Knowledge_Extraction_Pipeline_with_Docling</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

O Docling simplifica o processamento de documentos, analisando diversos formatos — incluindo compreensão avançada de PDF — e fornecendo integrações perfeitas com o ecossistema de IA de geração.


![](https://i.ytimg.com/vi/w-Ru0VL6IT8/maxresdefault.jpg)


[Docling](https://github.com/docling-project/docling) é uma biblioteca de processamento de documentos de ``código aberto``, flexível e poderosa que converte vários formatos de documentos em um formato unificado. Ela tem recursos avançados de compreensão de documentos alimentados por modelos de ``IA`` de última geração para análise de layout e reconhecimento de ``estrutura de tabela``.

O sistema inteiro roda localmente em computadores padrão e é projetado para ser extensível - os desenvolvedores podem adicionar novos modelos ou modificar o pipeline para necessidades específicas. É particularmente útil para tarefas como ``pesquisa de documentos corporativos``, ``recuperação de passagens`` e ``extração de conhecimento``. Com seus recursos avançados de ``chunking`` e processamento, é a ferramenta perfeita para fornecer conhecimento a aplicativos ``GenAI`` por meio de pipelines ``RAG`` (Retrieval Augmented Generation).

## <font color="gree">Principais características</font>

- ``Suporte de formato universal``: processe PDF, DOCX, XLSX, PPTX, Markdown, HTML, imagens e muito mais
- ``Compreensão avançada``: análise de layout com tecnologia de ``IA`` e reconhecimento de estrutura de tabela
- ``Saída flexível``: Exportar para HTML, Markdown, ``JSON`` ou texto simples
- ``Alto desempenho``: processamento eficiente em hardware local

## <font color="gree">Coisas em que eles estão trabalhando</font>

- Extração de metadados, incluindo título, autores, referências e idioma
- Inclusão de Modelos de Linguagem Visual (``SmolDocling``)
- Compreensão de gráficos (gráfico de barras, gráfico de pizza, gráfico de linhas, etc.)
- Compreensão da química complexa (``Estruturas moleculares``)

## <font color="gree">Introdução ao Exemplo</font>

### <font color="orange">Pré-requisitos</font>

1. Instale os pacotes necessários:

```bash
pip install -r requirements.txt

ou

uv sync
```
2. Configure suas variáveis ​​de ambiente criando um arquivo ``.env``:

```bash
OPENAI_API_KEY=your_api_key_here
```

### <font color="orange">Executando o Exemplo</font>

Execute os arquivos para construir e consultar o banco de dados de documentos:

1. Extrair conteúdo do documento: ``python 1-extraction.py``
2. Criar chunks de documentos: ``python 2-chunking.py``
3. Crie ``embeddings`` e armazene no LanceDB: ``python 3-embedding.py``
4. Teste a funcionalidade básica de pesquisa: ``python 4-search.py``
5. Inicie a interface de bate-papo do Streamlit: ``streamlit run 5-chat.py``

Em seguida, abra seu navegador e navegue até ``http://localhost:8501`` para interagir com a interface de Q&A do documento.

## <font color="gree">Processamento de documentos</font>

### <font color="orange">Formatos de entrada suportados</font>

| Formato | Descrição |
|---------|-----------|
| PDF | Documentos PDF nativos com preservação de layout |
| DOCX, XLSX, PPTX | Formatos do Microsoft Office (2007+) |
| Markdown | Texto simples (plain text) com marcação |
| HTML/XHTML | Documentos da Web |
| Imagens | PNG, JPEG, TIFF, BMP |
| XML do USPTO | Documentos de patentes |
| XML do PMC | Artigos do PubMed Central |

### <font color="orange">Pipeline de processamento</font>

O pipeline padrão inclui:

1. Análise de documentos com backend específico de formato
2. Análise de layout usando modelos de IA
3. Reconhecimento de estrutura de tabela
4. Extração de metadados
5. Organização e estruturação de conteúdo
6. Formatação de exportação

## <font color="gree">Modelos</font>

O ``Docling`` alavanca dois modelos primários de IA especializados para compreensão de documentos. Em seu núcleo, o modelo de análise de layout é construído na arquitetura ``RT-DETR`` (``Real-Time Detection Transformer``), que se destaca na detecção e classificação de elementos de página. Este modelo processa páginas com resolução de ``72 dpi`` e pode analisar uma única página em menos de um segundo em uma CPU padrão, tendo sido treinado no ``DocLayNet`` conjunto de dados abrangente.

O segundo modelo-chave é ``TableFormer``, um sistema de reconhecimento de estrutura de tabela que pode lidar com layouts de tabela complexos, incluindo bordas parciais, células vazias, células de abrangência e cabeçalhos hierárquicos. O ``TableFormer`` normalmente processa tabelas em 2 a 6 segundos na CPU, tornando-o eficiente para uso prático.

Para documentos que exigem extração de texto de imagens, o Docling integra-se com ``EasyOCR`` como um componente opcional, que opera a ``216 dpi`` para qualidade ideal, mas requer cerca de ``30 segundos`` por página. Tanto a análise de layout quanto os modelos TableFormer foram desenvolvidos pela ``IBM Research`` e estão disponíveis publicamente como pesos pré-treinados no ``Hugging Face`` em ``"ds4sd/docling-models"``.

Para obter informações mais detalhadas sobre esses modelos e sua implementação, consulte a [documentação técnica](https://arxiv.org/pdf/2408.09869).


## <font color="gree">Chunking</font>

Ao construir um aplicativo ``RAG`` (Retrieval Augmented Generation), você precisa dividir documentos em partes menores e significativas que podem ser facilmente pesquisadas e recuperadas. Mas isso não é tão simples quanto dividir o texto a cada ``X`` palavras ou caracteres.

<font color="pink">O que torna o chunking do Docling único é que ele entende a estrutura real do seu documento.</font> Ele tem duas abordagens principais:

1. O ``Hierarchical Chunker`` é como um analisador de documentos inteligente - ele sabe onde estão as ``"juntas"`` (joints) naturais do seu documento. Em vez de cortar o texto às cegas em pedaços de tamanho fixo, ele reconhece e preserva elementos importantes como seções, parágrafos, tabelas e listas. Ele mantém o relacionamento entre os cabeçalhos e seu conteúdo, e mantém os itens relacionados juntos (como itens em uma lista).

2. O ``Hybrid Chunker`` leva isso um passo adiante. Ele começa com os ``chunks hierárquicos``, mas então:

* Ele pode dividir pedaços (``chunks``) que são muito grandes para o seu modelo de ``embedding``	
* Ele pode costurar pedaços (``chunks``) que são muito pequenos
* Ele funciona com seu ``tokenizador específico``, então os pedaços se encaixarão perfeitamente com seu modelo de linguagem escolhido

## <font color="gree">Por que isso é ótimo para aplicações ``RAG``?</font>

Imagine que você está construindo um sistema para responder perguntas sobre documentos técnicos. Com chunking básico (como dividir a cada ``500`` palavras), você pode cortar bem no meio de uma tabela, ou separar um cabeçalho de seu conteúdo. Mas o chunking inteligente do ``Docling``:

* Mantém as informações relacionadas juntas
* Preserva a estrutura do documento
* Mantém o contexto (``como cabeçalhos e legendas``)
* Cria chunks otimizados para seu modelo de ``embedding`` específico
* Garante que cada chunk seja significativo e independente

Isso significa que quando seu sistema ``RAG`` recupera blocos, eles terão o contexto e a estrutura adequados, levando a respostas mais precisas e coerentes do seu modelo de linguagem.









Thank God!
