# Vias de geração de TDC — mapa das 6 linhas de negócio (expansão)
> PU 14 · 2026-06-28. Cada via = uma forma de um imóvel gerar potencial transferível = uma linha de negócio.
> Hoje só a **via 1** (tombados/ZEPEC) está montada. Este mapa liga cada via ao seu **substrato de dados**, ao **engine** (`engines/tdc/pcpt.py`) e ao que falta. Substrato de parques (via 5) já extraído.

| Via | Gera potencial por | Engine (pcpt.py) | Fi | Substrato de dados | Status |
|---|---|---|---|---|---|
| **1. Preservação cultural** (tombados/ZEPEC) | dono **fica** com o imóvel | `pcpt_sem_doacao` (Art.125) | 1 | **lista ZEPEC** (`zepec/ferramenta/`, 6.131) | ✅ **montada** |
| **2. Preservação ambiental** (ZEPAM) | dono fica | `pcpt_sem_doacao` (Art.124 II) | 1 | ZEPAM no Quadro 3 (CAbas 0,1) + **perímetros ZEPAM** (geo) | 🔒 geo + gate FUNDURB/SVMA/TCA |
| **3. Regularização fundiária** | dono **doa** o terreno | `pcpt_com_doacao` (Art.127) | **0,8** | ZEIS/baixa renda (**perímetros, geo**) | 🔒 geo |
| **4. Provisão de HIS** | dono doa | `pcpt_com_doacao` | **1,9** | ZEIS (**perímetros, geo**) | 🔒 geo |
| **5. Parques planejados** | dono doa | `pcpt_com_doacao` | **1,4 / 1,0** | **`tabelas/quadro7-parques.csv`** (272 parques, **147 propostos**) | ✅ **substrato extraído** |
| **6. Melhoramentos viários** (corredores de ônibus) | dono doa | `pcpt_com_doacao` | **2,0** | perímetros de corredores (**geo**) | 🔒 geo |

## Leitura comercial
- **Vias 3-6 = via COM doação** (Art.126/127): dono **doa o imóvel** e recebe potencial (CAmax × Fi até 2,0). **Público DISJUNTO da lista ZEPEC** — são donos de terreno em perímetros de parque/corredor/ZEIS, não tombados. (Codex Comercial R18 / Cálculos.)
- **Vias 1 e 2 = SEM doação** (dono fica) — a via 1 é o nosso produto; a via 2 (ZEPAM) é a expansão mais próxima (mesma lógica "dono fica", só muda o selo e os gates ambientais).
- **O que destrava as vias geo (2,3,4,6):** os **perímetros de zoneamento** (ZEPAM/ZEIS/corredores) — carga geo do Drive (lane B-9). Com eles + o engine (já pronto) + Atc (IPTU), cada via vira uma lista análoga à da via 1.

## Próximo passo concreto de cada via
- **Via 5 (parques):** cruzar `quadro7-parques.csv` (147 propostos) × cadastro para achar os terrenos doáveis. Engine e Fi prontos.
- **Vias 2/3/4/6:** pedir os perímetros geo (B-9); o engine já cobre as fórmulas e os Fi.
