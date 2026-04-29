"""
app.py — Calcolatore Margini & Sconti a Cascata
Avvio: streamlit run app.py
"""

import streamlit as st

# ──────────────────────────────────────────────
# CONFIGURAZIONE PAGINA
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Margini & Sconti",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CSS — MOBILE FIRST, FONT GRANDI, STILE PULITO
# ──────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sfondo pagina ── */
[data-testid="stAppViewContainer"] {
    background: #f0f2f6;
}
[data-testid="stAppViewBlockContainer"] {
    max-width: 560px;
    padding: 1rem 1.2rem 3rem;
    margin: 0 auto;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1.6rem;
    text-align: center;
}
.app-header h1 {
    color: #fff;
    font-size: 1.55rem;
    font-weight: 700;
    margin: 0 0 0.25rem;
    letter-spacing: -0.3px;
}
.app-header p {
    color: #94a3b8;
    font-size: 0.88rem;
    margin: 0;
}

/* ── Card generica ── */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.4rem 1.5rem 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border: 1px solid #e8edf2;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 1rem;
}

/* ── Risultato metric card ── */
.result-card {
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.result-card.blue   { background: #eff6ff; border: 1px solid #bfdbfe; }
.result-card.green  { background: #f0fdf4; border: 1px solid #bbf7d0; }
.result-card.orange { background: #fffbeb; border: 1px solid #fde68a; }
.result-card.red    { background: #fef2f2; border: 1px solid #fecaca; }
.result-card.gray   { background: #f8fafc; border: 1px solid #e2e8f0; }
.rc-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #475569;
    margin-bottom: 0.15rem;
}
.rc-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    line-height: 1;
}
.rc-value.blue   { color: #1d4ed8; }
.rc-value.green  { color: #15803d; }
.rc-value.orange { color: #b45309; }
.rc-value.red    { color: #b91c1c; }
.rc-value.gray   { color: #334155; }
.rc-icon { font-size: 1.8rem; opacity: 0.25; }

/* ── Alert ── */
.alert-red {
    background: #fef2f2;
    border: 1.5px solid #f87171;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.alert-red-title { font-weight: 700; color: #991b1b; font-size: 1rem; margin-bottom: 0.3rem; }
.alert-red-body  { color: #7f1d1d; font-size: 0.9rem; line-height: 1.5; }

.alert-green {
    background: #f0fdf4;
    border: 1.5px solid #4ade80;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.alert-green-title { font-weight: 700; color: #166534; font-size: 1rem; margin-bottom: 0.3rem; }
.alert-green-body  { color: #14532d; font-size: 0.9rem; }

/* ── Inputs: font grande mobile ── */
input[type="number"], input[type="text"] {
    font-size: 18px !important;
    height: 52px !important;
    border-radius: 10px !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    font-size: 18px !important;
    padding: 0.7rem 1rem !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
}

/* ── Divisore sezione ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 1.4rem 0 1rem;
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e2e8f0;
}

/* ── Pulsante Reset ── */
button[kind="secondary"] {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    height: 48px !important;
}
button[kind="primary"] {
    border-radius: 10px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    height: 52px !important;
    background: #1e3a5f !important;
    border-color: #1e3a5f !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.75rem;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
}

/* ── Nascondi elementi Streamlit ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def fmt_eur(v: float) -> str:
    return f"€ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_pct(v: float) -> str:
    return f"{v:.2f}%"

def result_card(label: str, value: str, icon: str, color: str) -> str:
    return f"""
    <div class="result-card {color}">
        <div>
            <div class="rc-label">{label}</div>
            <div class="rc-value {color}">{value}</div>
        </div>
        <div class="rc-icon">{icon}</div>
    </div>"""

def parse_sconti(testo: str) -> list[float]:
    """Parsa la stringa '40+10+5' in [40.0, 10.0, 5.0]. Ritorna [] se non valido."""
    testo = testo.strip().replace(" ", "").replace(",", ".")
    if not testo:
        return []
    try:
        return [float(x) for x in testo.split("+") if x]
    except ValueError:
        return []

def applica_sconti(prezzo: float, sconti: list[float]) -> tuple[float, float]:
    """Restituisce (prezzo_netto, sconto_totale_%)."""
    netto = prezzo
    for d in sconti:
        netto *= (1 - d / 100)
    sconto_totale = (1 - netto / prezzo) * 100 if prezzo > 0 else 0
    return netto, sconto_totale


# ──────────────────────────────────────────────
# SESSION STATE — reset ad ogni apertura
# ──────────────────────────────────────────────

# Chiavi che vogliamo azzerare al reset
INPUT_KEYS = ["acq", "vnd", "mar", "sconti_str"]

def _init_state():
    defaults = {"acq": 0.0, "vnd": 0.0, "mar": 0.0, "sconti_str": ""}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_tutto():
    for k in INPUT_KEYS:
        del st.session_state[k]
    st.rerun()

_init_state()


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <h1>📊 Margini & Sconti</h1>
    <p>Calcolo rapido su smartphone e desktop</p>
</div>
""", unsafe_allow_html=True)

# Reset TOP
if st.button("🔄  Reset tutto", key="reset_top", use_container_width=True):
    reset_tutto()

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SEZIONE 1 — INPUT PREZZI
# ──────────────────────────────────────────────

st.markdown('<div class="section-divider">Prezzi</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    acq = st.number_input(
        "Prezzo Acquisto (€)",
        min_value=0.0, step=0.01, format="%.2f",
        value=st.session_state["acq"],
        key="acq",
        placeholder="0.00",
    )
with col2:
    vnd = st.number_input(
        "Prezzo Vendita (€)",
        min_value=0.0, step=0.01, format="%.2f",
        value=st.session_state["vnd"],
        key="vnd",
        placeholder="0.00",
    )

mar_input = st.number_input(
    "Margine % (se vuoi calcolare a ritroso)",
    min_value=0.0, max_value=99.99, step=0.01, format="%.2f",
    value=st.session_state["mar"],
    key="mar",
    placeholder="es. 20.00",
)


# ──────────────────────────────────────────────
# LOGICA CALCOLO — 3 combinazioni
# ──────────────────────────────────────────────

margine_calc  = None
ricarico_calc = None
vendita_calc  = None
acquisto_calc = None
modo          = None

acq_val = st.session_state["acq"]
vnd_val = st.session_state["vnd"]
mar_val = st.session_state["mar"]

# Caso A: Acquisto + Vendita → Margine & Ricarico
if acq_val > 0 and vnd_val > 0 and mar_val == 0:
    modo = "A"
    if vnd_val > 0:
        margine_calc  = (vnd_val - acq_val) / vnd_val * 100
    if acq_val > 0:
        ricarico_calc = (vnd_val - acq_val) / acq_val * 100

# Caso B: Acquisto + Margine % → Vendita
elif acq_val > 0 and mar_val > 0 and vnd_val == 0:
    modo = "B"
    margine_calc  = mar_val
    vendita_calc  = acq_val / (1 - mar_val / 100)
    ricarico_calc = (vendita_calc - acq_val) / acq_val * 100

# Caso C: Vendita + Margine % → Acquisto
elif vnd_val > 0 and mar_val > 0 and acq_val == 0:
    modo = "C"
    margine_calc  = mar_val
    acquisto_calc = vnd_val * (1 - mar_val / 100)
    ricarico_calc = (vnd_val - acquisto_calc) / acquisto_calc * 100 if acquisto_calc > 0 else None

# Caso D: tutti e tre compilati → Acquisto + Vendita (margine input ignorato)
elif acq_val > 0 and vnd_val > 0 and mar_val > 0:
    modo = "A"
    if vnd_val > 0:
        margine_calc  = (vnd_val - acq_val) / vnd_val * 100
    if acq_val > 0:
        ricarico_calc = (vnd_val - acq_val) / acq_val * 100


# ──────────────────────────────────────────────
# RISULTATI PRINCIPALI
# ──────────────────────────────────────────────

if modo is not None:
    st.markdown('<div class="section-divider">Risultati</div>', unsafe_allow_html=True)

    # — Margine —
    if margine_calc is not None:
        col_m = "green" if margine_calc >= 15 else ("orange" if margine_calc >= 10 else "red")
        st.markdown(result_card("Margine %", fmt_pct(margine_calc), "📈", col_m), unsafe_allow_html=True)

    # — Ricarico —
    if ricarico_calc is not None:
        st.markdown(result_card("Ricarico %", fmt_pct(ricarico_calc), "🔁", "blue"), unsafe_allow_html=True)

    # — Vendita calcolata (Caso B) —
    if vendita_calc is not None:
        st.markdown(result_card("Prezzo Vendita calcolato", fmt_eur(vendita_calc), "🏷️", "blue"), unsafe_allow_html=True)

    # — Acquisto calcolato (Caso C) —
    if acquisto_calc is not None:
        st.markdown(result_card("Prezzo Acquisto calcolato", fmt_eur(acquisto_calc), "🛒", "gray"), unsafe_allow_html=True)

    # ── RISORSA / ALERT MARGINE ──
    # Usiamo il prezzo acquisto e vendita effettivi per il calcolo
    acq_eff = acq_val if acq_val > 0 else (acquisto_calc or 0)
    vnd_eff = vnd_val if vnd_val > 0 else (vendita_calc or 0)

    if margine_calc is not None and acq_eff > 0 and vnd_eff > 0:
        SOGLIA = 10.0
        risorsa = (vnd_eff * 0.90) - acq_eff  # negativa = devi abbassare l'acquisto

        if margine_calc < SOGLIA:
            st.markdown(f"""
            <div class="alert-red">
                <div class="alert-red-title">⛔ Margine sotto il 10%!</div>
                <div class="alert-red-body">
                    Il margine attuale è <strong>{fmt_pct(margine_calc)}</strong>.<br>
                    Per raggiungere il 10% con vendita a {fmt_eur(vnd_eff)},
                    il prezzo d'acquisto deve scendere di
                    <strong>{fmt_eur(abs(risorsa))}</strong>
                    fino a <strong>{fmt_eur(vnd_eff * 0.90)}</strong>.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result_card(
                "Risorsa (riduzione acquisto necessaria)",
                fmt_eur(risorsa),
                "⚠️", "red"
            ), unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-green">
                <div class="alert-green-title">✅ Margine OK</div>
                <div class="alert-green-body">
                    Il margine del <strong>{fmt_pct(margine_calc)}</strong> è sopra la soglia del 10%.
                    Operazione sostenibile.
                </div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SEZIONE 2 — SCONTI A CASCATA
# ──────────────────────────────────────────────

st.markdown('<div class="section-divider">Sconti a cascata</div>', unsafe_allow_html=True)

prezzo_base = st.number_input(
    "Prezzo base per lo sconto (€)",
    min_value=0.0, step=0.01, format="%.2f",
    value=0.0,
    placeholder="es. 100.00",
    key="prezzo_sconto_base",
)

sconti_str = st.text_input(
    "Sconti % separati da + (es. 40+10+5)",
    value=st.session_state["sconti_str"],
    key="sconti_str",
    placeholder="40+10+5",
)

sconti_lista = parse_sconti(sconti_str)

if prezzo_base > 0 and sconti_lista:
    netto, sc_totale = applica_sconti(prezzo_base, sconti_lista)
    risparmio = prezzo_base - netto

    st.markdown(result_card("Prezzo Netto dopo sconti", fmt_eur(netto), "🏷️", "blue"), unsafe_allow_html=True)
    st.markdown(result_card("Sconto complessivo %", fmt_pct(sc_totale), "✂️", "orange"), unsafe_allow_html=True)
    st.markdown(result_card("Risparmio totale (€)", fmt_eur(risparmio), "💰", "green"), unsafe_allow_html=True)

    # Dettaglio step by step
    with st.expander("📋 Dettaglio passo per passo"):
        val = prezzo_base
        righe = [f"Prezzo base: **{fmt_eur(val)}**"]
        for i, d in enumerate(sconti_lista, 1):
            val *= (1 - d / 100)
            righe.append(f"Dopo sconto {i} ({d:.2f}%): **{fmt_eur(val)}**")
        righe.append(f"**Sconto totale equivalente: {fmt_pct(sc_totale)}**")
        for r in righe:
            st.markdown(f"• {r}")

elif sconti_str and not sconti_lista:
    st.warning("⚠️ Formato non valido. Usa numeri separati da +, es: `40+10+5`")

elif prezzo_base == 0 and sconti_lista:
    st.info("Inserisci un prezzo base per vedere il netto.")


# ──────────────────────────────────────────────
# RESET BOTTOM
# ──────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄  Reset tutto", key="reset_bottom", use_container_width=True):
    reset_tutto()


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("""
<div class="footer">
    Margini &amp; Sconti · <code>streamlit run app.py</code>
</div>
""", unsafe_allow_html=True)
