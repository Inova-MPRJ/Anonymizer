import streamlit as st
import requests
import json
from tools.csv_maker import preview_csv, create_results_dataframe, create_csv_content_for_download

class AnonimizationUI:

    def sidebar(self):
        """Sidebar with navigation and configuration options"""
        with st.sidebar:
            st.header("Anonimizador de Dados PII")
            
            # Navigation
            st.markdown("### 📋 Navegação")
            page = st.radio(
                "Escolha a funcionalidade:",
                ["📝 Texto", "📊 CSV"],
                key="page_selection"
            )
            
            st.markdown("---")
            
            if page == "📝 Texto":
                st.markdown("""
                **Instruções:**
                1. Digite ou cole o texto que deseja anonimizar na área de entrada
                2. Clique em "Anonimizar Texto" para processar
                3. O resultado aparecerá na área de saída
                """)
            else:
                st.markdown("""
                **Instruções CSV:**
                1. Faça upload de um arquivo CSV
                2. O sistema processará a coluna "Teor" automaticamente
                3. Baixe o resultado com todos os textos anonimizados
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
            
            return page

    def csv_upload_page(self):
        """CSV upload and processing page"""
        st.header("📊 Anonimização de Arquivos CSV")
        
        st.markdown("""
        **Esta página processa arquivos CSV com as seguintes colunas:**
        `MPRJ`, `N. Integra`, `Data da ouvidoria`, `Data na PJ`, `Noticiante`, `Noticiado`, `Tema`, `Subtema`, `**Teor**`, `Providência`, `Juntada em`, `Observação`
        
        ⚠️ **Importante:** A anonimização será aplicada apenas na coluna **"Teor"**.
        """)
        
        st.markdown("---")
        
        # File upload
        uploaded_file = st.file_uploader(
            "📁 Escolha um arquivo CSV",
            type=['csv'],
            help="Selecione um arquivo CSV para anonimizar a coluna 'Teor'"
        )
        
        if uploaded_file is not None:
            # Show file details
            file_details = {
                "Nome do arquivo": uploaded_file.name,
                "Tamanho": f"{uploaded_file.size} bytes",
                "Tipo": uploaded_file.type
            }
            
            col1, col2 = st.columns(2)
            with col1:
                st.json(file_details)
            
            with col2:
                # Process button
                process_button = st.button(
                    "🔒 Processar CSV",
                    type="primary",
                    use_container_width=True
                )
            
            # Preview CSV (first few rows)
            df_preview, error = preview_csv(uploaded_file, nrows=3)
            if error:
                st.error(f"❌ Erro ao ler o arquivo: {error}")
                return
            else:
                st.subheader("👀 Prévia do arquivo (primeiras 3 linhas)")
                st.dataframe(df_preview, use_container_width=True)
                
                # Reset file position for processing
                uploaded_file.seek(0)
            
            # Process CSV
            if process_button:
                st.session_state.csv_processing = True
                st.rerun()
            
            # Show processing state
            if st.session_state.get("csv_processing", False):
                with st.spinner("🔄 Processando arquivo CSV... Isso pode levar alguns minutos dependendo do tamanho."):
                    try:
                        # Prepare file for API call
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                        
                        # Call CSV processing API
                        response = requests.post(
                            "http://127.0.0.1:5000/upload_csv",
                            files=files,
                            timeout=300  # 5 minutes timeout for CSV processing
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.csv_result = result
                            st.session_state.csv_processing = False
                            st.success("✅ CSV processado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                            st.session_state.csv_processing = False
                            
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Erro: Não foi possível conectar à API. Certifique-se de que o servidor está rodando em http://127.0.0.1:5000/")
                        st.session_state.csv_processing = False
                    except requests.exceptions.Timeout:
                        st.error("❌ Erro: Timeout na requisição. O processamento está demorando muito.")
                        st.session_state.csv_processing = False
                    except Exception as e:
                        st.error(f"❌ Erro ao processar o arquivo: {str(e)}")
                        st.session_state.csv_processing = False
            
            # Display results
            if st.session_state.get("csv_result"):
                self.display_csv_results()

    def display_csv_results(self):
        """Display CSV processing results"""
        result = st.session_state.csv_result
        
        st.markdown("---")
        
        # Results table - show only first 3 rows
        st.subheader("📋 Prévia dos Textos Anonimizados (3 primeiras linhas)")
        
        # Convert results to DataFrame using csv_maker function
        df_results = create_results_dataframe(result["resultados"])
        
        # Show only first 3 results in expandable sections
        max_display = min(3, len(df_results))
        for idx in range(max_display):
            row = df_results.iloc[idx]
            with st.expander(f"Linha {row['linha']} - Prévia: {row['texto_original'][:50]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Texto Original:**")
                    st.text_area(
                        "Original",
                        value=row['texto_original'],
                        height=150,
                        key=f"orig_{idx}",
                        label_visibility="collapsed"
                    )
                
                with col2:
                    st.markdown("**Texto Anonimizado:**")
                    st.text_area(
                        "Anonimizado",
                        value=row['texto_anonimizado'],
                        height=150,
                        key=f"anon_{idx}",
                        label_visibility="collapsed"
                    )
        
        # Show message if there are more results
        if len(df_results) > 3:
            st.info(f"ℹ️ Mostrando apenas as 3 primeiras linhas. Total de {len(df_results)} registros processados. Use as opções de download abaixo para obter todos os resultados.")
        
        # Download options
        st.subheader("📥 Download dos Resultados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as JSON
            json_data = json.dumps(result, indent=2, ensure_ascii=False)
            st.download_button(
                label="📄 Baixar JSON Completo",
                data=json_data,
                file_name="resultados_anonimizacao.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Download only anonymized texts
            anonymized_texts = "\n\n".join([
                f"Linha {item['linha']}:\n{item['texto_anonimizado']}"
                for item in result["resultados"]
            ])
            st.download_button(
                label="📝 Baixar Textos Anonimizados",
                data=anonymized_texts,
                file_name="textos_anonimizados.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # Download as CSV using csv_maker function
            csv_content, error = create_csv_content_for_download(result["resultados"])
            if error:
                st.error(f"Erro ao gerar CSV: {error}")
            else:
                st.download_button(
                    label="📊 Baixar CSV",
                    data=csv_content,
                    file_name="textos_anonimizados.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Baixa um arquivo CSV com duas colunas: Texto_Original e Texto_Anonimizado"
                )

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
        
        if "csv_processing" not in st.session_state:
            st.session_state.csv_processing = False
        
        if "csv_result" not in st.session_state:
            st.session_state.csv_result = None

        # Render sidebar and get selected page
        current_page = self.sidebar()
        
        # Render appropriate page
        if current_page == "📝 Texto":
            self.main_container()
            self.statistics_container()
        elif current_page == "📊 CSV":
            self.csv_upload_page()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "💡 **Dica:** Esta ferramenta é ideal para anonimizar documentos, emails, "
            "relatórios ou qualquer texto que contenha informações pessoais sensíveis."
        )


if __name__ == "__main__":
    AnonimizationUI().render()
