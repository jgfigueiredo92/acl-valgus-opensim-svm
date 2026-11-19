# O joelho sob carga: aprendizado de máquina e lesão do ligamento cruzado anterior no futebol

Repositório de códigos, dados derivados e resultados da dissertação de mestrado de João Gabriel da Silva Figueiredo, apresentada ao Programa de Pós-Graduação em Modelagem e Simulação de Biossistemas (PPGMSB) da Universidade do Estado da Bahia (UNEB), Campus II, Alagoinhas.

Orientador: Prof. Dr. Erivelton Nonato de Santana. Coorientador: Prof. Dr. José Roberto de Araújo Fontoura.

## Objetivo

Estimar, por simulação neuromusculoesquelética no OpenSim, a sobrecarga do joelho durante a mudança de direção de 90° (v-cut) e avaliar se variáveis biomecânicas extraídas das simulações discriminam, por Máquinas de Vetores de Suporte (SVM) com kernel linear, ciclos de elevada sobrecarga em valgo em participantes não utilizados no treinamento.

## Dados de entrada (não redistribuídos)

Os dados experimentais e os modelos musculoesqueléticos escalonados pertencem à base pública de Nitschke et al.:

- NITSCHKE, M. et al. *Optical motion capturing of change of direction motions reconstructed with inverse kinematics and dynamics and optimal control simulation*. Zenodo, 2022. DOI: [10.5281/zenodo.6949012](https://doi.org/10.5281/zenodo.6949012).
- NITSCHKE, M. et al. Change the direction: 3D optimal control simulation by directly tracking marker and ground reaction force data. *PeerJ*, v. 11, e14852, 2023. DOI: [10.7717/peerj.14852](https://doi.org/10.7717/peerj.14852).

Para reproduzir o processamento, faça o download da base no Zenodo e informe o caminho da pasta no início de cada script. Foram analisados os Participantes 02 a 11, com três ensaios de v-cut cada (30 ciclos).

## Sequência de execução

| Ordem | Script | Função |
|---|---|---|
| 1 | `scripts/fase3_reprocessamento_opensim.py` | Processamento dos 30 ensaios no OpenSim 4.5: filtragem Butterworth a 15 Hz, Dinâmica Inversa, Otimização Estática e Análise de Reação Articular do joelho direito |
| 2 | `scripts/comparar_controle_P02_0122.py` | Controle do ensaio P02/0123: compara o P02/0122 processado com a janela normal e com início 50 ms antes |
| 3 | `scripts/fase4_extracao_desfecho_frontal.py` | Extração do desfecho (pico do momento em valgo na aceitação de peso, em Nm/kg) e dos sete preditores |
| 4 | `scripts/fase5_validacao_svm_desfecho_frontal.py` | SVM linear (C = 1, pesos de classe balanceados), validação LOSO, GroupKFold aninhado, bootstrap por conglomerado (2.000 réplicas) e vetor de pesos |
| 5 | `scripts/fase6_robustez_svm.py` | Análises de sensibilidade: limiar P75 recalculado no treino, teste de permutação no nível do participante (1.000), exclusão do Participante 09, VIF e comparação entre validação por ciclo e por participante (50 repetições) |
| 6 | `scripts/fase7_robustez_contato.py` | Extração do desfecho com exclusão dos primeiros 10 ms após o contato inicial |
| 7 | `scripts/figuras/` | Geração das figuras da dissertação |

## Conteúdo

- `data/dataset_desfecho_frontal.csv`: desfecho, rótulo e sete preditores por ciclo (30 ciclos).
- `data/dataset_desfecho_frontal_ignora10ms.csv`: idem, com o desfecho extraído sem os primeiros 10 ms após o contato.
- `data/validacao_ID_30.csv` e `data/fase3_validacao_ID.csv`: concordância entre a Dinâmica Inversa deste estudo e os momentos de referência dos autores da base (RMSE e r de Pearson por ensaio).
- `results/fase5_predicoes_oof.csv`: predições fora da amostra do LOSO (participante, ensaio, rótulo, escore de decisão e classe prevista).
- `results/fase5_pesos.csv`: vetor de pesos do SVM.
- `results/*.txt`: saídas das fases 3, 5, 6 e 7, que originam os valores relatados na dissertação.
- `results/figures/`: figuras da dissertação.
- `opensim_outputs/`: resultados da Dinâmica Inversa, da Otimização Estática e da Análise de Reação Articular por ensaio (opcional).

## Requisitos

Python 3 com os pacotes de `requirements.txt` e OpenSim 4.5 (ferramentas de linha de comando) para a etapa 1. As etapas 3 a 7 dispensam o OpenSim depois que as saídas da etapa 1 existem.

## Licenças

Código: MIT (arquivo `LICENSE`). Dados derivados e resultados (`data/` e `results/`): CC BY 4.0. Ao utilizar este material, cite também a base original de Nitschke et al.

## Como citar

FIGUEIREDO, J. G. S. **O joelho sob carga: aprendizado de máquina e lesão do ligamento cruzado anterior no futebol**: códigos e dados. Zenodo, 2026. DOI: [DOI DO REPOSITÓRIO].

Consulte também o arquivo `CITATION.cff`.
