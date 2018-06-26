from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from demo.config import CONN_STR

def set_er_up(conn_str=None):
    if not conn_str:
        conn_str = CONN_STR
    session = sessionmaker(bind=create_engine(conn_str))()

    session.execute("DROP TABLE IF EXISTS users;")
    session.execute(
        """
        CREATE TABLE users (
            id VARCHAR(36) NOT NULL PRIMARY KEY,
            username NVARCHAR(50) NOT NULL,
            password NVARCHAR(20) NOT NULL
        );
        """
    )
    session.commit()
    session.close()

if __name__ == '__main__':
    set_er_up()
