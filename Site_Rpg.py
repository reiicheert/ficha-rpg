import streamlit as st
import os, subprocess, sys, json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="𝕬 𝕮𝖔𝖓𝖛𝖊𝖗𝖌𝖊̂𝖓𝖈𝖎𝖆", layout="wide")


def to_gothic(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    gothic = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟0123456789"
    return text.translate(str.maketrans(normal, gothic))


# --- INICIALIZAÇÃO DE VARIÁVEIS NO ESTADO DA SESSÃO ---
# Chaves que serão salvas no arquivo TXT
DATA_KEYS = ["hp_at", "hp_mx", "nome_v", "ident_v", "equip_v", "itens_v", "notas_v",
             "s_Corpo", "s_Vontade", "s_Social", "s_Mente", "ativas", "passivas", "cp_v"]

if 'ativas' not in st.session_state: st.session_state.ativas = []
if 'passivas' not in st.session_state: st.session_state.passivas = []

for k in DATA_KEYS:
    if k not in st.session_state:
        if "s_" in k:
            st.session_state[k] = 0
        elif "hp" in k:
            st.session_state[k] = 10
        elif k == "cp_v":
            st.session_state[k] = "#8B0000"
        else:
            st.session_state[k] = ""

# --- LÓGICA DE CARREGAMENTO (SIDEBAR) ---
with st.sidebar:
    st.subheader(to_gothic("Arquivos"))
    up_file = st.file_uploader(to_gothic("Carregar Ficha .txt"), type="txt")
    if up_file:
        try:
            d = json.load(up_file)
            if st.button(to_gothic("Confirmar Carregamento")):
                for k in DATA_KEYS:
                    if k in d: st.session_state[k] = d[k]
                st.rerun()
        except:
            st.error("Erro ao ler arquivo.")

# --- JAVASCRIPT AVISO DE SAÍDA ---
st.components.v1.html("""<script>window.onbeforeunload = function() { return "Ja salvou?"; };</script>""", height=0)

# --- CSS PARA ESTILIZAÇÃO ---
st.markdown("""
    <style>
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"],
    div[data-testid="stNumberInput"] button { display: none !important; }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important; height: 55px !important;
    }
    div[data-testid="stNumberInput"] input {
        color: transparent !important; -webkit-text-fill-color: transparent !important;
        text-align: center !important; height: 55px !important; font-size: 22px;
    }
    .bar-container {
        position: relative; width: 100%; height: 55px; margin-bottom: -55px;
        display: flex; align-items: center; justify-content: center;
        pointer-events: none; z-index: 5;
    }
    .inner-text { color: #d0d0d0; font-size: 18px; font-weight: bold; }
    div[data-testid="stColorPicker"] { display: flex; justify-content: center; align-items: center; height: 70px; padding-left: 11px; }
    button[key^="r_"] { background-color: rgba(255, 0, 0, 0.15) !important; color: white !important; border: 1px solid red !important; height: 40px !important; margin-top: 5px !important;}
    </style>
    """, unsafe_allow_html=True)


def draw_dice(color, value):
    return f"""<div style="display:flex;justify-content:center;align-items:center;margin-top:10px;margin-bottom:20px;">
    <svg viewBox="0 0 100 100" width="100" height="100">
    <path d="M50 5 L95 28 L95 72 L50 95 L5 72 L5 28 Z" fill="{color}" stroke="black" stroke-width="3"/>
    <path d="M50 5 L50 95 M5 28 L95 28 M5 72 L95 72 M50 5 L95 72 M50 5 L5 72 M5 28 L50 95 M95 28 L50 95" stroke="black" stroke-width="1" fill="none"/>
    <circle cx="22" cy="50" r="3" fill="#FFD700"/><circle cx="78" cy="50" r="3" fill="#FFD700"/>
    <text x="50" y="62" font-family="Arial" font-size="34" font-weight="900" fill="black" text-anchor="middle">{value}</text></svg></div>"""


def main():
    st.markdown(f"<h1 style='text-align: center;'>{to_gothic('A Convergencia')}</h1>", unsafe_allow_html=True)
    col_p, col_i, col_s = st.columns([1.5, 2.5, 1.3])

    # --- COLUNA PERFIL ---
    with col_p:
        st.subheader(to_gothic("Perfil"))
        # FOTO DO PERSONAGEM (Corrigido: st.image logo abaixo do uploader)
        f_char = st.file_uploader("Upload Personagem", type=["jpg", "png", "jpeg"], key="uploader_char",
                                  label_visibility="collapsed")
        if f_char: st.image(f_char, use_container_width=True)

        st.write(to_gothic("Vida"))
        v1, v2, v3 = st.columns([2, 1, 2])
        with v1:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Atual")}</span></div>',
                        unsafe_allow_html=True)
            cur = st.number_input("", 0, 999, key="hp_at", label_visibility="collapsed")
        with v2: cv = st.color_picker("", key="cp_v", label_visibility="collapsed")
        with v3:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Maxima")}</span></div>',
                        unsafe_allow_html=True)
            mx = st.number_input("", 0, 999, key="hp_mx", label_visibility="collapsed")

        p = (min(100, int((cur / mx) * 100)) if mx > 0 else 0)
        st.markdown(
            f'<div style="width:100%; background:#222; height:12px; margin-top:10px;"><div style="width:{p}%; background:{cv}; height:100%;"></div></div>',
            unsafe_allow_html=True)
        st.write(f"<p style='text-align:center; color:white; font-weight:bold;'>{cur} / {mx}</p>",
                 unsafe_allow_html=True)
        st.text_input(to_gothic("Nome"), key="nome_v")
        st.text_input(to_gothic("Identificacao"), key="ident_v")

    # --- COLUNA INVENTARIO ---
    with col_i:
        st.subheader(to_gothic("Equipamentos"))
        e1, e2 = st.columns([1, 2])
        with e1:
            st.write(f"<p style='font-size:12px;'>{to_gothic('Foto Arma')}</p>", unsafe_allow_html=True)
            f_w = st.file_uploader("Upload Arma", type=["jpg", "png", "jpeg"], key="uploader_weapon",
                                   label_visibility="collapsed")
            if f_w: st.image(f_w, use_container_width=True)
        with e2: st.text_area("E", height=250, key="equip_v", label_visibility="collapsed")
        st.write("---")
        st.subheader(to_gothic("Itens"))
        st.text_area("M", height=250, key="itens_v", label_visibility="collapsed")

    # --- COLUNA STATUS ---
    with col_s:
        st.subheader(to_gothic("Status"))
        # MATRIZ 2X2
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Corpo")}</span></div>',
                        unsafe_allow_html=True)
            val_c = st.number_input("", -99, 99, key="s_Corpo", label_visibility="collapsed")
            st.markdown(draw_dice("#FF4B4B", val_c), unsafe_allow_html=True)
        with r1c2:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Vontade")}</span></div>',
                        unsafe_allow_html=True)
            val_v = st.number_input("", -99, 99, key="s_Vontade", label_visibility="collapsed")
            st.markdown(draw_dice("#28A745", val_v), unsafe_allow_html=True)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Social")}</span></div>',
                        unsafe_allow_html=True)
            val_s = st.number_input("", -99, 99, key="s_Social", label_visibility="collapsed")
            st.markdown(draw_dice("#FFD700", val_s), unsafe_allow_html=True)
        with r2c2:
            st.markdown(f'<div class="bar-container"><span class="inner-text">{to_gothic("Mente")}</span></div>',
                        unsafe_allow_html=True)
            val_m = st.number_input("", -99, 99, key="s_Mente", label_visibility="collapsed")
            st.markdown(draw_dice("#A88BE2", val_m), unsafe_allow_html=True)

        st.write("---")
        st.subheader(to_gothic("Habilidades"))
        # ATIVAS
        st.write(f"**{to_gothic('Ativas')}**")
        ca1, ca2 = st.columns([4, 1])
        with ca1:
            n_at = st.text_input("n1", placeholder="Nome...", key="in_at", label_visibility="collapsed")
        with ca2:
            if st.button("+", key="b_at"):
                if n_at: st.session_state.ativas.append({"n": n_at, "d": ""}); st.rerun()
        for idx, at in enumerate(st.session_state.ativas):
            c_e, c_r = st.columns([5, 1])
            with c_e:
                with st.expander(to_gothic(at['n'])): at['d'] = st.text_area("d", value=at['d'], key=f"dat_{idx}",
                                                                             label_visibility="collapsed")
            with c_r:
                if st.button("X", key=f"r_at_{idx}"): st.session_state.ativas.pop(idx); st.rerun()

        # PASSIVAS
        st.write(f"**{to_gothic('Passivas')}**")
        cp1, cp2 = st.columns([4, 1])
        with cp1:
            n_ps = st.text_input("n2", placeholder="Nome...", key="in_ps", label_visibility="collapsed")
        with cp2:
            if st.button("+", key="b_ps"):
                if n_ps: st.session_state.passivas.append({"n": n_ps, "d": ""}); st.rerun()
        for idx, ps in enumerate(st.session_state.passivas):
            c_e, c_r = st.columns([5, 1])
            with c_e:
                with st.expander(to_gothic(ps['n'])): ps['d'] = st.text_area("d", value=ps['d'], key=f"dps_{idx}",
                                                                             label_visibility="collapsed")
            with c_r:
                if st.button("X", key=f"r_ps_{idx}"): st.session_state.passivas.pop(idx); st.rerun()

    st.write("---")
    st.subheader(to_gothic("Notas"))
    st.text_area("N", key="notas_v", height=100, label_visibility="collapsed")

    # DOWNLOAD (Ficha em Bloco de Notas)
    data_save = {k: st.session_state[k] for k in DATA_KEYS}
    st.download_button("💾 " + to_gothic("Baixar .txt"), json.dumps(data_save, indent=4, ensure_ascii=False),
                       file_name="ficha.txt")


if __name__ == "__main__":
    if st.runtime.exists():
        main()
    else:
        script_path = os.path.abspath(__file__);
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
