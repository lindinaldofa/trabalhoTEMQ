import numpy as np
import pandas as pd

# Para o cálculo dos indicadores de complexidade foi tomado como referência a biblioteca py-ecomplexity disponíbel em https://github.com/cid-harvard/py-ecomplexity

# Funções de preparação do DataFrame:
def rename_cols(df, cols):
    """
    Função para padronizar os nomes das colunas que serão utilizadas.
    Informe cols como um dict como no exemplo {'tempo': 'Ano', 'lugar':'ID IBGE', 'setor':'ID CNAE', 'valor':'Massa Salarial'}
    """
    cols_map_inv = {v: k for k, v in cols.items()}
    df = df.rename(columns=cols_map_inv)
    df = df[["tempo", "lugar", "setor", "valor"]]
    return df

def clean_data(df, t):
    """
    Função para evitar erros futuros.
    Remove linhas com medidas de diversificação ou ubiquidade iguais a zero para evitar erros de ZeroDivision no processo de normalização.
    """
    # Substitui valores ausentes por 0.
    if df.valor.isnull().values.any():
        df.valor.fillna(0, inplace=True)

    data_t = df[df.tempo == t].copy()
    # Verifica se há zeros.
    val_diversity_check = (
        data_t.reset_index().groupby(["lugar"])["valor"].sum().reset_index()
    )
    val_ubiquity_check = (
        data_t.reset_index().groupby(["setor"])["valor"].sum().reset_index()
    )
    val_diversity_check = val_diversity_check[val_diversity_check.valor != 0]
    val_ubiquity_check = val_ubiquity_check[val_ubiquity_check.valor != 0]
    
    # Remove informações com zero.
    data_t = data_t.reset_index()
    data_t = data_t.merge(
        val_diversity_check[["lugar"]], on="lugar", how="right"
    )
    data_t = data_t.merge(
        val_ubiquity_check[["setor"]], on="setor", how="right"
    )
    data_t.set_index(["index"], inplace=True)
    
    return data_t


# Calculando os indicadores de complexidade:

def create_export_matrix(data, year):
    """Transforma os dados em uma matriz região-setor para um determinado período."""
    pivot_table = data[data['tempo'] == year].pivot_table(index='lugar', columns='setor', values='valor', aggfunc='sum', fill_value=0)
    return pivot_table

def calcule_ql(matrix):
    """Cria uma matriz com os quocientes locacionais - QL."""
    row_sums = matrix.sum(axis=1)
    col_sums = matrix.sum(axis=0)
    total_sum = matrix.values.sum()
    
    expected = np.outer(row_sums, col_sums) / total_sum
    ql = matrix / expected
    return ql

def binarize_ql(ql_matrix, threshold=1):
    """Cria a matriz M, uma matriz binária com as Vantagens Comparativas Reveladas."""
    return (ql_matrix >= threshold).astype(int)


def calcule_diversity_ubiquity(binary_matrix):
    """Calcula as medidas de diversificação e ubiquidade."""
    diversity = binary_matrix.sum(axis=1)
    ubiquity = binary_matrix.sum(axis=0)
    return diversity, ubiquity

def method_of_reflections(binary_matrix, iterations=19):
    """
    Aplica o método dos reflexos para calcular os índices de complexidade.
    Número de iterações padrão definido como 19 para correspondência dos resultados com trabalhos já publicados.
    """
    Kr_0 = binary_matrix.sum(axis=1)
    Ks_0 = binary_matrix.sum(axis=0)

    Kr = Kr_0.copy()
    Ks = Ks_0.copy()
    
    for _ in range(iterations):
        Kr_new = binary_matrix.dot(Ks) / Kr_0
        Ks_new = binary_matrix.T.dot(Kr) / Ks_0
        Kr, Ks = Kr_new, Ks_new

    Kr = binary_matrix.dot(Ks) / Kr_0
    
    Kr_mean = Kr.mean()
    Kr_std = Kr.std()
    ice = (Kr - Kr_mean) / Kr_std

    Ks_mean = Ks.mean()
    Ks_std = Ks.std()
    ics = (Ks - Ks_mean) / Ks_std

    return Kr_0, Ks_0, ice, ics

