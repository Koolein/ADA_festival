import datetime
import os
import pytest

from daos.Festival_dao import FestivalDAO
from daos.Session_dao import SessionDAO
from db import Session, engine, Base

class TestFestivalSessionDBOP:
    @pytest.fixture(scope="session", autouse=True)
    def setup_database(self):
        # configure test database
        os.environ['DB_URL'] = 'sqlite:///festival_session_test.db'
        # create all tables
        Base.metadata.create_all(engine)

    def test_add_and_query_festival_and_session(self):
        session = Session()

        # Create and add a Festival record
        fest = FestivalDAO(
            id=1,
            name="Test Fest",
            start_date=datetime.datetime(2025, 5, 20, 10, 0),
            end_date=datetime.datetime(2025, 5, 22, 18, 0)
        )
        session.add(fest)

        # Create and add a Session record linked to the Festival
        sess = SessionDAO(
            festival_id=1,
            title="Opening Session",
            start_time=datetime.datetime(2025, 5, 20, 11, 0),
            end_time=datetime.datetime(2025, 5, 20, 12, 0)
        )
        session.add(sess)

        # Commit transactions
        session.commit()

        # Query Festivals
        festivals = session.query(FestivalDAO).all()
        print(f"\n### Total festivals: {len(festivals)}")
        for f in festivals:
            print(f"Festival {f.id}: {f.name} ({f.start_date.isoformat()} - {f.end_date.isoformat()})")

        # Query Sessions
        sessions = session.query(SessionDAO).all()
        print(f"\n### Total sessions: {len(sessions)}")
        for s in sessions:
            print(f"Session {s.id}: {s.title} [Festival {s.festival_id}] ({s.start_time.isoformat()} - {s.end_time.isoformat()})")

        # Assertions
        assert len(festivals) == 1
        assert festivals[0].id == 1
        assert festivals[0].name == "Test Fest"

        assert len(sessions) == 1
        assert sessions[0].festival_id == 1
        assert sessions[0].title == "Opening Session"

        session.close()
