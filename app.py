import streamlit as st

st.set_page_config(
    page_title="Calcolatrice Commerciale",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:        #0f0f0f;
    --surface:   #1a1a1a;
    --border:    #2e2e2e;
    --accent:    #d4ff00;
    --accent2:   #ff6b35;
    --text:      #f0f0f0;
    --muted:     #888;
    --danger:    #ff3b3b;
    --ok:        #39ff83;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Top bar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.topbar h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0;
    color: var(--text);
}
.topbar .tag {
    background: var(--accent);
    color: #000;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.3rem 0.7rem;
    border-radius: 2px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Section cards */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem 1.75rem 1.75rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    color: var(--text);
}

/* Result boxes */
.result-box {
    background: #111;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
}
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.25rem;
}
.result-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.02em;
    font-family: 'Syne', sans-serif;
}
.result-value.secondary { color: var(--text); font-size: 1.4rem; }
.result-value.positive { color: var(--ok); }
.result-value.warning-val { color: var(--accent2); }
.result-value.danger-val { color: var(--danger); }

/* Alert box */
.alert-box {
    background: rgba(255,59,59,0.08);
    border: 1px solid rgba(255,59,59,0.4);
    border-left: 3px solid var(--danger);
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
}
.alert-title {
    color: var(--danger);
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}
.alert-body {
    color: #f0f0f0;
    font-size: 0.85rem;
    line-height: 1.6;
    font-family: 'DM Mono', monospace;
}

/* Discount preview */
.disc-preview {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    background: rgba(212,255,0,0.07);
    border: 1px solid rgba(212,255,0,0.2);
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    margin-top: 0.2rem;
    display: inline-block;
}

/* Streamlit input overrides */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(212,255,0,0.15) !important;
}
label[data-testid="stWidgetLabel"] {
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: var(--muted) !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 0.5rem !important;
}

