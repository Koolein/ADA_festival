import pytest
from daos.Profile_dao import ProfileDAO
from daos.User_dao import UserDAO

def test_profile_crud():
    user_dao = UserDAO()
    user = user_dao.create('puser', 'p@example.com')
    dao = ProfileDAO()
    profile = dao.create(user.id, 'bio', 'contact')
    assert profile.id is not None
    fetched = dao.get(profile.id)
    assert fetched.user_id == user.id
    updated = dao.update(profile.id, bio='new')
    assert updated.bio == 'new'
    dao.delete(profile.id)
    user_dao.delete(user.id)