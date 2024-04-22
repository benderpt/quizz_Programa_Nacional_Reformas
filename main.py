import streamlit as st
import json
from streamlit_extras.stoggle import stoggle
import os

def run():
    st.set_page_config(
        page_title="Quizz Programa Nacional de Reformas",
        page_icon="🇪🇺",
    )

if __name__ == "__main__":
    run()

# CSS personalizado para os botões
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
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

st.markdown('<h1 style="color: #0e2a49; text-align: center;">Programa Nacional de Reformas</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color: #0e2a49; text-align: center;">Quizz</h2>', unsafe_allow_html=True)



if not st.session_state.quiz_finalizado:
    # Barra de progresso
    valor_barra_progresso = (st.session_state.current_index + 1) / len(dados_quiz)
    numero_pergunta_atual = st.session_state.current_index + 1
    st.write(f"Pergunta {numero_pergunta_atual} de {len(dados_quiz)}")
    st.progress(valor_barra_progresso)


    # Exibe a pergunta e as opções de resposta
    item_pergunta = dados_quiz[st.session_state.current_index]
    st.subheader(f"{item_pergunta['question']}")

    # Seleção de resposta
    opcoes = item_pergunta['options']
    resposta_correta = item_pergunta['answer']

if st.session_state.answer_submitted:
    # Define a mensagem e a cor do fundo com base na corretude da resposta
    if st.session_state.answer_submitted:
        # Assume que dados_quiz e item_pergunta estão definidos anteriormente no código
        item_pergunta = dados_quiz[st.session_state.current_index]
        caminho_imagem = item_pergunta.get('image_path',  '')
        caminho_caption = item_pergunta.get('caption')

        # Define a mensagem e a cor do fundo com base na corretude da resposta
        if st.session_state.selected_option == item_pergunta['answer']:
            mensagem = "Correto!"
            cor_borda = "#3CB371"  # Uma cor de fundo suave para resposta correta, por exemplo, verde claro
        else:
            mensagem = f"Errado. A resposta certa é {item_pergunta['answer']}"
            cor_borda = "#FFCDD2"  # Uma cor de fundo suave para resposta incorreta, por exemplo, vermelho claro

        # Renderiza o feedback
        st.markdown(f"""
        <div style="border: 10px solid {cor_borda}; border-radius: 10px; padding: 20px; text-align: center;">
            <h3>{mensagem}</h3>
            <p>{item_pergunta['explanation']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Verifica se o caminho da imagem existe e, se sim, mostra a imagem
        if caminho_imagem and os.path.isfile(caminho_imagem):
            st.markdown("___")
            st.image(caminho_imagem, caption=caminho_caption, use_column_width=True)

else:
    stoggle(
            "🔎 Pista",
            f"""{dados_quiz[st.session_state.current_index]['hint']}""",
        )
    st.markdown(""" ___""")
    # Renderiza os botões para seleção de opção
    for i, opcao in enumerate(opcoes):
        
        if st.button(opcao, key=i, use_container_width=True):
            st.session_state.selected_option = opcao
        

st.markdown(""" ___""")


# Função que atualiza o estado para mostrar o resultado
def mostrar_resultado():
    st.session_state.mostrar_resultado = True

# Botão de submissão e lógica de resposta
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(dados_quiz) - 1:
        st.button('Próxima', on_click=proxima_pergunta)
    else:
        # Se o quiz terminou, mas o resultado ainda não foi pedido para ser mostrado
        if not st.session_state.get('quiz_finalizado', False):
            # Botão que altera o estado para mostrar o resultado quando clicado
            if st.button('Mostrar Resultado', on_click=mostrar_resultado):
                # Atualiza o estado para finalizado
                st.session_state.quiz_finalizado = True

        # Se o resultado deve ser mostrado
        if st.session_state.get('mostrar_resultado', False):
            # Cria um bloco de Markdown para exibir a pontuação com estilo
            st.markdown(f"""
            <div style="border: 10px solid #78909C; border-radius: 10px; padding: 20px; text-align: center;">
                <h1>🥳 Quiz Concluído! 🥳</h1>
                <h4>Obteve {st.session_state.score} pontos em {len(dados_quiz) * 10} pontos possíveis</h4>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(""" ___""")

            # Botão de reiniciar
            if st.button('Reiniciar', on_click=reiniciar_quiz):
                pass

else:
    if st.session_state.current_index < len(dados_quiz):
        st.button('Submeter', on_click=submeter_resposta)
