import os
import json
import argparse

from extract.api_client  import FootballDataClient
from utils.config       import load_indicators_config

from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Obtengo constantes
load_dotenv()
API_KEY         = os.getenv("FOOTBALL_DATA_API_KEY")
CONFIG          = load_indicators_config()
EXTRACT_CONFIG  = CONFIG['datasets']


def extract_data(option: str, season: str, config: dict, key: str = API_KEY):

    client = FootballDataClient(api_key=key)

    data = client._get(
        endpoint = config['endpoint'],
        params = {
            'season' : season
        }
    )

    client._save_data(
        data = data,
        raw_path = CONFIG['storage']['raw_path'],
        season=season,
        option = option
    )

    print(f" - '{option}' descargados correctamente para la season {season}")
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Extractor de datos de LaLiga"
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        choices=list(EXTRACT_CONFIG.keys()),
        help="Dataset que se desea extraer"
    )

    parser.add_argument(
        "--season",
        type=int,
        required=True,
        help="Temporada de LaLiga (año de inicio)"
    )

    arg = parser.parse_args()

    dataset = arg.dataset
    season = arg.season

    extract_data(
        option = dataset,
        season = season,
        config = EXTRACT_CONFIG[dataset],
        key = API_KEY
    )
    
