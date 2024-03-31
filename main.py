import streamlit as st
import json
from streamlit_extras.stoggle import stoggle

def run():
    st.set_page_config(
        page_title="Quizz Programa Nacional de Reformas",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# CSS personalizado para os botões
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
</style>
""", unsafe_allow_html=True)

# Inicializa as variáveis da sessão se elas não existirem
valores_default = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False, 'quiz_finalizado': False}
for key, value in valores_default.items():
    st.session_state.setdefault(key, value)

# Carrega os dados do quiz
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    dados_quiz = json.load(f)

def reiniciar_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False
    st.session_state.quiz_finalizado = False

def submeter_resposta():
    # Verifica se uma opção foi selecionada
    if st.session_state.selected_option is not None:
        # Marca a resposta como submetida
        st.session_state.answer_submitted = True
        # Verifica se a opção selecionada está correta
        if st.session_state.selected_option == dados_quiz[st.session_state.current_index]['answer']:
            st.session_state.score += 10
    else:
        # Se nenhuma opção foi selecionada, mostra uma mensagem e não marca como submetida
        st.warning("Selecione uma opção antes de submeter.")

def proxima_pergunta():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# Título e descrição
st.subheader("Quizz Programa Nacional de Reformas")


if not st.session_state.quiz_finalizado:
    # Barra de progresso
    valor_barra_progresso = (st.session_state.current_index + 1) / len(dados_quiz)
    numero_pergunta_atual = st.session_state.current_index + 1
    st.write(f"Pergunta {numero_pergunta_atual} de {len(dados_quiz)}")
    st.progress(valor_barra_progresso)


    # Exibe a pergunta e as opções de resposta
    item_pergunta = dados_quiz[st.session_state.current_index]
    st.subheader(f"{item_pergunta['question']}")

    stoggle(
    "Pista",
    f"""{dados_quiz[st.session_state.current_index]['hint']}""",
)

    st.markdown(""" ___""")

    # Seleção de resposta
    opcoes = item_pergunta['options']
    resposta_correta = item_pergunta['answer']

if st.session_state.answer_submitted:
    # Define a mensagem e a cor do fundo com base na corretude da resposta
    if st.session_state.selected_option == dados_quiz[st.session_state.current_index]['answer']:
        mensagem = "Correto!"
        cor_fundo = "#D4EDDA"  # Uma cor de fundo suave para resposta correta, por exemplo, verde claro
    else:
        mensagem = "Incorreto"
        cor_fundo = "#f0f2f6"  # Uma cor de fundo suave para resposta incorreta, por exemplo, vermelho claro

    # Renderiza o feedback com as    variáveis definidas acima
    st.markdown(f"""
    <div style="background-color: {cor_fundo}; border-radius: 10px; padding: 20px; text-align: center;">
        <h3>{mensagem}</h3>
        <p>{item_pergunta['explanation']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(""" ___""")
    st.image(dados_quiz[st.session_state.current_index]['image_path'], use_column_width=True)
else:
    # Renderiza os botões para seleção de opção
    for i, opcao in enumerate(opcoes):
        if st.button(opcao, key=i, use_container_width=True):
            st.session_state.selected_option = opcao

st.markdown(""" ___""")


# Botão de submissão e lógica de resposta
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(dados_quiz) - 1:
        st.button('Próxima', on_click=proxima_pergunta)
    else:
        # Atualiza o estado para finalizado
        st.session_state.quiz_finalizado = True

        # Cria um bloco de Markdown para exibir a pontuação com estilo
        st.markdown(f"""
        <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; text-align: center;">
            <h1>Quiz Concluído!</h1>
            <h2>Sua pontuação é: <span style="color: #333;">{st.session_state.score} / {len(dados_quiz) * 10}</span></h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(""" ___""")

        # Botão de reiniciar
        if st.button('Reiniciar', on_click=reiniciar_quiz):
            pass

else:
    if st.session_state.current_index < len(dados_quiz):
        st.button('Submeter', on_click=submeter_resposta)
