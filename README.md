# A3 IA Retail

Projeto em Python para recomendacao de produtos usando o dataset **Online Retail**. A ideia central e transformar o historico de compras de uma loja online em recomendacoes do tipo:

> quem comprou o produto A tambem pode se interessar pelo produto B.

## Contexto do projeto

Lojas online acumulam muitos dados de vendas: pedidos, produtos comprados, quantidades, paises, clientes e datas. Esses dados podem revelar padroes importantes de comportamento, como produtos que costumam ser comprados juntos ou produtos que aparecem em pedidos parecidos.

O dataset Online Retail representa esse cenario. Cada linha da base e um item vendido dentro de um pedido. Ou seja, um mesmo `InvoiceNo` pode aparecer em varias linhas, cada uma representando um produto diferente dentro da mesma compra.

## Problema resolvido

O problema do projeto e:

**Como uma loja online pode usar compras anteriores para recomendar produtos relacionados aos clientes?**

Para responder isso, o projeto:

- limpa vendas invalidas, cancelamentos e produtos sem descricao;
- organiza os pedidos em cestas de compras;
- identifica associacoes fortes entre produtos;
- agrupa produtos com K-Means;
- compara os metodos para apoiar a conclusao final.

## Metodos implementados

### Apriori

Gera regras de associacao com base em conjuntos frequentes de produtos.

Exemplo de leitura:

```text
Se comprou A, recomenda B.
```

As principais metricas sao:

- `support`: frequencia da regra na base.
- `confidence`: probabilidade de comprar B quando A foi comprado.
- `lift`: forca da associacao. Valores acima de 1 indicam relacao positiva.

### FP-Growth

Tambem gera regras de associacao, como o Apriori, mas usa uma estrategia mais eficiente para encontrar conjuntos frequentes. No resultado atual, ele encontra as mesmas regras do Apriori, mas executa mais rapido.

### K-Means

Agrupa produtos com comportamento de compra parecido. A pipeline usa:

1. matriz produto x pedido;
2. `TruncatedSVD` para reduzir dimensionalidade;
3. `KMeans` para criar grupos de produtos;
4. pontuacao de proximidade dentro de cada cluster para gerar recomendacoes.

Esse metodo ajuda a responder:

```text
quais produtos pertencem ao mesmo grupo de comportamento?
```

## Estrutura do projeto

```text
.
├── data/
│   ├── raw/              # base original, nao versionada
│   └── processed/        # bases processadas geradas pela pipeline
├── notebooks/            # espaco para analise exploratoria e apresentacao tecnica
├── reports/
│   ├── figures/          # graficos futuros
│   └── tables/           # tabelas finais da analise
├── scripts/
│   └── run_pipeline.py   # atalho para executar a pipeline
├── src/a3_ia_retail/     # codigo principal do projeto
└── tests/                # testes automatizados
```

## Como o codigo funciona

A execucao principal esta em `src/a3_ia_retail/pipeline.py`. Ela coordena todos os passos:

1. Carrega a base original.
2. Gera um resumo inicial para EDA.
3. Limpa e padroniza os dados.
4. Cria a cesta de compras.
5. Executa Apriori.
6. Executa FP-Growth.
7. Executa K-Means.
8. Salva os resultados em CSV.
9. Cria a tabela comparativa dos metodos.

Os modulos principais sao:

- `data_loading.py`: leitura do CSV/XLSX e validacao das colunas obrigatorias.
- `preprocessing.py`: limpeza de cancelamentos, quantidades invalidas, precos invalidos e descricoes vazias.
- `eda.py`: tabelas exploratorias por pais e por produto.
- `basket.py`: transforma pedidos em matriz pedido x produto.
- `association.py`: executa Apriori e FP-Growth com `mlxtend`.
- `clustering.py`: executa K-Means e gera recomendacoes por cluster.
- `comparison.py`: resume os resultados dos metodos.

## Como iniciar

Recomendo usar Python 3.12. O projeto aceita Python 3.10 ate 3.13.

1. Crie e ative o ambiente virtual:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Coloque a base original em `data/raw/`.

Exemplos:

```text
data/raw/Online_Retail.csv
data/raw/Online Retail.xlsx
```

4. Execute a pipeline:

```bash
python scripts/run_pipeline.py --input data/raw/Online_Retail.csv
```

Tambem e possivel ajustar alguns parametros:

```bash
python scripts/run_pipeline.py \
  --input data/raw/Online_Retail.csv \
  --min-support 0.02 \
  --min-confidence 0.2 \
  --kmeans-clusters 12 \
  --kmeans-components 50
```

## Arquivos gerados

### `data/processed/online_retail_clean.csv`

Base limpa usada nas etapas seguintes. Inclui a coluna `Revenue`, calculada como:

```text
Revenue = Quantity * UnitPrice
```

### `data/processed/basket.csv`

Matriz de cesta de compras. Cada linha e um pedido e cada coluna e um produto. Valor `1` significa que o produto apareceu no pedido; valor `0` significa que nao apareceu.

### `reports/tables/eda_summary.csv`

Resumo da base bruta: linhas, colunas, duplicatas, descricoes nulas, clientes nulos e pedidos cancelados.

### `reports/tables/cleaning_summary.csv`

Resumo do tratamento dos dados, mostrando quantas linhas foram afetadas por cada regra de limpeza.

### `reports/tables/country_summary.csv`

Resumo por pais, com quantidade de pedidos e faturamento.

### `reports/tables/top_products_by_quantity.csv`

Ranking dos produtos mais vendidos em quantidade.

### `reports/tables/top_products_by_revenue.csv`

Ranking dos produtos com maior faturamento.

### `reports/tables/apriori_rules.csv`

Regras de associacao geradas pelo Apriori. As colunas mais importantes sao `antecedents`, `consequents`, `support`, `confidence` e `lift`.

### `reports/tables/fpgrowth_rules.csv`

Regras de associacao geradas pelo FP-Growth. Possui a mesma leitura das regras do Apriori.

### `reports/tables/kmeans_product_clusters.csv`

Lista cada produto, o cluster em que ele foi colocado pelo K-Means e a distancia ate o centro do cluster.

### `reports/tables/kmeans_recommendations.csv`

Recomendacoes geradas dentro dos clusters do K-Means. Contem `product`, `recommended_product`, `cluster` e `recommendation_score`.

### `reports/tables/method_comparison.csv`

Tabela final de comparacao entre os metodos. Inclui tempo de execucao, quantidade de regras ou recomendacoes e metricas medias.

## Validacao

Para validar o projeto:

```bash
python -m pytest -q
python -m ruff check .
```

## Observacoes

Os arquivos de dados e resultados sao ignorados pelo Git para evitar versionar arquivos grandes ou derivados. O repositorio deve guardar o codigo, a estrutura e a documentacao; a base original e as tabelas geradas ficam locais.
