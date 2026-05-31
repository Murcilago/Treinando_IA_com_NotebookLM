# Mr. Crawley

> *"Mr. Crawley, what went on in your web?"*

Utilitário para consolidar documentação multi-página em um único arquivo HTML auto-contido, pronto para uso como fonte no [NotebookLM](https://notebooklm.google.com/).

Feito para resolver o problema clássico: a documentação que você quer estudar está espalhada por dezenas de páginas linkadas, mas o NotebookLM tem limite de 50 fontes.

---

## Como funciona

1. Parte de uma URL inicial
2. Segue os links internos até a profundidade configurada
3. Extrai o conteúdo principal de cada página (remove nav, footer, scripts)
4. Embute imagens como base64 diretamente no HTML
5. Gera um único arquivo HTML com índice navegável e âncoras por página

---

## Uso

```bash
# Ativar o ambiente virtual (na raiz do projeto)
source .venv/bin/activate

# Uso básico — profundidade 1 (página inicial + links diretos)
python tools/crawley.py https://docs.delta.io/latest/index.html

# Profundidade 2 com delay maior (sites com rate limiting)
python tools/crawley.py https://docs.databricks.com/en/delta/index.html --depth 2 --delay 1.0

# Sem imagens — arquivo menor, só texto e código
python tools/crawley.py https://spark.apache.org/docs/latest/sql-programming-guide.html --no-images

# Arquivo de saída customizado
python tools/crawley.py <url> --output downloads/delta_lake.html
```

---

## Opções

| Opção | Padrão | Descrição |
|-------|--------|-----------|
| `url` | — | URL de partida (obrigatório) |
| `--depth N` | `1` | Profundidade máxima de links a seguir |
| `--delay S` | `0.5` | Intervalo entre requisições (segundos) |
| `--output FILE` | `docs_consolidado.html` | Arquivo de saída |
| `--allow-external` | off | Seguir links para outros domínios |
| `--no-images` | off | Não embutir imagens (arquivo menor) |

---

## Dica: converter para PDF

Abra o HTML gerado no Chrome e use **Ctrl+P → Salvar como PDF → sem margens**.
O PDF pode ser carregado diretamente no NotebookLM.

---

## Dependências

```bash
uv pip install requests beautifulsoup4 lxml
```
