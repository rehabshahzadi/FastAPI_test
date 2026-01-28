import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse  
from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Patient's ID", examples=['P001'])]
    name: Annotated[str, Field(..., description="Patient's name")]
    city: Annotated[str, Field(..., description="Patient's city")]
    age: Annotated[int, Field(..., description="Patient's age", gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Patient's gender")]  
    height: Annotated[float, Field(..., description="Patient's height in meters", gt=0)]
    weight: Annotated[float, Field(..., description="Patient's weight in kilograms", gt=0)]

    @computed_field
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)   
    

    @computed_field
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.post('/create')
def create_patient(patient: Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')
    
    data[patient.id]=patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'Patient created successfully', 'patient':data[patient.id]})