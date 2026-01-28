import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse  
from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal, Optional
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
    
class PatientUpdate(BaseModel):
    id: Annotated[Optional[str], Field(default=None, description="Patient's ID", examples=['P001'])]
    name: Annotated[Optional[str], Field(default=None, description="Patient's name")]
    city: Annotated[Optional[str], Field(default=None, description="Patient's city")]
    age: Annotated[Optional[int], Field(default=None, description="Patient's age", gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description="Patient's gender")]  
    height: Annotated[Optional[float], Field(default=None, description="Patient's height in meters", gt=0)]
    weight: Annotated[Optional[float], Field(default=None, description="Patient's weight in kilograms", gt=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)



@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_data = data[patient_id]
    updated_patient_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_data.items():
        existing_patient_data[key] = value
    existing_patient_data['id'] = patient_id
    patient_pydantic_obj=Patient(**existing_patient_data)
    existing_patient_data=patient_pydantic_obj.model_dump(exclude={'id'})
    data[patient_id] = existing_patient_data
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Patient updated successfully', 'patient':data[patient_id]})
