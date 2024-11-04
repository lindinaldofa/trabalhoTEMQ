<div align="center">
    <img src='assets/ufpepimes.png' width="100">
    <h4 align="center">
        UNIVERSIDADE FEDERAL DE PERNAMBUCO
        <br>
        PIMES - PROGRAMA DE PÓS-GRADUAÇÃO EM ECONOMIA
        <br>
        TÓPICOS ESPECIAIS EM MÉTODOS QUANTITATIVOS
        <br>
        <br>
        <br>
        RELAÇÃO ENTRE CRÉDITO E COMPLEXIDADE ECONÔMICA NOS ESTADOS BRASILEIROS:
        <br>
        VERIFICANDO SE HÁ DIFERENÇAS ENTRE ESTADOS COM BAIXA, MÉDIA E ALTA COMPLEXIDADE NO ANO DE 2022.
        <br>
        <br>
    </h4>
        <br>
        Trabalho Final para Conclusão da Disciplina
        <br>
        ministrada pelo <strong>Prof. Dr. Gustavo Ramos Sampaio</strong>.
        <br>
        <br>
        <br>
        Estudante: <strong>Lindinaldo Freitas de Alencar</strong>.
        <br>
        <br>
</div>
<hr />

### ARQUIVOS DO PROJETO:

- [resultados.ipynb](notebooks/resultados.ipynb)

Notebook principal do projeto. Contém o conjunto dos resultados, indicadores que foram calculados e a aplicação dos Testes de Kruskal-Wallis e de Donn.

- [funcoes.py](notebooks/funcoes.py)

Arquivo python que reune as principais funções utilizadas no projeto. Especialmente as responsáveis palo cálculo dos indicadores de complexidade econômica e de convergência com o crédito.

- [rais.ipynb](notebooks/rais.ipynb)

Notebook utilizado para tratar os dados da RAIS e criar a base de dados [rais2022.pkl](assets/rais2022.pkl).

- [scr.ipynb](notebooks/scr.ipynb)

Notebook utilizado para tratar os dados do SCR e criar a base de dados [scr122022.pkl](assets/scr122022.pkl).

- [basefinal.ipynb](notebooks/basefinal.ipynb)

Notebook utilizado para unificar as bases de dados (RAIS e SCR), calcular os indicadores de complexidade econômica e os índices de convergência com o crédito, resultando na base de dados final [df_2022.csv](assets/df_2022.csv)


<hr />

### RESUMO:
Diferentes interpretações da economia capitalista conferem ao crédito um importante papel para manutenção e expansão do nível de atividade econômica, estando também relacionado com as condições que permitem o crescimento econômico e o desenvolvimento de uma sociedade. Dado o cenário de desigualdades regionais que caracteriza o Brasil e assumindo índices de complexidade econômica como indicativos de desenvolvimento, torna-se viável analisar empiricamente as relações entre o crédito e a atividade econômica. Desse modo, será verificada a existência de diferenças na relação entre crédito e complexidade econômica para os estados brasileiros classificados em grupos de baixa, média e alta complexidade econômica, tendo como enfoque o ano de 2022.


##### O presente trabalho tem como referência o Projeto de Dissertação de Lindinaldo Freitas de Alencar, sob orientação do Professor Dr. João Policarpo Rodrigues Lima. [Ver Projeto.](assets/PROJETO%20DE%20PESQUISA%20-%20CRÉDITO%20E%20DESENVOLVIMENTO.pdf)

### DADOS:
Os dados utilizados são da Relação Anual de Informações Sociais – RAIS e do Sistema de Informações de Créditos – SCR, referentes ao ano de 2022. Os microdados da RAIS são fornecidos pelo Programa de Disseminação das Estatísticas do Trabalho, vinculado ao Ministério do Trabalho e Emprego do Governo Federal. Os dados do SCR são fornecidos pelo Departamento de Monitoramento do Sistema Financeiro – Desig do Banco Central do Brasil – Bacen.

Os dados de massa salarial em nível regional provenientes da RAIS serão utilizados para o cálculo do Índice de Complexidade Econômica Regional – ICE-R, conforme proposto por Freitas (2019). Para o cálculo da massa salarial será considerada a soma dos salários nominais do mês de dezembro para os vínculos ativos em 31 de dezembro de cada ano. Os dados das carteiras de crédito ativas por unidade da federação do SCR serão utilizados em conjunto com a RAIS para o cálculo do Índice de Convergência entre Diversificação e Crédito – ICDC e do Índice de Convergência entre Ubiquidade e Crédito – ICUC. Serão considerados apenas os dados das carteiras de crédito relativos as operações com pessoas jurídicas, agregados por estado e pela Classificação Nacional de Atividades Econômicas – CNAE Subclasses.

### ESTRATÉGIA EMPÍRICA

O Índice de Complexidade Econômica Regional – ICE-R será calculado utilizando o método dos reflexos, conforme Hidalgo et al (2007), mas baseado na massa salarial em nível regional como proposto por Freitas (2019). Segundo Freitas et al (2023), o primeiro passo dessa abordagem passa pelo cálculo das vantagens comparativas reveladas por região e período. Tomando $w_{rs}$ como a massa salarial do setor $s$ na região $r$ e adequando o índice de Balassa (1965), podemos definir um quociente locacional $(QLw_{rs})$ para cada ano:
$$
QLw_{rs} = \frac{\frac{w_{rs}}{\sum_sw_{rs}}}{\frac{\sum_rw_{rs}}{\sum_r\sum_sw_{rs}}}
\quad (1)
$$

