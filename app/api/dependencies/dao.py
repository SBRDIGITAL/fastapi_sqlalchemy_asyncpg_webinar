from app.api.dao.user import user_dao, UserDAO



def get_user_dao() -> UserDAO:
    """ ## Возвращает экземпляр класса `UserDAO`. """
    return user_dao