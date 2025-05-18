import streamlit as st
import re

def load_messages(filename="messages.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    messages = content.split('---')
    
    projects = []
    for message in messages:
        if not message.strip():
            continue
        
        nome_match = re.search(r'Nome: (.*?)(?:\n|$)', message)
        votos_match = re.search(r'Votos: (\d+)', message)
        link_match = re.search(r'Link: (.*?)(?:\n|$)', message)
        desc_match = re.search(r'Descrição: (.*?)(?:\n|$)', message, re.DOTALL)
        user_match = re.search(r'Usuário: (.*?)(?:\n|$)', message)
        
        if nome_match and votos_match and link_match:
            projects.append({
                'nome': nome_match.group(1).strip(),
                'votos': int(votos_match.group(1)),
                'link': link_match.group(1).strip(),
                'descricao': desc_match.group(1).strip() if desc_match else '',
                'usuario': user_match.group(1).strip() if user_match else ''
            })
    
    return projects
  
def truncar_nome(nome, limite=24):
    partes = nome.split()
    resultado = ''
    for parte in partes:
        if len(resultado + ' ' + parte) <= limite:
            resultado += (' ' + parte if resultado else parte)
        else:
            break
    return resultado

# Define o diálogo uma única vez
@st.dialog("Detalhes do Projeto")
def show_details():
    project = st.session_state.selected_project
    st.markdown(f"### {project['nome']}")
    st.markdown(f"**Usuário Discord:** {project['usuario']}")
    st.markdown(f"**Descrição:** {project['descricao']}")
    st.markdown(f"[Abrir no GitHub]({project['link']})")

def main():
    st.set_page_config(page_title="Projetos Imersão IA", layout="wide", initial_sidebar_state="expanded", page_icon="🏆")
    st.title("🏆 :orange[Top Projetos] - :blue[Imersão IA]")
    st.caption("Ranking dos projetos mais votados da Imersão IA :blue[Alura] + **:blue[G]:red[o]:orange[o]:blue[g]:green[l]:red[e]**! 😸 :red[Vote no meu projeto [aqui](https://discord.com/channels/1369193715989614684/1369193716434337849/1373142479859355749)!]")
    st.info("Os votos são atualizados a cada 5 minutos.")
    
    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None

    projects = load_messages()
    sorted_projects = sorted(projects, key=lambda x: x['votos'], reverse=True)
    
    st.sidebar.error("A votação se encerra às 23:59.")
    
    # Sidebar search
    st.sidebar.title("🔎 Pesquise o seu projeto!")
    search_term = st.sidebar.text_input("Digite o nome seu nome:").lower()
    

    if search_term:
        search_results = [p for p in projects if search_term in p['nome'].lower()]
        if search_results:
            for project in search_results:
                st.sidebar.markdown("---")
                st.sidebar.markdown(f"### {project['nome']}")
                st.sidebar.markdown(f"**Votos:** {project['votos']}")
                st.sidebar.markdown(f"**Usuário Discord:** {project['usuario']}")
                st.sidebar.markdown(f"**Descrição:** {project['descricao']}")
                st.sidebar.markdown(f"[Link do Projeto]({project['link']})")
        else:
            st.sidebar.warning("Nenhum projeto encontrado.")

    cols = st.columns(3)
    for idx, project in enumerate(sorted_projects[:30]):
        col = cols[idx % 3]
        with col:
            nome_truncado = truncar_nome(project['nome'])
            st.markdown(f"##### {idx + 1}. {nome_truncado}")
            st.markdown(f"**Votos:** **{project['votos']}**")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("GitHub", url=project['link'], type="primary", use_container_width=True)
            with col2:
              if st.button("Detalhes", key=f"detalhes_{idx}", use_container_width=True):
                  st.session_state.selected_project = project
                  show_details()  # Chama o dialog aqui com o projeto certo
                  
    st.write("")
    st.write("")
    st.markdown("""
    <div style='text-align: center; font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;'>
        Feito com carinho 💙 por <a href="https://github.com/matheusaudibert" target="_blank">Matheus Audibert</a>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
