import streamlit as st

# Idiomas soportados
idiomas = ['Español', 'Inglés', 'Francés', 'Alemán', 'Italiano']

# Diccionario para cambiar textos en función del idioma seleccionado
textos = {
    'Español': {
        'titulo': 'Analizador de cuentas en Twitter',
        'ingreso_cuenta': 'Cuenta de Twitter',
        'boton_analizar': 'Analizar'
    },
    'Inglés': {
        'titulo': 'Twitter Account Analyzer',
        'ingreso_cuenta': 'Twitter Account',
        'boton_analizar': 'Analyze'
    },
    'Francés': {
        'titulo': 'Analyseur de Compte Twitter',
        'ingreso_cuenta': 'Compte Twitter',
        'boton_analizar': 'Analyser'
    },
    'Alemán': {
        'titulo': 'Twitter Account Analyse',
        'ingreso_cuenta': 'Twitter-Konto',
        'boton_analizar': 'Analysieren'
    },
    'Italiano': {
        'titulo': 'Analizzatore di account Twitter',
        'ingreso_cuenta': 'Account Twitter',
        'boton_analizar': 'Analizzare'
    }
}

def main():
    # Selección de idioma
    idioma_seleccionado = st.sidebar.selectbox('Elige un idioma', idiomas)

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #007bff;
            color: white;
            border-color: #007bff;
            border-radius: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Configuración de idioma
    st.title(textos[idioma_seleccionado]['titulo'])

    # Entrada de texto
    usuario_texto = st.text_input(textos[idioma_seleccionado]['ingreso_cuenta'])

    if st.button(textos[idioma_seleccionado]['boton_analizar']):
        # Botones de filtrar
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Filtrar 1"):
                filtrar_1(usuario_texto)
        with col2:
            if st.button("Filtrar 2"):
                filtrar_2(usuario_texto)
        with col3:
            if st.button("Filtrar 3"):
                filtrar_3(usuario_texto)

        mostrar_resultados(usuario_texto)

def filtrar_1(usuario_texto):
    # Lógica de filtrado 1
    st.write(f"Filtrado 1: {usuario_texto}")

def filtrar_2(usuario_texto):
    # Lógica de filtrado 2
    st.write(f"Filtrado 2: {usuario_texto}")

def filtrar_3(usuario_texto):
    # Lógica de filtrado 3
    st.write(f"Filtrado 3: {usuario_texto}")

def mostrar_resultados(usuario_texto):
    st.title("Resultados")
    st.header("Cuenta de usuario: " + usuario_texto)

    st.markdown("---")
    st.markdown('<div style="background-color: white; padding: 40px 400px; font-size: 20px;">Texto dentro del rectángulo 1</div>', unsafe_allow_html=True)
    st.markdown('<span style="background-color: green; color: white; padding: 10px; border-radius: 5px; font-size: 14px;">Positivo</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="background-color: white; padding: 40px 400px; font-size: 20px;">Texto dentro del rectángulo 2</div>', unsafe_allow_html=True)
    st.markdown('<span style="background-color: red; color: white; padding: 10px; border-radius: 5px; font-size: 14px;">Negativo</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="background-color: white; padding: 40px 400px; font-size: 20px;">Texto dentro del rectángulo 3</div>', unsafe_allow_html=True)
    st.markdown('<span style="background-color: green; color: white; padding: 10px; border-radius: 5px; font-size: 14px;">Positivo</span>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

