import streamlit as st

# Configurazione Pagina
st.set_page_config(page_title="Calcolatrice Business", layout="centered")

# Funzione per gestire sconti multipli (es. 40+10+5)
def parse_multiple_discounts(discount_str):
    if not discount_str:
        return 0.0
    try:
        # Pulisce la stringa e divide per il simbolo +
        parts = [float(p.strip()) for p in str(discount_str).split('+') if p.strip()]
        total_complement = 1.0
        for p in parts:
            total_complement *= (1 - p / 100)
        return (1 - total_complement) * 100
    except ValueError:
        return 0.0

# Funzione per mostrare lo sconto calcolato sotto l'input
def display_discount_info(value):
    if value > 0:
        st.caption(f"Sconto reale composto: **{value:.2f}%**")

# Funzione Alert Margine
def check_margin_alert(margin_val, purchase_price):
    if margin_val < 10.0:
        st.error(f"⚠️ Margine insufficiente: {margin_val:.2f}%")
        # Formula: Prezzo Vendita Target = Acquisto / 0.90
        target_price = purchase_price / 0.90
        gap = target_price - (purchase_price / (1 - margin_val/100) if margin_val != 100 else 0)
        needed_euro = target_price - (purchase_price / (1 - margin_val/100)) # Calcolo semplificato per l'utente
        # Valore da aggiungere al prezzo di vendita attuale per arrivare al 10% di margine
        current_sales = purchase_price / (1 - margin_val/100) if margin_val < 100 else 0
        diff = target_price - current_sales
        st.info(f"Per raggiungere il 10% di margine, aggiungi **{diff:.2f}€** al prezzo di vendita attuale.")
    else:
        st.success(f"Margine ottimale: {margin_val:.2f}%")

# UI - Header
st.title("📊 Calcolatrice Business")
st.markdown("Strumento professionale per il calcolo di margini e ricarichi.")

# Creazione Tab per organizzare le funzioni
tab1, tab2, tab3, tab4 = st.tabs([
    "Margine (Prezzi/Sconti)", 
    "Prezzo Vendita Target", 
    "Calcolo Sconto",
    "Info Formule"
])

# --- TAB 1: MARGINE ---
with tab1:
    mode = st.radio("Metodo di calcolo:", ["Valori in €", "Sconti %"])
    
    if mode == "Valori in €":
        col1, col2 = st.columns(2)
        acq = col1.number_input("Prezzo Acquisto (€)", min_value=0.01, step=1.0, value=50.0)
        vend = col2.number_input("Prezzo Vendita (€)", min_value=0.01, step=1.0, value=60.0)
        
        margine = ((vend - acq) / vend) * 100
        st.metric("Margine Finale", f"{margine:.2f}%")
        check_margin_alert(margine, acq)

    else:
        col1, col2 = st.columns(2)
        sconto_acq_raw = col1.text_input("Sconto Acquisto (es. 45 o 40+10)", "45")
        sconto_ven_raw = col2.text_input("Sconto Vendita (es. 30 o 20+5)", "30")
        
        s_acq = parse_multiple_discounts(sconto_acq_raw)
        display_discount_info(s_acq)
        s_ven = parse_multiple_discounts(sconto_ven_raw)
        display_discount_info(s_ven)
        
        # Calcolo margine puro basato su sconti (ipotizzando listino 100)
        prezzo_acq_finto = 100 * (1 - s_acq / 100)
        prezzo_ven_finto = 100 * (1 - s_ven / 100)
        margine = ((prezzo_ven_finto - prezzo_acq_finto) / prezzo_ven_finto) * 100
        
        st.metric("Margine Finale", f"{margine:.2f}%")
        # Per l'alert usiamo un prezzo di acquisto base di 50€ come esempio se il listino è vuoto
        check_margin_alert(margine, 50.0)

# --- TAB 2: PREZZO VENDITA TARGET ---
with tab2:
    col1, col2 = st.columns(2)
    p_acq = col1.number_input("Prezzo Acquisto (€)", min_value=0.01, step=1.0, value=50.0, key="target_acq")
    m_desiderato = col2.number_input("Margine Desiderato (%)", min_value=0.0, max_value=99.0, step=1.0, value=15.0)
    
    target_v = p_acq / (1 - (m_desiderato / 100))
    st.subheader(f"Prezzo di Vendita: **{target_v:.2f}€**")

# --- TAB 3: CALCOLO SCONTO ---
with tab3:
    col1, col2 = st.columns(2)
    listino = col1.number_input("Prezzo Listino (€)", min_value=0.01, step=1.0, value=100.0)
    netto = col2.number_input("Prezzo Netto (€)", min_value=0.01, step=1.0, value=60.0)
    
    sconto_applicato = (1 - (netto / listino)) * 100
    st.metric("Sconto Applicato", f"{sconto_applicato:.2f}%")

# --- TAB 4: INFO ---
with tab4:
    st.markdown("""
    **Formule utilizzate:**
    *   **Margine:** `(Vendita - Acquisto) / Vendita`
    *   **Sconto Composto:** `1 - [(1-s1) * (1-s2) * ...]`
    *   **Prezzo Target:** `Acquisto / (1 - Margine Desiderato)`
    *   **Alert 10%:** Calcolato come differenza tra il prezzo attuale e `Acquisto / 0.90`.
    """)
