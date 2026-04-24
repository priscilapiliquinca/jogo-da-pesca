import streamlit as st
import time

st.set_page_config(page_title="Pesca das Rimas", page_icon="🐟")

# Estilos visuais
st.markdown("""
    <style>
    .stButton>button { background-color: #007bff; color: white; border-radius: 10px; height: 3em; font-size: 20px; }
    .palavra-box { background-color: #e3f2fd; padding: 20px; border-radius: 15px; border: 3px dashed #1e90ff; text-align: center; font-size: 55px; font-weight: bold; color: #0d47a1; }
    .tempo-texto { font-size: 35px !important; color: #ff4b4b; font-weight: bold; text-align: center; }
    .pontos-texto { font-size: 25px; color: #28a745; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

def enviar_rima():
    rima = st.session_state.campo_rima.strip().lower()
    if rima:
        alvo_low = st.session_state.alvo.lower()
        # Lógica de rima: verifica se as últimas 2 letras batem
        if len(rima) > 1 and rima.endswith(alvo_low[-2:]) and rima != alvo_low:
            if rima not in st.session_state.rimas:
                st.session_state.rimas.append(rima)
                st.session_state.pontos += 10
                st.toast(f"✅ {rima.upper()}! +10 pts", icon='🐟')
        st.session_state.campo_rima = ""

if 'fase' not in st.session_state:
    st.session_state.fase = 'selecao'

st.title("🐟 Jogo da Pesca: Rimas")
st.write("### Professoras Priscila e Fabíula")

# LISTA CORRIGIDA: 3 é AMOR
peixes = {
    "1": "Mão", "2": "Escola", "3": "Amor", "4": "Cantar", "5": "Janela",
    "6": "Gato", "7": "Alegria", "8": "Papel", "9": "Dente", "10": "Chuva"
}

if st.session_state.fase == 'selecao':
    st.info("O aluno pescou! Escolha o peixe correspondente:")
    cols = st.columns(2)
    for i, (num, palavra) in enumerate(peixes.items()):
        with cols[i % 2]:
            if st.button(f"Peixe {num}: {palavra}", key=f"btn_{num}"):
                st.session_state.alvo = palavra
                st.session_state.inicio = time.time()
                st.session_state.pontos = 0
                st.session_state.rimas = []
                st.session_state.fase = 'jogo'
                st.rerun()

elif st.session_state.fase == 'jogo':
    st.markdown(f'<div class="palavra-box">{st.session_state.alvo.upper()}</div>', unsafe_allow_html=True)
    
    tempo_total = 90 # 1 minuto e meio
    passado = int(time.time() - st.session_state.inicio)
    tempo_restante = tempo_total - passado
    
    if tempo_restante > 0:
        st.markdown(f'<p class="tempo-texto">⏳ {tempo_restante}s</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="pontos-texto">⭐ Pontos: {st.session_state.pontos}</p>', unsafe_allow_html=True)
        
        # Campo de texto que limpa sozinho
        st.text_input("Digite a rima e dê ENTER:", key="campo_rima", on_change=enviar_rima)
        
        st.write("**Rimas aceitas:**")
        st.info(", ".join(st.session_state.rimas) if st.session_state.rimas else "Aguardando rimas...")
        
        time.sleep(0.5)
        st.rerun()
    else:
        st.balloons()
        st.header(f"⏰ Fim do Tempo!")
        st.success(f"Pontuação: {st.session_state.pontos} pontos.")
        if st.button("Voltar para o Início"):
            st.session_state.fase = 'selecao'
            st.rerun()