/* Reset button */
div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    border-radius: 4px !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(212,255,0,0.05) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Column gap */
[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def parse_sconto(s: str) -> float | None:
    """Parsa uno sconto semplice o concatenato (es. '40+10+5') → float 0-1."""
    if not s or not s.strip():
        return None
    try:
        netto = 100.0
        for parte in s.strip().split("+"):
            v = float(parte.strip())
            if v < 0 or v >= 100:
                return None
            netto *= (1 - v / 100)
        return 1 - netto / 100
    except (ValueError, ZeroDivisionError):
        return None


def fmt_pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def fmt_eur(v: float) -> str:
    return f"€ {v:,.2f}"


def sconto_totale_label(s: str) -> str | None:
    """Restituisce etichetta 'Sconto totale: XX.XX%' se sconto multiplo."""
    if not s or "+" not in s:
        return None
    v = parse_sconto(s)
    if v is None:
        return None
    return f"Sconto totale: {v * 100:.2f}%"


def alert_margine(acquisto: float, vendita: float) -> None:
    """Mostra alert se margine < 10% e calcola il recupero necessario."""
    if vendita <= 0:
        return
    margine = (vendita - acquisto) / vendita
    if margine < 0.10:
        acq_max = vendita * 0.90
        riduzione = acquisto - acq_max
        st.markdown(f"""
        <div class="alert-box">
            <div class="alert-title">⚠ Margine sotto al 10%</div>
            <div class="alert-body">
                Margine attuale: <strong>{margine*100:.2f}%</strong><br>
                Per raggiungere il 10%, il prezzo d'acquisto massimo è <strong>{fmt_eur(acq_max)}</strong><br>
                → Devi ridurre il prezzo d'acquisto di <strong>{fmt_eur(riduzione)}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)


def result_metric(label: str, value: str, cls: str = "") -> None:
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">{label}</div>
        <div class="result-value {cls}">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# ── RESET SESSION STATE ────────────────────────────────────────────────────────

KEYS = [
    "s1_acq", "s1_ven",
    "s2_sc_acq", "s2_sc_ven", "s2_listino",
    "s3_acq", "s3_marg",
    "s4_listino", "s4_netto",
    "s5_sc",
]

def reset_all():
    for k in KEYS:
        if k in st.session_state:
            del st.session_state[k]

# Inizializza valori vuoti alla prima apertura
for k in KEYS:
    if k not in st.session_state:
        st.session_state[k] = None if k.startswith("s") and not k.startswith("s2_sc") and not k.startswith("s5") else ""


# ── TOP BAR ───────────────────────────────────────────────────────────────────

col_title, col_reset = st.columns([5, 1])
with col_title:
    st.markdown("""
    <div class="topbar">
        <h1>🧮 Calcolatrice Commerciale</h1>
        <span class="tag">v1.0</span>
    </div>
    """, unsafe_allow_html=True)
with col_reset:
    st.markdown("<div style='padding-top:1.8rem'>", unsafe_allow_html=True)
    if st.button("⟳ Reset tutti i campi"):
        reset_all()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 Margine da Prezzi €",
    "🏷 Margine da Sconti %",
    "🎯 Prezzo di Vendita",
    "🔖 Calcolo Sconto",
    "🔗 Sconti Multipli",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Margine da Prezzi €
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="section-label">Sezione 01</div>
    <div class="section-title">Calcolo Margine e Ricarico da Prezzi in Euro</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        acq1 = st.number_input("Prezzo di acquisto (€)", min_value=0.0, step=0.01,
                               format="%.2f", key="s1_acq", value=None,
                               placeholder="es. 50.00")
    with c2:
        ven1 = st.number_input("Prezzo di vendita (€)", min_value=0.0, step=0.01,
                               format="%.2f", key="s1_ven", value=None,
                               placeholder="es. 60.00")

    if acq1 is not None and ven1 is not None:
        if ven1 == 0:
            st.error("Il prezzo di vendita non può essere zero.")
        elif acq1 > ven1:
            st.warning("⚠ Il prezzo di acquisto è maggiore del prezzo di vendita.")
        else:
            # Formule: MARGINE = (Ven-Acq)/Ven  |  RICARICO = (Ven/Acq)-1
            margine = (ven1 - acq1) / ven1
            ricarico = (ven1 / acq1 - 1) if acq1 > 0 else 0

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                cls = "ok" if margine >= 0.10 else "danger-val"
                result_metric("Margine %", fmt_pct(margine), cls)
            with col_b:
                result_metric("Ricarico %", fmt_pct(ricarico), "secondary")
            with col_c:
                result_metric("Utile lordo", fmt_eur(ven1 - acq1), "secondary")

            alert_margine(acq1, ven1)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Margine da Sconti %
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-label">Sezione 02</div>
    <div class="section-title">Calcolo Margine e Ricarico da Sconti %</div>
    """, unsafe_allow_html=True)
    st.markdown("<small style='color:#888'>Accetta sconti multipli concatenati, es. <code>40+10+5</code></small>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        sc_acq_raw = st.text_input("Sconto acquisto %", key="s2_sc_acq",
                                   placeholder="es. 45  oppure  40+10")
        lbl = sconto_totale_label(sc_acq_raw)
        if lbl:
            st.markdown(f'<div class="disc-preview">→ {lbl}</div>', unsafe_allow_html=True)

    with c2:
        sc_ven_raw = st.text_input("Sconto vendita %", key="s2_sc_ven",
                                   placeholder="es. 30  oppure  25+5")
        lbl2 = sconto_totale_label(sc_ven_raw)
        if lbl2:
            st.markdown(f'<div class="disc-preview">→ {lbl2}</div>', unsafe_allow_html=True)

    with c3:
        listino2 = st.number_input("Listino (opzionale) €", min_value=0.0, step=0.01,
                                   format="%.2f", key="s2_listino", value=None,
                                   placeholder="facoltativo")

    if sc_acq_raw and sc_ven_raw:
        sc_acq = parse_sconto(sc_acq_raw)
        sc_ven = parse_sconto(sc_ven_raw)

        if sc_acq is None or sc_ven is None:
            st.error("Inserire valori numerici validi (es. 45 oppure 40+10+5).")
        elif (1 - sc_ven) == 0:
            st.error("Sconto vendita del 100%: impossibile calcolare.")
        else:
            # MARGINE DA % = ((1-Sc_Ven)-(1-Sc_Acq))/(1-Sc_Ven)
            # semplificato: (Sc_Acq - Sc_Ven) / (1 - Sc_Ven)
            margine2 = (sc_acq - sc_ven) / (1 - sc_ven)
            ricarico2 = ((1 - sc_ven) / (1 - sc_acq)) - 1 if sc_acq < 1 else 0

            col_a, col_b = st.columns(2)
            with col_a:
                cls = "ok" if margine2 >= 0.10 else "danger-val"
                result_metric("Margine %", fmt_pct(margine2), cls)
            with col_b:
                result_metric("Ricarico %", fmt_pct(ricarico2), "secondary")

            # Se listino fornito, mostra prezzi in €
            if listino2 and listino2 > 0:
                acq_netto = listino2 * (1 - sc_acq)
                ven_netto = listino2 * (1 - sc_ven)
                col_c, col_d = st.columns(2)
                with col_c:
                    result_metric("Netto acquisto", fmt_eur(acq_netto), "secondary")
                with col_d:
                    result_metric("Netto vendita", fmt_eur(ven_netto), "secondary")

            # Alert margine < 10%
            if margine2 < 0.10:
                # Sc_Acq_max tale che margine = 10%:  sc_acq_max = 1 - (1-sc_ven)/0.9
                sc_acq_max = 1 - (1 - sc_ven) / 0.90
                st.markdown(f"""
                <div class="alert-box">
                    <div class="alert-title">⚠ Margine sotto al 10%</div>
                    <div class="alert-body">
                        Margine attuale: <strong>{margine2*100:.2f}%</strong><br>
                        Per raggiungere il 10%, lo sconto acquisto massimo è <strong>{sc_acq_max*100:.2f}%</strong><br>
                        (sconto vendita fisso a {sc_ven*100:.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Prezzo di Vendita da Margine Desiderato
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="section-label">Sezione 03</div>
    <div class="section-title">Calcolo Prezzo di Vendita da Margine Desiderato</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        acq3 = st.number_input("Prezzo di acquisto (€)", min_value=0.0, step=0.01,
                               format="%.2f", key="s3_acq", value=None,
                               placeholder="es. 50.00")
    with c2:
        marg3 = st.number_input("Margine desiderato (%)", min_value=0.0, max_value=99.9,
                                step=0.1, format="%.1f", key="s3_marg", value=None,
                                placeholder="es. 15")

    if acq3 is not None and marg3 is not None:
        if acq3 == 0:
            st.error("Il prezzo di acquisto non può essere zero.")
        elif marg3 >= 100:
            st.error("Il margine non può essere pari o superiore al 100%.")
        else:
            marg3_dec = marg3 / 100
            # Prezzo vendita = Acquisto / (1 - Margine)
            ven3 = acq3 / (1 - marg3_dec)
            ricarico3 = marg3_dec / (1 - marg3_dec)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                result_metric("Prezzo di vendita", fmt_eur(ven3), "positive")
            with col_b:
                result_metric("Ricarico equivalente", fmt_pct(ricarico3), "secondary")
            with col_c:
                result_metric("Utile lordo", fmt_eur(ven3 - acq3), "secondary")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Calcolo Sconto da Listino e Netto
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="section-label">Sezione 04</div>
    <div class="section-title">Calcolo Sconto da Listino e Prezzo Netto</div>
    """, unsafe_allow_html=True)
    st.markdown("<small style='color:#888'>Funziona sia per prezzi di acquisto che di vendita</small>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        listino4 = st.number_input("Prezzo listino (€)", min_value=0.0, step=0.01,
                                   format="%.2f", key="s4_listino", value=None,
                                   placeholder="es. 100.00")
    with c2:
        netto4 = st.number_input("Prezzo netto (€)", min_value=0.0, step=0.01,
                                 format="%.2f", key="s4_netto", value=None,
                                 placeholder="es. 60.00")

    if listino4 is not None and netto4 is not None:
        if listino4 == 0:
            st.error("Il prezzo listino non può essere zero.")
        elif netto4 > listino4:
            st.warning("⚠ Il prezzo netto è maggiore del listino.")
        else:
            # Sconto = 1 - Netto/Listino
            sconto4 = 1 - netto4 / listino4
            risparmio = listino4 - netto4

            col_a, col_b = st.columns(2)
            with col_a:
                result_metric("Sconto applicato %", fmt_pct(sconto4), "positive")
            with col_b:
                result_metric("Risparmio €", fmt_eur(risparmio), "secondary")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Sconti Multipli Concatenati
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class="section-label">Sezione 05</div>
    <div class="section-title">Calcolo Sconti Concatenati (Cascata)</div>
    """, unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#888'>Inserisci gli sconti separati da <code>+</code>, "
        "es. <code>40+10+5</code></small>",
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    sc5_raw = st.text_input("Sconti concatenati", key="s5_sc",
                            placeholder="es.  40+10+5")

    if sc5_raw and sc5_raw.strip():
        parti = [p.strip() for p in sc5_raw.split("+") if p.strip()]
        try:
            valori = [float(p) for p in parti]
            if any(v < 0 or v >= 100 for v in valori):
                st.error("Ogni sconto deve essere tra 0 e 99.")
            else:
                # Calcolo cascata
                netto = 100.0
                steps = []
                for v in valori:
                    netto = netto * (1 - v / 100)
                    steps.append(round(100 - netto, 4))

                sconto_totale = 1 - netto / 100
                netto_finale = netto

                # Steps table
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    result_metric("Sconto totale %", fmt_pct(sconto_totale), "positive")
                with col_b:
                    result_metric("Netto (su base 100)", f"{netto_finale:.4f}", "secondary")
                with col_c:
                    result_metric("N° sconti applicati", str(len(valori)), "secondary")

                # Dettaglio passi
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<div style='font-family:DM Mono,monospace;font-size:0.75rem;color:#888;'>"
                            "DETTAGLIO CALCOLO CASCATA</div>", unsafe_allow_html=True)
                base = 100.0
                rows_html = ""
                for i, v in enumerate(valori):
                    dopo = base * (1 - v / 100)
                    rows_html += (
                        f"<tr>"
                        f"<td style='padding:0.4rem 1rem 0.4rem 0;color:#888'>Sconto {i+1}</td>"
                        f"<td style='padding:0.4rem 1rem;color:#d4ff00'>- {v:.1f}%</td>"
                        f"<td style='padding:0.4rem 1rem;color:#f0f0f0'>→ {dopo:.4f}</td>"
                        f"</tr>"
                    )
                    base = dopo
                st.markdown(
                    f"<table style='border-collapse:collapse;font-family:DM Mono,monospace;"
                    f"font-size:0.8rem;margin-top:0.5rem'>{rows_html}</table>",
                    unsafe_allow_html=True)

        except ValueError:
            st.error("Formato non valido. Usa numeri separati da '+', es. 40+10+5")


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #2e2e2e;padding-top:1rem;display:flex;
justify-content:space-between;align-items:center">
    <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
    color:#555;letter-spacing:0.1em">CALCOLATRICE COMMERCIALE © 2025</span>
    <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#555">
    MARGINE · RICARICO · SCONTI</span>
</div>
""", unsafe_allow_html=True)
