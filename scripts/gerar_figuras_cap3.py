"""
Gera as Figuras 3 e 4 do Capítulo 3 e as tabelas de apoio.

Entradas (na PASTA_FASE3):
  validacao_ID_30.csv               concordância da Dinâmica Inversa nos 30 ensaios
  dataset_desfecho_frontal.xlsx     saída da fase 4 (30 ciclos)
e os modelos Participant_XX.osim do Zenodo (massas corporais).

Saídas (na mesma pasta):
  figura3_validacao_ID.png/.pdf
  figura4_desfecho_participante.png/.pdf
"""
import glob, os, xml.etree.ElementTree as ET
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

PASTA_FASE3 = r'C:\JG\opensim\Resultados_FASE3'
PASTA_ZENODO = (r'C:\JG\opensim\Dados_Zenodo'
                r'\Nitschke_et_al_Change_of_Direction_Marker_Simulation')
INK, GRID, CINZA, AZUL, LARANJA = '#2B2B2B', '#E3E6EA', '#9AA3AE', '#2F6DB5', '#C2410C'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})


def massa(p):
    arq = glob.glob(os.path.join(PASTA_ZENODO, f'Participant_{p}', '**', f'Participant_{p}.osim'),
                    recursive=True)[0]
    return sum(float(b.find('mass').text) for b in ET.parse(arq).getroot().iter('Body')
               if b.find('mass') is not None and b.find('mass').text)


def estilo(ax):
    ax.grid(axis='y', color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'): ax.spines[sp].set_color('#B8BEC6')
    ax.tick_params(colors=INK, length=0)


def salvar(fig, nome):
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(PASTA_FASE3, f'{nome}.{ext}'), dpi=300,
                    bbox_inches='tight', facecolor='white')


# ---------- Figura 3: concordância da Dinâmica Inversa ----------
v = pd.read_csv(os.path.join(PASTA_FASE3, 'validacao_ID_30.csv'),
                dtype={'participante': str, 'trial': str})
v['participante'] = v.participante.str.zfill(2)
massas = {p: massa(p) for p in v.participante.unique()}
v['RMSE_Nmkg'] = v.RMSE_Nm / v.participante.map(massas)
nomes = {'knee_angle_r_moment': 'Flexão do\njoelho', 'hip_adduction_r_moment': 'Adução do\nquadril',
         'hip_flexion_r_moment': 'Flexão do\nquadril', 'ankle_angle_r_moment': 'Flexão plantar\ndo tornozelo'}
ordem = list(nomes)
rng = np.random.default_rng(1)
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, col, tit, yl in ((axs[0], 'RMSE_Nmkg', '(A) RMSE normalizado pela massa', 'RMSE (Nm/kg)'),
                         (axs[1], 'r', '(B) Coeficiente de correlação de Pearson', 'r')):
    for i, k in enumerate(ordem):
        s = v[v.momento == k]; x = i + rng.uniform(-0.18, 0.18, len(s)); o = (s.participante != '09').to_numpy()
        ax.scatter(x[o], s[col][o], s=26, color=CINZA, edgecolor='white', linewidth=0.8, zorder=3,
                   label='Demais participantes' if i == 0 else None)
        ax.scatter(x[~o], s[col][~o], s=34, color=AZUL, edgecolor='white', linewidth=0.8, zorder=4,
                   label='Participante 09' if i == 0 else None)
        ax.hlines(s[col].median(), i - 0.3, i + 0.3, color=INK, linewidth=2, zorder=5,
                  label='Mediana' if i == 0 else None)
    ax.set_xticks(range(4)); ax.set_xticklabels([nomes[k] for k in ordem])
    ax.set_title(tit, fontsize=11, color=INK, loc='left'); ax.set_ylabel(yl, color=INK); estilo(ax)
axs[0].set_ylim(0, None); axs[1].set_ylim(0.78, 1.01)
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.07, 1, 1)); salvar(fig, 'figura3_validacao_ID')

# ---------- Figura 4: desfecho por participante ----------
d = pd.read_excel(os.path.join(PASTA_FASE3, 'dataset_desfecho_frontal.xlsx'), dtype={'Participante': str})
d['Participante'] = d.Participante.str.zfill(2)
d['valgo_kg'] = d.Momento_Valgo_Pico_Nm / d.Participante.map({p: massa(p) for p in d.Participante.unique()})
p75 = np.quantile(d.valgo_kg, 0.75); d['classe'] = (d.valgo_kg >= p75).astype(int)
ordem = d.groupby('Participante').valgo_kg.median().sort_values().index.tolist()
fig, ax = plt.subplots(figsize=(9, 4.4))
for i, p in enumerate(ordem):
    s = d[d.Participante == p]
    ax.vlines(i, s.valgo_kg.min(), s.valgo_kg.max(), color='#CBD1D8', linewidth=2, zorder=2)
    for _, r in s.iterrows():
        ax.scatter(i, r.valgo_kg, s=44, color=LARANJA if r.classe else CINZA, marker='D' if r.classe else 'o',
                   edgecolor='white', linewidth=0.9, zorder=4)
ax.axhline(p75, color=INK, linestyle=(0, (5, 3)), linewidth=1.2, zorder=3)
ax.text(1.5, p75 + 0.008, f'P75 = {p75:.3f} Nm/kg'.replace('.', ','), ha='center', va='bottom', color=INK,
        fontsize=9.5, bbox=dict(facecolor='white', edgecolor='none', pad=1))
ax.axhline(0, color='#B8BEC6', linewidth=0.8, zorder=1)
ax.set_xticks(range(len(ordem))); ax.set_xticklabels([f'P{p}' for p in ordem])
ax.set_xlabel('Participante (ordenado pela mediana)', color=INK)
ax.set_ylabel('Pico do momento em valgo (Nm/kg)', color=INK); estilo(ax)
n1 = int(d.classe.sum())
ax.legend(handles=[
    Line2D([], [], marker='o', ls='', color=CINZA, markeredgecolor='white', markersize=8,
           label=f'Classe 0 (Padrão de Referência, n = {len(d) - n1})'),
    Line2D([], [], marker='D', ls='', color=LARANJA, markeredgecolor='white', markersize=7,
           label=f'Classe 1 (Elevada Sobrecarga em Valgo, n = {n1})')], loc='upper left', frameon=False)
fig.tight_layout(); salvar(fig, 'figura4_desfecho_participante')
print(f'Figuras salvas em {PASTA_FASE3} | P75 = {p75:.4f} Nm/kg | Classe 1 = {n1}')