def calcule_ic(data,cols):
    """
    Função prinicipal para calcular os índices de complexidade.
    Recebe o DataFrame com a informação das colunas que serão utilizadas e retorna um DataFrame com os resultados.
    Informe cols como um dict como no exemplo {'tempo': 'Ano', 'lugar':'ID IBGE', 'setor':'ID CNAE', 'valor':'Massa Salarial'}
    """
    data = rename_cols(data,cols)
    years = data['tempo'].unique()
    result_list = []

    for year in years:
        df = clean_data(data, year)
        export_matrix = create_export_matrix(df, year)
        ql_matrix = calcule_ql(export_matrix)
        binary_matrix = binarize_ql(ql_matrix)
        Kr, Ks, ice, ics = method_of_reflections(binary_matrix)
        
        # Cria um DataFrame temporário para armazenar os resultados do ano corrente.
        temp_df = pd.DataFrame({
            'lugar': export_matrix.index.repeat(export_matrix.shape[1]),
            'setor': np.tile(export_matrix.columns, export_matrix.shape[0]),
            'tempo': year,
            'QL': ql_matrix.values.flatten(),
            'M': binary_matrix.values.flatten(),
            'Kr': np.repeat(Kr, export_matrix.shape[1]),
            'Ks': np.tile(Ks, export_matrix.shape[0]),
            'ICE': np.repeat(ice, export_matrix.shape[1]),
            'ICS': np.tile(ics, export_matrix.shape[0])
        })
        
        result_list.append(temp_df)
    
    # Concatena todos os DataFrames temporários.
    result_df = pd.concat(result_list, ignore_index=True)
    
    # Merge com o DataFrame original para manter todas as colunas.
    final_df = pd.merge(data, result_df, on=['lugar', 'setor', 'tempo'])
    
    return final_df


# Outras Funções

def calcule_m(data,cols):
    """
    Calcula a Matriz M com as Vantagens Comparativas Reveladas de modo direto.
    Retorna o DataFrame original com as colunas QL e M, respectivamente o quociente locacional e a matriz M.
    Informe cols como um dict como no exemplo {'tempo': 'Ano', 'lugar':'ID IBGE', 'setor':'ID CNAE', 'valor':'Massa Salarial'}
    """
    data = rename_cols(data,cols)
    years = data['tempo'].unique()
    result_list = []

    for year in years:
        df = clean_data(data, year)
        export_matrix = create_export_matrix(df, year)
        ql_matrix = calcule_ql(export_matrix)
        binary_matrix = binarize_ql(ql_matrix)
        
        # Criar DataFrame temporário para armazenar os resultados do ano corrente
        temp_df = pd.DataFrame({
            'lugar': export_matrix.index.repeat(export_matrix.shape[1]),
            'setor': np.tile(export_matrix.columns, export_matrix.shape[0]),
            'tempo': year,
            'QL': ql_matrix.values.flatten(),
            'M': binary_matrix.values.flatten(),
        })
        
        result_list.append(temp_df)
    
    # Concatenar todos os DataFrames temporários
    result_df = pd.concat(result_list, ignore_index=True)
    
    # Merge com o DataFrame original para manter todas as colunas
    final_df = pd.merge(data, result_df, on=['lugar', 'setor', 'tempo'])
    
    return final_df


# Função para Calcular os indicadores de convergência
def calcule_iconv(c,d):
    """
    Cálculo de indicadores de convergência.
    Aplica a fórmula (c-d)/(c+d) para comparar a diferença entre c e d. onde c indica a medida de convergência e d a medida de divergência.
    Assim, quanto mais c for maior que d o resultado se aproxima de 1. E quanto mais c < d o resultado se aproxima de -1. 
    """
    if c+d != 0:
        i = (c-d)/(c+d)
    else:
        i = None
    return i
