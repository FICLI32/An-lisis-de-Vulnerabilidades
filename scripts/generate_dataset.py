import pandas as pd
import json
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
LOGGER = logging.getLogger(__name__)

def generate_comparison_dataset(results_path, output_file):
    path = Path(results_path)
    if not path.exists():
        LOGGER.error(f"El directorio {results_path} no existe.")
        return

    json_files = list(path.glob("*.json"))
    if not json_files:
        LOGGER.warning(f"No se encontraron archivos JSON en {results_path}.")
        return

    all_data = []

    for file in json_files:
        LOGGER.info(f"Procesando {file.name}...")
        try:
            with open(file, "r") as f:
                data = json.load(f)
            
            artifacts = data.get("artifacts", [])
            repo_name = file.stem
            
            # Estadísticas básicas
            total_artifacts = len(artifacts)
            
            # Distribución por tipo
            types = {}
            languages = {}
            for art in artifacts:
                art_type = art.get("type", "unknown")
                art_lang = art.get("language", "unknown")
                types[art_type] = types.get(art_type, 0) + 1
                languages[art_lang] = languages.get(art_lang, 0) + 1
            
            # Crear fila de resumen
            row = {
                "repo": repo_name,
                "total_dependencies": total_artifacts,
                "top_language": max(languages, key=languages.get) if languages else "N/A",
                "unique_types": len(types),
                "unique_languages": len(languages)
            }
            
            # Añadir conteos por tipo como columnas (prefijadas con 'type_')
            for t, count in types.items():
                row[f"type_{t}"] = count
                
            all_data.append(row)
            
        except Exception as e:
            LOGGER.error(f"Error al procesar {file.name}: {e}")

    # Crear DataFrame
    df = pd.DataFrame(all_data).fillna(0)
    
    # Asegurar que el directorio de salida existe
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar CSV
    df.to_csv(output_file, index=False)
    LOGGER.info(f"Dataset de comparación guardado en {output_file}")
    
    return df

if __name__ == "__main__":
    RESULTS_DIR = "data/results"
    OUTPUT_CSV = "data/repo_comparison_dataset.csv"
    generate_comparison_dataset(RESULTS_DIR, OUTPUT_CSV)
