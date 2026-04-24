import json

notebook_path = "nbs/sbom/generacion_sbom.ipynb"

with open(notebook_path, "r") as f:
    nb = json.load(f)

# Nuevo contenido
new_cells = [
    {
        "cell_type": "markdown",
        "id": "compare-repos",
        "metadata": {},
        "source": [
            "## Comparación de Repositorios (Dataset Estructurado)\n",
            "\n",
            "Finalmente, cargamos el dataset estructurado que permite comparar los repositorios de manera consistente. Este dataset incluye métricas agregadas por repositorio."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "load-comparison",
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "df_comparison = pd.read_csv(\"../../data/repo_comparison_dataset.csv\")\n",
            "df_comparison.sort_values(by=\"total_dependencies\", ascending=False)"
        ]
    }
]

# Añadir celdas si no existen ya
ids_existentes = [cell.get("id") for cell in nb["cells"]]
if "compare-repos" not in ids_existentes:
    nb["cells"].extend(new_cells)

with open(notebook_path, "w") as f:
    json.dump(nb, f, indent=1)

print(f"Notebook {notebook_path} actualizado correctamente.")
