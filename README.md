# A3 IA Retail

Projeto em Python para recomendar produtos do dataset **Online Retail** usando:

- regras de associacao com Apriori;
- regras de associacao com FP-Growth;
- similaridade entre produtos com base em coocorrencia nos pedidos.

## Objetivo

Usar o historico de vendas da base Online Retail para descobrir produtos que costumam ser comprados juntos e gerar recomendacoes do tipo: "quem comprou A tambem pode comprar B".

## Estrutura

```text
.
├── data/
│   ├── raw/              # coloque aqui o CSV/XLSX original
│   └── processed/        # arquivos tratados gerados pelo projeto
├── notebooks/            # analises exploratorias e apresentacao tecnica
├── reports/
│   ├── figures/          # graficos
│   └── tables/           # tabelas finais
├── scripts/              # atalhos de execucao
├── src/a3_ia_retail/     # codigo principal
└── tests/                # testes automatizados
```

## Como iniciar

> Recomendo usar Python 3.12 para este projeto. O `pyproject.toml` aceita Python 3.10 ate 3.13.

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Coloque a base em `data/raw/`.

O arquivo pode ser `.csv`, `.xlsx` ou `.xls`. Exemplos aceitos:

- `data/raw/online_retail.csv`
- `data/raw/Online Retail.xlsx`

4. Rode a pipeline inicial:

```bash
python scripts/run_pipeline.py --input data/raw/online_retail.csv
```

ou, se instalar o projeto em modo editavel:

```bash
python -m pip install -e .
a3-retail --input data/raw/online_retail.csv
```

## Passos do trabalho

1. Carregar a base e conferir tamanho, colunas, tipos e primeiras linhas.
2. Fazer EDA: nulos, cancelamentos, paises com mais vendas, produtos mais vendidos, produtos com maior faturamento e quantidade de pedidos.
3. Limpar cancelamentos, devolucoes, quantidades invalidas, precos invalidos e descricoes vazias.
4. Padronizar descricoes de produtos.
5. Criar a cesta de compras no formato pedido x produto.
6. Aplicar Apriori e gerar regras com support, confidence e lift.
7. Aplicar FP-Growth e gerar regras equivalentes.
8. Calcular similaridade entre produtos.
9. Comparar tempo, quantidade de regras, lift medio, confianca media e exemplos de recomendacao.
10. Montar relatorio e apresentacao.

## Saidas geradas

A pipeline salva arquivos em `reports/tables/`:

- `data/processed/online_retail_clean.csv`
- `data/processed/basket.csv`
- `eda_summary.csv`
- `cleaning_summary.csv`
- `apriori_rules.csv`
- `fpgrowth_rules.csv`
- `similarity_recommendations.csv`
- `method_comparison.csv`
