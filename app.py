import streamlit as st
import pandas as pd

# Caricamento configurazione da Excel
def load_config():
    try:
        df = pd.read_excel('config_v1.xlsx')
        return dict(zip(df['Parametro'], df['Valore']))
    except Exception as e:
        return {
            'colore_sfondo': '#2a2a2a',
            'colore_input_focus': '#d3d3d3',
            'colore_testo': '#ffffff',
            'font_family': 'sans-serif',
            'font_size_etichette': '14px',
            'colore_alert': '#ff4b4b'
        }

config = load_config()

st.set_page_config(page_title="Business Calculator", layout="wide")

# CSS Custom per stile Responsive e Interazioni
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config['colore_sfondo']};
        color: {config['colore_testo']};
        font-family: {config['font_family']};
    }}
    /* Stile etichette sopra input */
    label p {{
        font-size: {config['font_size_etichette']} !important;
        font-weight: bold;
        color: {config['colore_testo']} !important;
    }}
    /* Effetto Focus sugli input */
    .stTextInput input:focus {{
        background-color: {config['colore_input_focus']} !important;
        color: black !important;
        border: 2px solid white;
    }}
    /* Container per i campi input */
    .stTextInput input {{
        max-width: 250px;
    }}
    .alert-box {{
        padding: 15px;
        background-color: {config['colore_alert']};
        color: white;
        border-radius: 8px;
        margin-top: 10px;
        font-weight: bold;
        border: 1px solid white;
    }}
    </style>
    """, unsafe_allow_html=True)

def parse_multiple_discounts(discount_str):
    if not discount_str:
        return 0.0
    try:
        # Gestione sconti multipli (es: 40+10+5)
        parts = str(discount_str).replace(',', '.').split('+')
        net_factor = 1.0
        for p in parts:
            if p.strip():
                net_factor *= (1 - float(p.strip()) / 100)
        return (1 - net_factor) * 100
    except:
        return 0.0

# Inizializzazione Session State per Reset Campi
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_fields():
    st.session_state.reset_key += 1

st.title("📊 Business Commercial Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📦 Acquisto")
    
    # Prezzo di Listino
    c1, b1 = st.columns([0.8, 0.2])
    listino_val = c1.text_input("Listino (€)", key=f"list_{st.session_state.reset_key}")
    if b1.button("❌", key="b1"): reset_fields(); st.rerun()
    
    # Sconto Acquisto
    c2, b2 = st.columns([0.8, 0.2])
    sconto_acq_raw = c2.text_input("Sconto Acq. (es. 40+10)", key=f"sacq_{st.session_state.reset_key}")
    if b2.button("❌", key="b2"): reset_fields(); st.rerun()
    
    # Prezzo Acquisto Diretto (se non si ha listino)
    c3, b3 = st.columns([0.8, 0.2])
    prezzo_acq_input = c3.text_input("Prezzo Acquisto Diretto (€)", key=f"pacq_{st.session_state.reset_key}")
    if b3.button("❌", key="b3"): reset_fields(); st.rerun()

    # Logica Calcolo Costo Effettivo
    val_listino = float(listino_val.replace(',', '.')) if listino_val else 0.0
    sconto_acq_perc = parse_multiple_discounts(sconto_acq_raw)
    
    if val_listino > 0:
        costo_effettivo = val_listino * (1 - sconto_acq_perc / 100)
    else:
        costo_effettivo = float(prezzo_acq_input.replace(',', '.')) if prezzo_acq_input else 0.0
    
    if sconto_acq_raw:
        st.caption(f"Sconto totale applicato: {sconto_acq_perc:.2f}%")
    st.metric("Costo Netto Reale", f"{costo_effettivo:,.2f} €")

with col2:
    st.subheader("🏷️ Vendita")
    
    c4, b4 = st.columns([0.8, 0.2])
    prezzo_vendita_raw = c4.text_input("Prezzo Vendita (€)", key=f"pvend_{st.session_state.reset_key}")
    if b4.button("❌", key="b4"): reset_fields(); st.rerun()

    c5, b5 = st.columns([0.8, 0.2])
    sconto_vendita_raw = c5.text_input("Sconto Vendita (%)", key=f"svend_{st.session_state.reset_key}")
    if b5.button("❌", key="b5"): reset_fields(); st.rerun()
    
    c6, b6 = st.columns([0.8, 0.2])
    margine_target = c6.text_input("Margine Desiderato (%)", key=f"mtarg_{st.session_state.reset_key}")
    if b6.button("❌", key="b6"): reset_fields(); st.rerun()

    val_vendita_lordo = float(prezzo_vendita_raw.replace(',', '.')) if prezzo_vendita_raw else 0.0
    sconto_vend_perc = parse_multiple_discounts(sconto_vendita_raw)
    prezzo_vendita_netto = val_vendita_lordo * (1 - sconto_vend_perc / 100)
    
    if sconto_vendita_raw:
        st.caption(f"Sconto vendita tot: {sconto_vend_perc:.2f}%")
    st.metric("Vendita Netta", f"{prezzo_vendita_netto:,.2f} €")

with col3:
    st.subheader("📈 Analisi")
    
    if prezzo_vendita_netto > 0 and costo_effettivo > 0:
        # Formule Commerciali
        margine = ((prezzo_vendita_netto - costo_effettivo) / prezzo_vendita_netto) * 100
        ricarico = ((prezzo_vendita_netto - costo_effettivo) / costo_effettivo) * 100
        utile = prezzo_vendita_netto - costo_effettivo
        
        st.write(f"**Margine:** {margine:.2f}%")
        st.write(f"**Ricarico:** {ricarico:.2f}%")
        st.write(f"**Utile Netto:** {utile:,.2f} €")
        
        # Gestione Alert Margine < 10%
        if margine < 10.0:
            # Calcolo riduzione acquisto per arrivare al 10% di margine
            # Formula: (Vendita - (Costo - Riduzione)) / Vendita = 0.10
            # Riduzione = Costo - (Vendita * 0.90)
            target_acq = prezzo_vendita_netto * 0.90
            risorsa_necessaria = costo_effettivo - target_acq
            
            st.markdown(f"""
                <div class="alert-box">
                    ⚠️ ALERT MARGINE BASSO ({margine:.2f}%)<br>
                    Per raggiungere il 10% di margine minimo:<br>
                    Abbassare il prezzo d'acquisto di: <b>{risorsa_necessaria:,.2f} €</b>
                </div>
            """, unsafe_allow_html=True)

    # Calcolo PV da Margine Desiderato
    if margine_target and costo_effettivo > 0:
        mt = float(margine_target.replace(',', '.')) / 100
        if mt < 1:
            pv_richiesto = costo_effettivo / (1 - mt)
            st.success(f"Per un margine del {margine_target}%, vendi a: {pv_richiesto:,.2f} €")

st.divider()
st.info("Nota: L'app è responsive e i colori sono configurabili dal file Excel allegato.")
