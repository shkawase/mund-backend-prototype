import json
from typing import Annotated, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

with open("datasets.json", encoding="utf-8") as f:
    datasets = json.load(f)


@app.get("/datasets/{dataset_id}")
def get_dataset_by_id(dataset_id: str):
    for d in datasets:
        if d.get("datasetId") == dataset_id:
            return d
    return {"error": "not found"}


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    element: Optional[str] = None
    mass: Optional[int] = None


def filter(data: dict, filter_params: FilterParams):
    if not filter_params:
        return data
    if filter_params.element:
        data = [
            d
            for d in data
            if d.get("nuclide", {}).get("element") == filter_params.element
        ]
    if filter_params.mass is not None:
        data = [
            d for d in data if d.get("nuclide", {}).get("mass") == filter_params.mass
        ]
    return data


@app.get("/datasets")
def filter_datasets(filter_query: Annotated[FilterParams, Query(...)]):
    return filter(datasets, filter_query)
