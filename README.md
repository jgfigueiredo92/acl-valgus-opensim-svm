# Knee valgus loading in cutting: OpenSim + linear SVM with subject-independent validation

Code, derived data and out-of-fold predictions for:

J. G. S. Figueiredo, E. N. Santana, J. R. A. Fontoura, J. A. S. Santana, D. B. C. Seabra, J. N. Silva. *Subject-Independent Validation of an Interpretable OpenSim-SVM Pipeline for Classifying Knee Valgus Loading in Cutting Maneuvers.* ACDSA 2027 (IEEE), Paper ID 879.

It also supports the master's dissertation *O joelho sob carga: aprendizado de máquina e lesão do ligamento cruzado anterior no futebol* (PPGMSB, State University of Bahia).

## Input data (not redistributed)

The raw data and scaled musculoskeletal models come from the open dataset of Nitschke et al.:

- M. Nitschke et al., *Optical motion capturing of change of direction motions reconstructed with inverse kinematics and dynamics and optimal control simulation*, Zenodo, 2022. doi: [10.5281/zenodo.6949012](https://doi.org/10.5281/zenodo.6949012)
- M. Nitschke et al., *Change the direction: 3D optimal control simulation by directly tracking marker and ground reaction force data*, PeerJ 11:e14852, 2023. doi: [10.7717/peerj.14852](https://doi.org/10.7717/peerj.14852)

Download the dataset from Zenodo and set the data path at the top of each script (see `scripts/config` notes below). The analysis uses participants 02 to 11, three 90° v-cut trials each (30 trials).

## Pipeline

| Order | Script | What it does |
|---|---|---|
| 1 | `scripts/fase3_reprocessamento_opensim.py` | OpenSim 4.5 processing of the 30 trials: 15 Hz Butterworth filtering, inverse dynamics, static optimization and joint reaction analysis (right knee) |
| 2 | `scripts/comparar_controle_P02_0122.py` | Control for trial P02/0123: compares P02/0122 processed with the normal window and with a start 50 ms earlier |
| 3 | `scripts/fase4_extracao_desfecho_frontal.py` | Extracts the outcome (peak knee valgus moment during weight acceptance, N·m/kg) and the seven predictors |
| 4 | `scripts/fase5_validacao_svm_desfecho_frontal.py` | Linear SVM (C = 1, balanced class weights), leave-one-subject-out validation, nested group 3-fold CV, cluster bootstrap (2000 replicates), weight vector |
| 5 | `scripts/fase6_robustez_svm.py` | Sensitivity analyses: P75 recalculated within training folds, subject-level permutation test (1000), exclusion of participant 09, VIF, trial-wise vs subject-wise CV (50 repetitions) |
| 6 | `scripts/fase7_robustez_contato.py` | Outcome extracted ignoring the first 10 ms after initial contact |
| 7 | `scripts/figuras/` | Figure scripts (dissertation and paper) |

## Repository contents

- `data/dataset_desfecho_frontal.csv`: outcome, class label and seven predictors per trial (30 trials).
- `data/dataset_desfecho_frontal_ignora10ms.csv`: same, with the outcome extracted ignoring the first 10 ms after initial contact.
- `data/validacao_ID_30.csv`, `data/fase3_validacao_ID.csv`: agreement between our inverse dynamics and the reference moments of the dataset authors (RMSE and Pearson r per trial).
- `results/fase5_predicoes_oof.csv`: out-of-fold LOSO predictions (participant, trial, label, decision score, predicted class).
- `results/fase5_pesos.csv`: SVM weight vector.
- `results/*.txt`: printed outputs of phases 3, 5, 6 and 7.
- `results/figures/`: figures of the dissertation and the paper.
- `opensim_outputs/`: inverse dynamics, static optimization and joint reaction results per trial (optional, see note).

## Requirements

Python 3 with the packages in `requirements.txt`, and OpenSim 4.5 (command-line tools) for step 1. Steps 3 to 7 run without OpenSim once the step 1 outputs exist.

## Licenses

Code: MIT (see `LICENSE`). Derived data and results in `data/` and `results/`: CC BY 4.0. Please also cite the original dataset of Nitschke et al.

## How to cite

See `CITATION.cff`, or cite the archived release: [REPOSITORY DOI].