Assim, quando $QL_{rs}$ é maior ou igual a 1 a região $r$ possui vantagem comparativa no setor $s$. Com as informações sobre quais regiões possuem vantagens comparativas em cada setor, será construída a matriz $M_{rs}$ com as linhas formadas pelas regiões e as colunas pelos setores, definida por:
$$
M_{rs} = \left\{
\begin{aligned}
 1,\ se\ QLw_{rs} \geq 1 \\
 0, \ se \ QLw_{rs} < 1
 \end{aligned}
\right.
\quad(2)
$$

Em seguida, são definidas medidas de diversificação $k_{r,0}$ e ubiquidade $k_{s,0}$, dadas por:
$$
k_{r,0} = \sum_s M_{rs} \quad(3) \\
$$
$$
k_{s,0} = \sum_r M_{rs} \quad(4)
$$

Dessa forma, o indicador (3) representa a diversificação das regiões, fornecendo a quantidade de setores em que há vantagem comparativa na região $r$, enquanto (4) expressa a ubiquidade, dada pela quantidade de regiões onde o mesmo setor possui vantagem comparativa.

A partir dos indicadores de diversificação e ubiquidade são calculados os índices de complexidade econômica das regiões e dos setores, seguindo os procedimentos definidos em Freitas et al (2023) e outros autores para aplicação do método dos reflexos. Com a obtenção do Índice de Complexidade Econômica Regional se torna possível classificar as regiões por nível de complexidade (alta, média e baixa), considerando os tercis do ICE-R.

O Índice de Convergência entre Diversificação e Crédito – ICDC também terá como primeiro passo o cálculo das vantagens comparativas reveladas por região e período, entretanto, o quociente locacional será agora calculado em relação ao crédito disponível. Assim, seja $c_{rs}$ o montante da carteira de crédito do setor %s% na região %r%, então o $QLc_{rs}$ será dado por:
$$
QLc_{rs} = \frac{\frac{c_{rs}}{\sum_s c_{rs}}}{\frac{\sum_r c_{rs}}{\sum_r\sum_s c_{rs}}}
\quad (5)
$$

Analogamente, quando $QLc_{rs}$ é maior ou igual a 1 a região $r$ possui vantagem comparativa no setor $s$. Semelhante a construção da matriz $M_{rs}$, com as regiões nas linhas e os setores nas colunas, serão construídas as matrizes $C_{rs}$ e $D_{rs}$:
$$
C_{rs} = \left\{
\begin{aligned}
 1,\ se\ QLw_{rs} \ e\ QLc_{rs} \geq 1 \\
 0, \ se \ QLw_{rs} \ e\ QLc_{rs} < 1
 \end{aligned}
\right.
\quad(6)
$$
$$
D_{rs} = \left\{
\begin{aligned}
 1,\ se\ QLw_{rs} \geq 1 \ e\ QLc_{rs} < 1 \\
 0, \ se\ QLw_{rs} < 1 \ ou\ QLc_{rs} \geq 1
 \end{aligned}
\right.
\quad(7)
$$

Bem como são definidas as seguintes medidas por região:
$$
co_r = \sum_s C_{rs} \quad(8)
$$
$$
di_r = \sum_s D_{rs} \quad(9)
$$

Onde $co_r$ fornece a quantidade de setores na região $r$ que possuem vantagens comparativas reveladas baseadas tanto na massa salarial quanto na disponibilidade de crédito, enquanto $di_r$ representa a quantidade de setores que possuem VCR apenas com base na massa salarial.

Assim, o Índice de Convergência entre Diversificação e Crédito para cada região será obtido por:
$$
ICDC_r = \frac{(co_r - di_r)}{(co_r + di_r)} \quad(10)
$$

Note que $co_r + di_r = k_{r,0}$, logo:
$$
ICDC_r = \frac{(co_r - di_r)}{k_{r,0}} \quad(11)
$$

O $ICDC_r$ compara a diferença entre $co_r$ e $di_r$ com a soma entre elas, assumindo valores no intervalo $[-1,1]$. Note que $di_r=0\Rightarrow co_r=k_{r,0}\Rightarrow ICDC_r=1$, ou seja, quando todos os setores na região $r$ que possuem vantagens comparativas reveladas baseadas na massa salarial também possuem pela disponibilidade de crédito, temos uma convergência perfeita. Analogamente, quando $co_r=0$ temos que $di_r=k_{r,0}\Rightarrow ICDC_r=-1$, indicando que não há nenhuma convergência.

De modo análogo, pode ser aplicado o mesmo procedimento para obtenção do Índice de Convergência entre Ubiquidade e Crédito – ICUC por setor, resultando em:
$$
ICUC_s = \frac{(co_s - di_s)}{k_{s,0}} \quad(12)
$$

Com a obtenção do $ICDC_r$ e a divisão dos estados em grupos por nível de complexidade será possível calcular medidas descritivas (média, mediana, desvio padrão) para cada grupo, bem como analisar e comparar os histogramas e os valores das medidas descritivas entre os grupos, além da aplicação do Teste de Kruskal-Wallis e do Teste de Donn. Desse modo, poderá ser identificado se há diferenças e como elas variam entre as regiões de baixa, média e alta complexidade.

### REFERÊNCIAS

FREITAS, Elton Eduardo et al. Indústrias relacionadas, complexidade econômica e diversificação regional: uma aplicação para microrregiões brasileiras. 2019.

FREITAS, Elton Eduardo et al. Dataviva: espaço de atividades e indicadores regionais de complexidade econômica. Cedeplar, Universidade Federal de Minas Gerais, 2023.

HIDALGO, César A. et al. The product space conditions the development of nations. Science, v. 317, n. 5837, p. 482-487, 2007.

<hr />

Para o cálculo dos indicadores de complexidade foi tomado como referência a biblioteca [py-ecomplexity](https://github.com/cid-harvard/py-ecomplexity). Mas a aplicação do método dos reflexos foi implementada tendo como referência Freitas et al (2023).