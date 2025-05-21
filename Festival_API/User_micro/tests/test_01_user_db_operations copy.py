import pytest
from daos.User_dao import UserDAO

def test_user_crud():
    dao = UserDAO()
    user = dao.create('testuser', 'test@example.com')
    assert user.id is not None
    fetched = dao.get(user.id)
    assert fetched.username == 'testuser'
    updated = dao.update(user.id, username='newuser')
    assert updated.username == 'newuser'
    dao.delete(user.id)
    assert dao.get(user.id) is None