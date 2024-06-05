import json

from sqlalchemy.orm import sessionmaker

from crud.crud_department import CRUDDepartment
from crud.crud_workers import CRUDWorkers

from connection import *

from schemas.child import ChildSchema
from schemas.department import DepartmentSchema
from schemas.worker import WorkerSchema

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base.metadata.create_all(engine)

#add_to_db.add_data_to_db(session)

crud_department = CRUDDepartment()
crud_worker = CRUDWorkers()

print(crud_worker.get_all_by_name(session,""))

# print(crud_department.get(session,1))
#
# dep_schema = DepartmentSchema(id = 1, name = "DMI" ,street = "Czarneckiego" ,city ="Krzemienica" ,postcode ="37-100")
#
# crud_department.add_or_update(session,dep_schema)
#
# #print(crud_department.delete(session,1))
#
# #print(crud_department.add_worker(session,1,18163326656))
#
# print(crud_department.delete_worker(session,1,18163326656))

###########################################################################

# res = crud_worker.get_all(session,"Gia")
#
# for r in res:
#     print(r)
#
# print(crud_worker.get(session,18163326656))
#
# my_json = [{'dob': '2018-06-22T14:06:12.358997', 'imie': 'Kuba'}]
#
# worker_schema = WorkerSchema(pesel = "002602221442" ,imie = "Szymon" ,nazwisko ="Grad" ,age = 22 ,criminal_record = False, children = my_json, department_id = 2 )
#
# #print(crud_worker.add_or_update(session,worker_schema))
#
# print(crud_worker.delete(session,51308861845))
#
# crud_worker.add_or_update_salary(session,18163326656,11,10000)
#
# chlid_schema = ChildSchema(imie="Kamil",dob = '1997-06-01T22:33:02.021817')
#
# crud_worker.add_or_update_child(session,18163326656 ,chlid_schema)
#
#
# worker = crud_worker.get(session,18163326656)




session.commit()







