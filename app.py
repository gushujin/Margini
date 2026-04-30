Ruolo: Agisci come uno sviluppatore Python senior esperto in Web App con Streamlit.

Obiettivo: Crea una Web App responsive chiamata "Calcolatrice Business Commerciale". L'app deve essere pronta per il deploy su GitHub e Streamlit Cloud.

Specifiche Tecniche:

Framework: Streamlit.

Stato Iniziale: Tutti i campi di input devono essere vuoti o resettati ad ogni apertura/refresh dell'app.

Interfaccia: Pulita, professionale e mobile-friendly.

Gestione Sconti Multipli: Implementa una funzione che accetti stringhe come "40+10+5". Il programma deve calcolare lo sconto reale composto (es: 40+10+5 = 48.7%) e visualizzare il risultato immediatamente sotto il campo di input.

Logiche di Calcolo (Riferimento foglio MARGINE_RICARICO (OR) di calcolo-margini_2.xlsx):

Margine da Prezzi: Input "Prezzo Acquisto" e "Prezzo Vendita". Calcola il Margine % = ((Vendita - Acquisto) / Vendita) * 100.

Margine da Sconti: Input "Sconto Acquisto %" e "Sconto Vendita %". Calcola il margine lavorando solo sulle percentuali (anche se il listino è vuoto).

Alert Protezione Margine (10%): Se il margine calcolato (in qualsiasi modalità) è inferiore al 10%, mostra un Alert rosso. Calcola automaticamente quanto valore in € è necessario sottrarre al prezzo d'acquisto attuale per ottenere esattamente un margine del 10% (es: acquisto 50€, vendita 53€ -> Margine 5.66% -> Alert -> Valore per abbassare l'acquisto = 2.3€).

Prezzo di Vendita Target: Input "Prezzo Acquisto" e "Margine Desiderato %". Calcola Prezzo Vendita = Acquisto / (1 - (Margine/100)).

Calcolo Sconto Netto: Input "Listino" e "Prezzo Netto". Calcola la percentuale di sconto applicata.

Output Richiesto:

Codice completo per app.py.

Contenuto per il file requirements.txt (es: streamlit).

Usa st.tabs o st.sidebar per organizzare le diverse sezioni di calcolo.
