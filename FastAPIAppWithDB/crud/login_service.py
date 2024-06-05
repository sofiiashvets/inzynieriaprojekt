
import bcrypt

from sqlalchemy.orm import Session

from models.login_data import LoginData


class LoginService:


    def login_user(self, db: Session, login: str, password: str):

        user = db.query(
            LoginData
        ) \
        .filter(LoginData.username == login) \
        .first()

        if user.password == password:
            return True

        return False






