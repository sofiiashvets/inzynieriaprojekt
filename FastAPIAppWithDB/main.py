import os

import bcrypt
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Body, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from connection import *
from crud.crud_department import CRUDDepartment
from crud.crud_workers import CRUDWorkers
from crud.login_service import LoginService
from database import Session
from models.login_data import LoginData
from schemas.child import ChildSchema
from schemas.department import DepartmentSchemaCreate
from schemas.worker import WorkerSchema

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# origins = [
#     "http://localhost:8080"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

templates = Jinja2Templates(directory="templates")

crud_workers = CRUDWorkers()
crud_departments = CRUDDepartment()
login_service = LoginService()


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/workers")
def get_all_workers(db : Session = Depends(get_db)):

    result =  crud_workers.get_all(db)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Workers not found")



@app.get("/workers/get/{name}")
def get_workers(name: str, db: Session = Depends(get_db)):

    result = crud_workers.get_all_by_name(db, name)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Workers not found")


@app.get("/workers/id/{id}")
def get_workers(id: int, db: Session = Depends(get_db)):

    result = crud_workers.get(db, id)

    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Worker not found")


@app.post("/workers/update")
def add_or_update_worker(worker: WorkerSchema, db: Session = Depends(get_db)):

    return crud_workers.add_or_update(db, worker)


@app.delete("/workers/delete/{pesel}")
def delete_worker(pesel: str, db: Session = Depends(get_db)):

    return crud_workers.delete(db, pesel)


@app.post("/workers/update/child/{pesel}")
def add_or_update_child(pesel: int, child: ChildSchema, db: Session = Depends(get_db)):

    return crud_workers.add_or_update_child(db,pesel,child)


@app.post("/workers/update/salary/")
def add_or_update_child(pesel: int, month: int, amount: int, db: Session = Depends(get_db)):

    return crud_workers.add_or_update_salary(db,pesel,month,amount)


#############################Departments###############################################################################


@app.get("/departments/{name}")
def get_dept_by_name(name: str, db: Session = Depends(get_db)):

    result = crud_departments.get_by_name(db,name)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Departments not found")


@app.get("/departments/id/{id}")
def get_dept_by_name(id: int, db: Session = Depends(get_db)):

    result = crud_departments.get(db,id)

    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Department not found")

@app.post("/departments/update")
def add_or_update_department(department: DepartmentSchemaCreate, db: Session = Depends(get_db)):

    return crud_departments.add_or_update(db,department)


@app.delete("/departments/delete/{id}")
def delete_department(id: int, db: Session = Depends(get_db)):

    return crud_departments.delete(db,id)


@app.post("/departments/add_worker/")
def add_worker_to_department(dept_id: int,worker_pesel: int, db: Session = Depends(get_db)):

    return crud_departments.add_worker(db,dept_id,worker_pesel)

@app.post("/departments/delete_worker/")
def delete_worker_from_department(worker_pesel: int, db: Session = Depends(get_db)):

    return crud_departments.delete_worker(db,worker_pesel)


##################################Files#################################################################################

@app.get("/locust")
async def get_locust():

    file_path = f"C:\\Users\\sgrad\\PycharmProjects\\locust\\locustfile.py"

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="download/xDD")  # jak sie wpisze jakies głupoty to pobiera plik XD
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/files/")
async def create_file(file: bytes = File()): #Czytanie pliku. obiera plik jako jego kontekst
    return {"file_size": file}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None): # Pobiera plik jako obiekt

    return {"filename": file.file.read()}


@app.post("/savefile")
async def save_file(file : UploadFile):

    file_name = file.filename[0: -4] # works only with .txt

    outFileName = f"C:\\Users\\sgrad\\Desktop\\{file_name}_saved.txt"
    outFile = open(outFileName, "w")

    print(type(file.file))

    file_context = str(file.file.read())
    file_context = file_context[2: len(file_context)-1]

    outFile.write(file_context)
    outFile.close()

    return True


@app.get("/readfile/{filename}")
async def read_file(filename : str):

    file_path =f"C:\\Users\\sgrad\\Desktop\\{filename}"

    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/cat")
async def get_cat():

    file_path = f"C:\\Users\\sgrad\\Desktop\\cat.jpg"

    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/downloadfile/{filename}")
async def read_file(filename : str):

    file_path =f"C:\\Users\\sgrad\\Desktop\\{filename}"

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="download/xDD") #jak sie wpisze jakies głupoty to pobiera plik XD
    else:
        raise HTTPException(status_code=404, detail="File not found")

######################################################HTML##############################################################

@app.get("/login")
async def get_html(request: Request):

    file_path = f"C:\\Users\\sgrad\\Desktop\\HTMl\\FastApi\\index.html"

    if os.path.exists(file_path):
        return templates.TemplateResponse("index.html",{"request": request})
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/departments")
def submit(request: Request, login: str = Form(...), password: str = Form(...),db: Session = Depends(get_db)):

    dept = []
    dept.append(crud_departments.get(db,1))
    dept.append(crud_departments.get(db,2))
    dept.append(crud_departments.get(db,3))
    dept.append(crud_departments.get(db,4))
    dept.append(crud_departments.get(db,5))

    if login_service.login_user(db,login,password):
        return templates.TemplateResponse("departments.html",{"request": request,"list": dept})
    else:
        return templates.TemplateResponse("index.html",{"request": request})


################################################ VUE API ###############################################################

@app.get("/api/v1/workers/get/{name}")
def get_workers(name: str, db: Session = Depends(get_db)):

    result = crud_workers.get_all_by_name(db, name)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Workers not found")


@app.get("/api/v1/departments/{name}")
def get_dept_by_name(name: str, db: Session = Depends(get_db)):

    result = crud_departments.get_by_name_with_workers(db,name)

    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Departments not found")





