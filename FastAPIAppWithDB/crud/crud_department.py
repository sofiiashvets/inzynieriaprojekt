from typing import List

from sqlalchemy import null, func
from sqlalchemy.orm import Session

from crud.crud_workers import CRUDWorkers
from models.department import Department
from models.worker import Worker
from schemas.department import DepartmentSchema, DepartmentSchemaWL

crud_w = CRUDWorkers()

class CRUDDepartment:
    """
    Departments facade
    """

    def get_by_name(self, db: Session, q: str) -> List[DepartmentSchema]:
        """
        Fetch all departments by name.

        Parameters:
        q - Search by name
        """
        query = db.query(func.count(Worker.pesel), Department).join(Department).filter(Department.name == q).group_by(Department.id).limit(100)
        out_list = []
        for dep in query:
            dep_schema = DepartmentSchema.from_orm(dep.Department)
            dep_schema.workers_no = dep[0]
            out_list.append(dep_schema)
        return out_list

    def get_by_name_with_workers(self, db: Session, q: str) -> List[DepartmentSchemaWL]:
        """Fetch all departments by name with workers."""
        query = db.query(func.count(Worker.pesel), Department).join(Department).filter(Department.name == q).group_by(Department.id).limit(100)
        out_list = []
        for dep in query:
            dep_schema = DepartmentSchemaWL.from_orm(dep.Department)
            dep_schema.workers = crud_w.get_workers_by_depart_id(db, dep_schema.id)
            out_list.append(dep_schema)
        return out_list

    def get(self, db: Session, department_id: int) -> Optional[DepartmentSchema]:
        """Fetch a department by ID."""
        try:
            dep = db.query(Department).filter(Department.id == department_id).first()
            if not dep:
                return None

            out_dep = DepartmentSchema.from_orm(dep)
            work_no = db.query(Worker).filter(Worker.department_id == dep.id).count()
            out_dep.workers_no = work_no
            return out_dep
        except Exception:
            return None

    def add_or_update(self, db: Session, data: DepartmentSchema) -> DepartmentSchema:
        """Add or update a department."""
        dep = db.query(Department).filter(Department.id == data.id).first()
        if dep is None:
            dep = Department(
                id=data.id,
                name=data.name,
                street=data.street,
                city=data.city,
                postcode=data.postcode,
            )
            db.add(dep)
        else:
            dep.name = data.name
            dep.street = data.street
            dep.city = data.city
            dep.postcode = data.postcode

        db.commit()
        return DepartmentSchema.from_orm(dep)

    def delete(self, db: Session, department_id: int) -> bool:
        """Delete a department by ID."""
        try:
            workers = db.query(Worker).filter(Worker.department_id == department_id).all()
            departments = db.query(Department).filter(Department.id == department_id).all()

            db.begin()
            for w in workers:
                db.delete(w)
            for d in departments:
                db.delete(d)
            db.commit()
            return True
        except Exception:
            return False

    def add_worker(self, db: Session, department_id: int, worker_id: int) -> bool:
        """Add a worker to a department."""
        try:
            worker_pesel = str(worker_id)
            worker = db.query(Worker).filter(Worker.pesel == worker_pesel).first()
            if worker:
                worker.department_id = department_id
                db.commit()
                return True
            return False
        except Exception:
            return False

    def delete_worker(self, db: Session, worker_id: int) -> bool:
        """Remove a worker from a department."""
        try:
            worker_pesel = str(worker_id)
            worker = db.query(Worker).filter(Worker.pesel == worker_pesel).first()
            if worker:
                worker.department_id = null()
                db.commit()
                return True
            return False
        except Exception:
            return False