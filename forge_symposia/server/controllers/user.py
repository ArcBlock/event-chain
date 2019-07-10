from forge_symposia.server.models import DBUser

def get_user(did):
    user = DBUser.query.filter_by(did=did).first()
    return user
