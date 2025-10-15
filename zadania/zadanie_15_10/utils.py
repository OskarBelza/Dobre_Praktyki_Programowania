import csv
from pathlib import Path
from typing import List, Type
from pydantic import BaseModel


def load_data(path: Path, model: Type[BaseModel]) -> List[BaseModel]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [model.model_validate(row) for row in reader]
