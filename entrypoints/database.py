from sqlalchemy import create_engine, text as sql

from environment.database import env_database_connection_str

if __name__ == "__main__":
    cs = env_database_connection_str('db')

    eng = create_engine(cs)

    with eng.connect() as conn:
        rs = conn.execute(sql('SELECT 1;'))

    for row in rs:
        print(row)

