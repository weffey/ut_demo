from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=create_engine('sqlite:///database.db'))()

session.execute("DROP TABLE IF EXISTS users;")
session.execute(
    """
    CREATE TABLE users (
        id VARCHAR(36) NOT NULL PRIMARY KEY,
        username NVARCAHR(50) NOT NULL,
        password NVARCAHR(20) NOT NULL
    );
    """
)
session.commit()
session.close()
