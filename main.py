# main.py

import uvicorn
from fastapi import FastAPI, HTTPException
from mongita import MongitaClientDisk
from typing import Dict, List
from pydantic import BaseModel
from pyexpat import model

# objects

class Shape(BaseModel):
    name: str
    no_of_sides: int
    id: int

class OmegatProps(BaseModel):
    project_name: str
    source_lang: str
    target_lang: str

class Segments(BaseModel):
    segment_list: list = None

class Segment(BaseModel):
    segment_number: int    

class Report(BaseModel):
    report_id: str
    props: Dict[str, str] = None
    segments: List[Dict] = []


# shapes = [
#     {"item_name": "Circle", "no_of_sides": 1, "id": 1},
#     {"item_name": "Triangle", "no_of_sides": 3, "id": 2},
#     {"item_name": "Octagon", "no_of_sides": 8, "id": 3}
# ]

app = FastAPI()

client = MongitaClientDisk()
db = client.xdiff_db
reports = db.reports
# client.drop_database('db')


  
@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/reports")
async def get_reports():
    existing_reports = reports.find({})
    return [
        {key: report[key] for key in report if key != "_id"}
        for report in existing_reports
    ]

@app.get("/reports/{report_id}")
async def get_report_by_id(report_id: str):
    if reports.count_documents({"report_id": report_id}) > 0:
        report = reports.find_one({"report_id": report_id})
        return {key: report[key] for key in report if key != "_id"}
    raise HTTPException(status_code=404, detail=f"No report with id {report_id} found.")

@app.post("/reports")
async def post_report(report: Report):
    reports.insert_one(report.dict())
    return report

@app.put("/reports/{report_id}")
async def update_report(report_id: str, report: Report):
    reports.replace_one({"report_id": report_id}, report.dict(), upsert=True)
    return report

@app.delete("/reports/{report_id}")
async def delete_report(report_id: str):
    delete_result = reports.delete_many({"id": report_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No report with id {report_id} exists.")
    return {"OK": True}

@app.get("/sub")
async def call_another_func():
    x = root()
    return x

#if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

# authentication (basic auth?)
# query parameters
# web sockets???
# capps.capstan.be/api/xdiff
# add user id to props ??+
# drop mongita and upgrade to mongo?

# project_name is fine as id? or hash would be better? 
