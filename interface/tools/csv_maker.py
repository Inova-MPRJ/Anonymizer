import pandas as pd

def preview_csv(uploaded_file, nrows=3):
    """Preview first few rows of CSV file"""
    try:
        df_preview = pd.read_csv(uploaded_file, nrows=nrows)
        return df_preview, None
    except Exception as e:
        return None, str(e)

def create_results_dataframe(results):
    """Convert API results to pandas DataFrame"""
    return pd.DataFrame(results)

def create_csv_content_for_download(results):
    """Create CSV content in memory for download with proper UTF-8 encoding"""
    try:
        # Prepare data for CSV
        csv_data = []
        for item in results:
            csv_data.append({
                "Texto_Original": item["texto_original"],
                "Texto_Anonimizado": item["texto_anonimizado"]
            })
        
        # Create CSV using pandas with proper UTF-8 encoding
        df = pd.DataFrame(csv_data)
        csv_content = df.to_csv(index=False, encoding='utf-8-sig')
        
        return csv_content.encode('utf-8-sig'), None
    except Exception as e:
        return None, str(e)