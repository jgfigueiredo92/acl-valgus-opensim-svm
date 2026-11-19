# O joelho sob carga: aprendizado de máquina e lesão do ligamento cruzado anterior no futebol

Repositório de códigos, dados derivados e resultados da dissertação de mestrado de João Gabriel da Silva Figueiredo, apresentada ao Programa de Pós-Graduação em Modelagem e Simulação de Biossistemas (PPGMSB) da Universidade do Estado da Bahia (UNEB), Campus II, Alagoinhas.

Orientador: Prof. Dr. Erivelton Nonato de Santana. Coorientador: Prof. Dr. José Roberto de Araújo Fontoura.

DOI (versão 1.0.1): [10.5281/zenodo.24358610](https://doi.org/10.5281/zenodo.24358610)

## Objetivo

Estimar, por simulação neuromusculoesquelética no OpenSim, a sobrecarga do joelho durante a mudança de direção de 90° (v-cut) e avaliar se variáveis biomecânicas extraídas das simulações discriminam, por Máquinas de Vetores de Suporte (SVM) com kernel linear, ciclos de elevada sobrecarga em valgo em participantes não utilizados no treinamento.

## Dados de entrada (não redistribuídos)

Os dados experimentais e os modelos musculoesqueléticos escalonados pertencem à base pública de Nitschke et al.:

- NITSCHKE, M. et al. *Optical motion capturing of change of direction motions reconstructed with inverse kinematics and dynamics and optimal control simulation*. Zenodo, 2022. DOI: [10.5281/zenodo.6949012](https://doi.org/10.5281/zenodo.6949012).
- NITSCHKE, M. et al. Change the direction: 3D optimal control simulation by directly tracking marker and ground reaction force data. *PeerJ*, v. 11, e14852, 2023. DOI: [10.7717/peerj.14852](https://doi.org/10.7717/peerj.14852).

Foram analisados os Participantes 02 a 11, com três ensaios de v-cut cada (30 ciclos).

## Sequência de execução

Os códigos estão em notebooks Jupyter, salvos com as respectivas saídas, o que permite conferir os resultados sem executá-los.

| Ordem | Arquivo | Função |
|---|---|---|
| 1 | `fase3_reprocessamento_opensim.ipynb` | Processamento dos ensaios no OpenSim 4.5: filtragem Butterworth a 15 Hz, Dinâmica Inversa, Otimização Estática e Análise de Reação Articular do joelho direito, com comparação da Dinâmica Inversa aos momentos de referência dos autores da base |
| 2 | `Comparar controle P02 0122.ipynb` | Controle do ensaio P02/0123: compara o P02/0122 processado com a janela normal e com início 50 ms antes |
| 3 | `Fase4 extracao desfecho frontal.ipynb` | Extração do desfecho (pico do momento em valgo na aceitação de peso, em Nm/kg) e dos sete preditores |
| 4 | `Fase5 validacao svm desfecho frontal.ipynb` | SVM linear (C = 1, pesos de classe balanceados): Nível 1, GroupKFold aninhado (K = 3) com limiar por G-Mean no laço interno; Nível 2, validação LOSO com bootstrap por conglomerado (2.000 réplicas); vetor de pesos |
| 5 | `Fase6 robustez svm.ipynb` | Análises de sensibilidade: limiar P75 recalculado no treino, teste de permutação no nível do participante (1.000), exclusão do Participante 09, VIF e comparação entre validação por ciclo e por participante (50 repetições) |
| 6 | `Fase7 robustez contato.ipynb` | Extração do desfecho com exclusão dos primeiros 10 ms após o contato inicial |
| 7 | `GERAÇÃO DE FIGURAS.ipynb` e `gerar_figuras_cap3.py` | Geração das Figuras 3 e 4 da dissertação (validação da Dinâmica Inversa e desfecho por participante), em versões de notebook e de script |

## Arquivos de dados e resultados

| Arquivo | Conteúdo |
|---|---|
| `dataset_desfecho_frontal.xlsx` | Desfecho, rótulo e sete preditores por ciclo (30 ciclos), gerado na etapa 3 |
| `dataset_desfecho_frontal_ignora10ms.xlsx` | Idem, com o desfecho extraído sem os primeiros 10 ms após o contato (etapa 6) |
| `validacao_ID_30.csv` | Concordância entre a Dinâmica Inversa deste estudo e a dos autores da base nos 30 ensaios (RMSE e r de Pearson para quatro momentos articulares) |
| `fase3_validacao_ID.csv` e `fase3_relatorio.txt` | Registro da execução da etapa 1 para o Participante 02 (ensaios 0122 e 0123) |
| `fase5_resultados.txt` | Saída completa da etapa 4 |
| `fase5_predicoes_oof.csv` | Predições fora da amostra por ciclo: participante, massa, pico do momento em valgo, desfecho normalizado, classe, escore e predição do Nível 1 e escore e predição do LOSO |
| `fase5_pesos.csv` | Vetor de pesos do SVM ajustado com todos os ciclos e média e desvio padrão nas partições do Nível 1 e do LOSO |
| `fase5_nivel1.png` e `fase5_nivel2.png` | Matrizes de confusão e curvas ROC dos Níveis 1 e 2 |
| `fase6_robustez.txt` | Saída completa da etapa 5 |
| `fase7_robustez_contato.txt` | Saída completa da etapa 6 |

Observações:
- Os arquivos `fase5_predicoes_oof.csv`, `fase5_pesos.csv` e `fase3_validacao_ID.csv` usam ponto e vírgula como separador e vírgula como separador decimal. O arquivo `validacao_ID_30.csv` usa vírgula como separador e ponto como separador decimal.
- O arquivo de predições identifica o participante, mas não o número do ensaio.
- As Figuras 7 e 8 da dissertação foram geradas a partir dos valores das saídas das etapas 4 e 5 e não estão incluídas neste repositório.

## Como reproduzir

1. Faça o download da base de Nitschke et al. no Zenodo.
2. Nos notebooks, os caminhos estão definidos no início do código para o computador original (`C:\JG\opensim\Dados_Zenodo`, `C:\JG\opensim\Resultados_FASE3` e `C:\OpenSim 4.5\bin\opensim-cmd.exe`). Substitua-os pelos caminhos do seu computador.
3. Execute as etapas na ordem da tabela. As etapas 3 a 7 dispensam o OpenSim depois que as saídas da etapa 1 existem.

Requisitos: Python 3 com numpy, pandas, scipy, scikit-learn e matplotlib (ver `requirements.txt`), além do openpyxl para a leitura dos arquivos `.xlsx`, e OpenSim 4.5 (ferramentas de linha de comando) para a etapa 1.

## Licenças

Código: MIT (arquivo `LICENSE`). Dados derivados e resultados: CC BY 4.0. Ao utilizar este material, cite também a base original de Nitschke et al.

## Como citar

FIGUEIREDO, J. G. S. **O joelho sob carga**: aprendizado de máquina e lesão do ligamento cruzado anterior no futebol (códigos e dados). Versão 1.0.1. [S. l.]: Zenodo, 2026. DOI: https://doi.org/10.5281/zenodo.24358610.

Consulte também o arquivo `CITATION.cff`.
