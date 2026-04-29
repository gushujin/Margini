import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Margine Reale", layout="centered")

# CSS per Font Grandi e Mobile UI
st.markdown("""
<style>
    .stNumberInput input { font-size: 20px !important; height: 50px !important; }
    .stTextInput input { font-size: 20px !important; height: 50px !important; }
    .main { background-color: #f8f9fa; }
    .metric-box { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; }
    .res-val { font-size: 24px; font-weight: bold; color: #d32f2f; }
</style>
""", unsafe_allow_html=True)

# Funzioni di calcolo
def parse_cascata(testo, prezzo_lordo):
    if not testo or prezzo_lordo == 0: return prezzo_lordo
    try:
        sconti = [float(x.strip().replace(',', '.')) for x in testo.split('+') if x.strip()]
        netto = prezzo_lordo
        for s in sconti:
            netto *= (1 - s/100)
        return round(netto, 2)
    except:
        return prezzo_lordo

def calc_sconto_equiv(lordo, netto):
    if lordo == 0: return 0
    return round((1 - netto/lordo) * 100, 2)

# --- INIZIO APP ---
st.title("📊 Calcolatore Margine Reale")

# Reset Function
def reset():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

if st.button("🔄 RESET CAMPI"):
    reset()

st.divider()

# --- SEZIONE ACQUISTO ---
st.subheader("🛒 ACQUISTO")
col1, col2 = st.columns([1, 1])
with col1:
    acq_lordo = st.number_input("Prezzo Listino ACQ (€)", min_value=0.0, step=0.01, key="al")
with col2:
    acq_sconti = st.text_input("Sconti (es. 40+10)", key="as")

acq_netto = parse_cascata(acq_sconti, acq_lordo)
sc_acq_tot = calc_sconto_equiv(acq_lordo, acq_netto)
st.info(f"**Netto Acquisto: {acq_netto} €** (Sconto tot: {sc_acq_tot}%)")

st.divider()

# --- SEZIONE VENDITA ---
st.subheader("🏷️ VENDITA")
col3, col4 = st.columns([1, 1])
with col3:
    ven_lordo = st.number_input("Prezzo Listino VEN (€)", min_value=0.0, step=0.01, key="vl")
with col4:
    ven_sconti = st.text_input("Sconti (es. 5+2)", key="vs")

ven_netto = parse_cascata(ven_sconti, ven_lordo)
sc_ven_tot = calc_sconto_equiv(ven_lordo, ven_netto)
st.info(f"**Netto Vendita: {ven_netto} €** (Sconto tot: {sc_ven_tot}%)")

st.divider()

# --- RISULTATI E MARGINE ---
if ven_netto > 0:
    margine_reale = round(((ven_netto - acq_netto) / ven_netto) * 100, 2)
    
    st.subheader("📈 RISULTATO")
    
    # Colore in base al margine
    color = "green" if margine_reale >= 10 else "red"
    st.markdown(f"<div style='font-size:30px; color:{color}; font-weight:bold;'>Margine: {margine_reale}%</div>", unsafe_allow_html=True)

    if margine_reale < 10:
        # Calcolo Risorsa
        acq_max_per_10pct = ven_netto * 0.90
        risorsa = acq_max_per_10pct - acq_netto
        
        st.error(f"⚠️ MARGINE INSUFFICIENTE (Sotto 10%)")
        st.markdown(f"""
        <div class='metric-box'>
            <p>Per raggiungere il margine del 10%:</p>
            <p>Il prezzo d'acquisto netto deve scendere di:</p>
            <div class='res-val'>{round(risorsa, 2)} €</div>
            <p><small>(Acquisto netto obiettivo: {round(acq_max_per_10pct, 2)} €)</small></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Margine Target Rispettato")

st.divider()
if st.button("🔄 RESET CAMPI (Fine pagina)"):
    reset()
