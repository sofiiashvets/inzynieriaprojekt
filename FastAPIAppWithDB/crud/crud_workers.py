from typing import List

from sqlalchemy import or_, null
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from models.salary import Salary
from models.worker import Worker
from schemas.child import ChildSchema
from schemas.worker import WorkerSchema


class CRUDWorkers:
    """
    Workers facade
    """

    def get_all(self, db: Session) -> List[WorkerSchema]:
        """Fetch all workers."""
        query = db.query(Worker).limit(100)
        return [WorkerSchema.model_validate(w) for w in query]

    def get_all_by_name(self, db: Session, q: str) -> List[WorkerSchema]:
        """
        Fetch all workers by name.

        Parameters:
        q - Search by first name or last name
        """
        query = db.query(Worker).filter(or_(Worker.imie == q, Worker.nazwisko == q)).limit(100)
        return [WorkerSchema.model_validate(w) for w in query]

    def get(self, db: Session, worker_id: int) -> Optional[WorkerSchema]:
        """Fetch a worker by ID."""
        worker = db.query(Worker).filter(Worker.pesel == str(worker_id)).first()
        return WorkerSchema.model_validate(worker) if worker else None

    def get_workers_by_depart_id(self, db: Session, dept_id: int) -> List[WorkerSchema]:
        """Fetch all workers in a department."""
        workers = db.query(Worker).filter(Worker.department_id == dept_id).all()
        return [WorkerSchema.model_validate(w) for w in workers]

    def add_or_update(self, db: Session, data: WorkerSchema) -> Optional[WorkerSchema]:
        """Add or update a worker."""
        worker = db.query(Worker).filter(Worker.pesel == data.pesel).first()
        if worker is None:
            worker = Worker(
                pesel=data.pesel,
                imie=data.imie,
                nazwisko=data.nazwisko,
                age=data.age,
                criminal_record=data.criminal_record,
                children=data.children,
                department_id=data.department_id
            )
            db.add(worker)
        else:
            worker.pesel = data.pesel
            worker.imie = data.imie
            worker.nazwisko = data.nazwisko
            worker.age = data.age
            worker.criminal_record = data.criminal_record
            worker.children = data.children
            worker.department_id = data.department_id

        db.commit()
        return WorkerSchema.model_validate(worker)

    def delete(self, db: Session, worker_pesel: str) -> bool:
        """Delete a worker by PESEL."""
        try:
            workers = db.query(Worker).filter(Worker.pesel == worker_pesel).all()
            salary = db.query(Salary).filter(Salary.worker_pesel == worker_pesel).all()

            for s in salary:
                db.delete(s)

            for w in workers:
                db.delete(w)

            db.commit()
            return True
        except Exception:
            return False

    def add_or_update_child(self, db: Session, worker_id: int, child_schema: ChildSchema) -> Optional[WorkerSchema]:
        """Add or update a child for a worker."""
        worker = db.query(Worker).filter(Worker.pesel == str(worker_id)).first()
        if worker is None:
            return None

        for child in worker.children:
            if child["dob"] == child_schema.dob or child["imie"] == child_schema.imie:
                child["imie"] = child_schema.imie
                child["dob"] = child_schema.dob
                flag_modified(worker, "children")
                db.commit()
                return WorkerSchema.model_validate(worker)

        worker.children.append(child_schema.dict())
        flag_modified(worker, "children")
        db.commit()
        return WorkerSchema.model_validate(worker)

    def add_or_update_salary(self, db: Session, worker_id: int, month: int, amount: int) -> Optional[WorkerSchema]:
        """Add or update a worker's salary."""
        worker_pesel = str(worker_id)
        sal = db.query(Salary).filter(Salary.worker_pesel == worker_pesel, Salary.month == month).first()

        if sal is None:
            sal = Salary(month=month, amount=amount, worker_pesel=worker_pesel)
            db.add(sal)
        else:
            sal.month = month
            sal.amount = amount

        db.commit()
        return self.get(db, worker_id)