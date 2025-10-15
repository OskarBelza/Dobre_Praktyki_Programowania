import csv
from pathlib import Path
from typing import List, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Optional, Dict
from sqlalchemy import select
import json
from fastapi.responses import Response


def pretty_json(rows) -> Response:
    data = [dict(r) for r in rows]
    return Response(
        content=json.dumps(list(data), indent=2, ensure_ascii=False),
        media_type="application/json",
    )


def list_all(
    db: Session,
    columns: tuple,
    order_by,
):
    rows = db.execute(select(*columns).order_by(order_by)).mappings().all()
    return pretty_json(rows)


# Obsolete
def load_data(path: Path, model: Type[BaseModel]) -> List[BaseModel]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [model.model_validate(row) for row in reader]


def load_csv(
    session: Session,
    model: Type[DeclarativeMeta],
    csv_path: Path,
    *,
    field_map: Optional[Dict[str, str]] = None,
    delimiter: str = ",",
) -> int:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        if field_map:
            for r in reader:
                rows.append({field_map.get(k, k): v for k, v in r.items()})
        else:
            rows = list(reader)

    if rows:
        session.bulk_insert_mappings(model, rows)
        session.commit()
    return len(rows)