import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.yml"

def load_indicators_config(path: Path = CONFIG_PATH) -> dict:
  """Carga la configuración YAML desde la raíz del proyecto."""
  if not path.exists():
    raise FileNotFoundError(
        f"❌ No se encontró el archivo de configuración en la ruta esperada:"
        f" {path}"
    )

  with open(path, "r", encoding="utf-8") as f:
    return yaml.safe_load(f)

