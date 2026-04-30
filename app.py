import streamlit as st

# Configurazione della pagina per essere responsive
st.set_page_config(page_title="Calcolatrice Business", layout="centered")

# Funzione per calcolare sconti multipli (es. 40+10+5)
def parse_multi_discount(discount_str):
    if not discount_str:
        return 0.0
    try:
        # Divide la stringa per '+' e calcola il valore composto
        parts = [float(p.strip().replace(',', '.')) for p in str(discount_str).split('+') if p.strip()]
        total_complement = 1.0
        for p in parts:
            total_complement *= (1 - p / 100)
        return (1 - total_complement) * 100
    except Exception:
        return None

# Funzione per calcolare la risorsa necessaria per raggiungere il 10% di margine
def calculate_resource_gap(purchase_price, current_sale_price):
    # Per avere il 10% di margine: (Vendita - X) / Vendita = 0.10
    # X (nuovo acquisto) = Vendita * 0.90
    target_purchase = current_sale_price * 0.90
    gap = purchase_price - target_purchase
    return gap if gap > 0 else 0.0

# Reset automatico dei campi: inizializziamo lo stato della sessione
if 'reset' not in st.session_state:
    st.session_state.reset = False

st.title("📊 Calcolatrice Business Commerciale")
st.markdown("---")

# Organizzazione in Tab
tab1, tab2, tab3 = st.tabs(["💰 Calcolo Margini", "🎯 Target Vendita", "🏷️ Calcolo Sconto Netto"])

# --- TAB 1: CALCOLO MARGINI ---
with tab1:
    st.subheader("Calcola il Margine Operativo")
    mode = st.radio("Metodo di calcolo:", ["Prezzi (€)", "Sconti (%)"], horizontal=True)
    
    if mode == "Prezzi (€)":
        col1, col2 = st.columns(2)
        p_acq = col1.number_input("Prezzo Acquisto (€)", min_value=0.0, step=0.01, value=0.0)
        p_vend = col2.number_input("Prezzo Vendita (€)", min_value=0.0, step=0.01, value=0.0)
        
        if p_vend > 0:
            margine = ((p_vend - p_acq) / p_vend) * 100
            st.metric("Margine", f"{margine:.2f}%")
            
            if margine < 10.0:
                gap = calculate_resource_gap(p_acq, p_vend)
                st.error(f"⚠️ Alert: Margine inferiore al 10%!")
                st.info(f"Risorsa necessaria (abbassare prezzo acquisto): **{gap:.2f}€**")
            else:
                st.success("Margine di sicurezza garantito (>10%).")

    else:
        col1, col2 = st.columns(2)
        s_acq_raw = col1.text_input("Sconto Acquisto % (es: 45 o 40+10)", key="sacq")
        s_ven_raw = col2.text_input("Sconto Vendita % (es: 30)", key="sven")
        
        val_acq = parse_multi_discount(s_acq_raw)
        val_ven = parse_multi_discount(s_ven_raw)
        
        if val_acq is not None: col1.caption(f"Sconto reale Acq: **{val_acq:.2f}%**")
        if val_ven is not None: col2.caption(f"Sconto reale Ven: **{val_ven:.2f}%**")
        
        if val_acq is not None and val_ven is not None:
            # Calcolo margine puro su basi percentuali (Listino ipotetico = 100)
            net_acq = 100 * (1 - val_acq / 100)
            net_ven = 100 * (1 - val_ven / 100)
            margine_sconto = ((net_ven - net_acq) / net_ven) * 100
            st.metric("Margine da Sconti", f"{margine_sconto:.2f}%")
            
            if margine_sconto < 10.0:
                # Esempio su base 100 per l'abbattimento acquisto
                gap_perc = calculate_resource_gap(net_acq, net_ven)
                st.error("⚠️ Alert: Margine da sconti troppo basso!")
                st.info(f"Valore da abbattere sul netto acquisto (base 100€): **{gap_perc:.2f}€**")

# --- TAB 2: PREZZO DI VENDITA TARGET ---
with tab2:
    st.subheader("Calcola Prezzo di Vendita Necessario")
    colA, colB = st.columns(2)
    acq_base = colA.number_input("Costo Acquisto (€)", min_value=0.0, step=0.01, key="acq_target")
    margine_req = colB.number_input("Margine Desiderato (%)", min_value=0.0, max_value=99.0, step=0.1, key="m_req")
    
    if margine_req < 100:
        prezzo_target = acq_base / (1 - (margine_req / 100))
        st.subheader(f"Prezzo di vendita consigliato: **{prezzo_target:.2f}€**")

# --- TAB 3: CALCOLO SCONTO NETTO ---
with tab3:
    st.subheader("Calcola Sconto applicato")
    colL, colN = st.columns(2)
    listino = colL.number_input("Prezzo di Listino (€)", min_value=0.0, step=0.01)
    netto = colN.number_input("Prezzo Netto (€)", min_value=0.0, step=0.01)
    
    if listino > 0:
        sconto_effettivo = (1 - (netto / listino)) * 100
        st.metric("Sconto Applicato", f"{sconto_effettivo:.2f}%")

# Footer per info
st.sidebar.title("Opzioni")
if st.sidebar.button("Reset Campi"):
    st.rerun()
st.sidebar.info("Calcolatrice basata sul foglio MARGINE_RICARICO (OR).")
