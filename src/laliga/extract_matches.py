import os
import json

from laliga.api_client import FootballDataClient

from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Obtengo la API_KEY
load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

def extract_matches(season: int, api_key: str = API_KEY):

    
    if not api_key:
        raise RuntimeError("Falta la api key FOOTBALL_DATA_API_KEY")

    client = FootballDataClient(api_key)

    try:
        data = client.get_matches(season)
    finally:
        client.close()

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    output_dir = Path("data/raw")
    output_dir.mkdir(
        parents = True,
        exist_ok = True
    )

    output_path = output_dir / (
        f"laliga_matches_{season}_{timestamp}.json"
    )

    with output_path.open("x", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Partidos recibidos: {len(data['matches'])}")
    print(f"Archivo guardado: {output_path}")

    return output_path


if __name__ == "__main__":
    extract_matches(season=2026)
