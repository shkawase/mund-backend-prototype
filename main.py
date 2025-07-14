import json
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()

with open("datasets.json", encoding="utf-8") as f:
    datasets = json.load(f)


@app.get("/datasets/{dataset_id}")
def get_dataset_by_id(dataset_id: str):
    for d in datasets:
        if d.get("datasetId") == dataset_id:
            return d
    return {"error": "not found"}


@app.get("/datasets")
def filter_datasets(
    element: Optional[str] = Query(None),
    mass: Optional[int] = Query(None),
):
    results = datasets
    if element:
        results = [d for d in results if d.get("nuclide", {}).get("element") == element]
    if mass is not None:
        results = [d for d in results if d.get("nuclide", {}).get("mass") == mass]
    return results
