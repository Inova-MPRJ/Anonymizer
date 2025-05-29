import streamlit as st
import requests
import json

class AnonimizationUI:

    def sidebar(self):
        """Sidebar with configuration options"""
        with st.sidebar:
            st.header("Anonimizador de Dados PII")
            
            st.markdown("""
            **Instruções:**
            1. Digite ou cole o texto que deseja anonimizar na área de entrada
            2. Clique em "Anonimizar Texto" para processar
            3. O resultado aparecerá na área de saída
            """)
            
            st.markdown("---")
            
            st.markdown("""
            **Entidades Detectadas:**
            - 👤 **PERSON**: Nomes de pessoas
            - 📧 **EMAIL**: Endereços de email  
            - 📱 **PHONE_NUMBER**: Números de telefone
            - 🆔 **CPF**: Números de CPF
            - 🏫 **ESCOLA**: Nomes de escolas e instituições de ensino
            - 📍 **ENDEREÇO**: Endereços e localização
            """)
            
            st.markdown("---")
            
            st.markdown("""
            **Sobre:**
            Esta ferramenta utiliza o Microsoft Presidio para identificar e anonimizar 
            informações pessoais identificáveis (PII) em textos em português.
            """)

    def main_container(self):
        """Main container with input and output text areas"""
        st.header("🔒 Anonimização de Dados Pessoais")
        
        # Create two columns for input and output
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Texto Original")
            
            # Sample text for demonstration
            sample_text = """Olá, meu nome é João Silva e moro em São Paulo. 
                            Meu email é joao.silva@email.com e meu telefone é (11) 99999-9999.
                            Meu CPF é 123.456.789-10 e trabalho na empresa XYZ Ltda."""
            
            st_input_text = st.text_area(
                label="Digite ou cole o texto para anonimizar:",
                value=sample_text if not st.session_state.get("input_text") else st.session_state.input_text,
                height=300,
                key="text_input",
                placeholder="Digite seu texto aqui..."
            )
            
            # Store input text in session state
            st.session_state.input_text = st_input_text
            
            # Anonymize button
            col1_1, col1_2 = st.columns([1, 1])
            with col1_1:
                anonymize_button = st.button(
                    "🔒 Anonimizar Texto", 
                    type="primary",
                    use_container_width=True
                )
            with col1_2:
                clear_button = st.button(
                    "🗑️ Limpar", 
                    use_container_width=True
                )
        
        with col2:
            st.subheader("✅ Texto Anonimizado")
            
            # Handle clear button
            if clear_button:
                st.session_state.input_text = ""
                st.session_state.output_text = ""
                st.session_state.processing = False
                st.rerun()
            
            # Handle anonymize button
            if anonymize_button and st_input_text.strip():
                st.session_state.processing = True
                st.rerun()
            
            # Show loading state
            if st.session_state.get("processing", False):
                with st.spinner("🔄 Processando texto... Isso pode levar alguns segundos."):
                    try:
                        # Call the anonymization API
                        response = requests.post(
                            "http://127.0.0.1:5000/",
                            json={"text": st_input_text},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            anonymized_result = result.get("Texto anonimizado", "")
                            st.session_state.output_text = anonymized_result
                            st.session_state.processing = False
                            st.success("✅ Texto anonimizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                            st.session_state.processing = False
                            st.session_state.output_text = ""
                            
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Erro: Não foi possível conectar à API. Certifique-se de que o servidor está rodando em http://127.0.0.1:5000/")
                        st.session_state.processing = False
                        st.session_state.output_text = ""
                    except requests.exceptions.Timeout:
                        st.error("❌ Erro: Timeout na requisição. O processamento está demorando muito.")
                        st.session_state.processing = False
                        st.session_state.output_text = ""
                    except Exception as e:
                        st.error(f"❌ Erro ao processar o texto: {str(e)}")
                        st.session_state.processing = False
                        st.session_state.output_text = ""
            
            # Display output
            output_text = st.session_state.get("output_text", "")
            st.text_area(
                label="Resultado da anonimização:",
                value=output_text,
                height=300,
                key="text_output",
                placeholder="O texto anonimizado aparecerá aqui..."
            )
            
            # Download button (if there's output)
            if output_text:
                st.download_button(
                    label="📥 Baixar Texto Anonimizado",
                    data=output_text,
                    file_name="texto_anonimizado.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    def statistics_container(self):
        """Container to show anonymization statistics"""
        if st.session_state.get("output_text"):
            st.markdown("---")
            st.subheader("📊 Estatísticas")
            
            col1, col2, col3 = st.columns(3)
            
            input_length = len(st.session_state.get("input_text", ""))
            output_length = len(st.session_state.get("output_text", ""))
            
            with col1:
                st.metric("Caracteres Original", input_length)
            
            with col2:
                st.metric("Caracteres Anonimizado", output_length)
            
            with col3:
                if input_length > 0:
                    reduction_percent = round((1 - output_length/input_length) * 100, 1)
                    st.metric("Redução", f"{reduction_percent}%")

    def render(self):
        """Main render method"""
        st.set_page_config(
            page_title="Anonimizador de Dados PII",
            page_icon="🔒",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Initialize session state variables
        if "input_text" not in st.session_state:
            st.session_state.input_text = ""

        if "output_text" not in st.session_state:
            st.session_state.output_text = ""

        if "processing" not in st.session_state:
            st.session_state.processing = False

        # Render components
        self.sidebar()
        self.main_container()
        self.statistics_container()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "💡 **Dica:** Esta ferramenta é ideal para anonimizar documentos, emails, "
            "relatórios ou qualquer texto que contenha informações pessoais sensíveis."
        )


if __name__ == "__main__":
    AnonimizationUI().render()
