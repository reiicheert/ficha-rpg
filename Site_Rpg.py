import streamlit as st
import os
import subprocess
import sys

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="𝕬 𝕮𝖔𝖓𝖛𝖊𝖗𝖌𝖊̂𝖓𝖈𝖎𝖆", layout="wide")


# Função para converter texto para Gótico Negrito uniforme
def to_gothic(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    gothic = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟0123456789"
    trans = str.maketrans(normal, gothic)
    return text.translate(trans)


# Inicializa a lista de status no estado da sessão
if 'lista_status' not in st.session_state:
    st.session_state.lista_status = [to_gothic("Mente"), to_gothic("Corpo"), to_gothic("Social")]


def main():
    # --- TÍTULO CENTRALIZADO ---
    st.markdown(f"<h1 style='text-align: center;'>{to_gothic('A Convergencia')}</h1>", unsafe_allow_html=True)
    st.write("")

    # --- GRID PRINCIPAL ---
    col_perfil, col_inventario, col_stats = st.columns([1.5, 2, 1.2])

    # COLUNA DA ESQUERDA (PERFIL E VIDA)
    with col_perfil:
        st.subheader(to_gothic("Perfil"))
        foto = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if foto:
            st.image(foto, use_container_width=True)

        # --- BARRA DE VIDA ---
        st.write(f"**{to_gothic('Vida')}**")
        col_hp1, col_hp2, col_hp3 = st.columns([1, 1, 1])
        with col_hp1:
            hp_atual = st.number_input(to_gothic("Atual"), value=10, min_value=0, key="hp_at")
        with col_hp2:
            hp_max = st.number_input(to_gothic("Maximo"), value=10, min_value=1, key="hp_mx")
        with col_hp3:
            cor_vida = st.color_picker(to_gothic("Cor"), "#8B0000")

        percentual = min(100, int((hp_atual / hp_max) * 100))

        # REMOVIDA A BORDA AMARELA (border: none)
        st.markdown(f"""
            <div style="width: 100%; background-color: #222; border-radius: 3px; border: none;">
                <div style="width: {percentual}%; background-color: {cor_vida}; height: 20px; border-radius: 2px; transition: width 0.5s;">
                </div>
            </div>
            <p style="text-align: center; font-size: 0.9em; font-family: serif;">{hp_atual} / {hp_max}</p>
        """, unsafe_allow_html=True)

        st.write("")
        st.text_input(to_gothic("Nome do Personagem"))
        st.text_input(to_gothic("Identificacao"))

    # COLUNA CENTRAL (INVENTARIO)
    with col_inventario:
        st.subheader(to_gothic("Inventario"))
        st.text_area(to_gothic("Itens"), placeholder=to_gothic("Lista de itens..."), height=250)
        st.text_area(to_gothic("Equipamentos"), placeholder=to_gothic("Lista de equipamentos..."), height=250)

    # COLUNA DA DIREITA (STATUS E HABILIDADES)
    with col_stats:
        st.subheader(to_gothic("Status"))
        for status in st.session_state.lista_status:
            st.number_input(status, min_value=0, max_value=100, value=0)

        # Adicionador compacto
        c_txt, c_btn = st.columns([3, 1])
        with c_txt:
            novo_status = st.text_input("Novo", label_visibility="collapsed", placeholder=to_gothic("Novo..."))
        with c_btn:
            st.write("")
            if st.button("+"):
                if novo_status:
                    st.session_state.lista_status.append(to_gothic(novo_status))
                    st.rerun()

        st.write("")
        st.subheader(to_gothic("Habilidades"))
        st.text_area("", placeholder=to_gothic("Descreva as habilidades..."), height=250, label_visibility="collapsed")

    # --- ÁREA INFERIOR (NOTAS) ---
    st.write("---")
    st.subheader(to_gothic("Notas"))
    st.text_area("", placeholder=to_gothic("Notas da campanha..."), height=150, label_visibility="collapsed")


# --- LÓGICA PARA EXECUTAR NO PYCHARM ---
if __name__ == "__main__":
    if st.runtime.exists():
        main()
    else:
        script_path = os.path.abspath(__file__)
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])