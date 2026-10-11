
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Read the CSV file
df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    data = df.copy()

    if class_:
        data = data[data["class"].isin(class_)]

    return {
        "students": data.rename(
            columns={"studentId": "studentId"}
        ).to_dict(orient="records")
    }
