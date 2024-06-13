from dataclasses import dataclass
import os
import hashlib
from collections.abc import Iterator
from typing import Callable, override

from sqlalchemy import create_engine, text, TextClause

MIGRATIONS_QUERIES: dict[str, Callable[..., TextClause]] = {
    'create': lambda schema: text(f"""
CREATE TABLE {schema}.meta (
    id          serial primary key
  , created     timestamp with time zone not null default now()
  , updated     timestamp with time zone not null default now()
  , ident       varchar(15) null
  , description varchar(255) not null
  , hash        bytea not null
);
    """),
    'insert': lambda schema, ident, desc, hash: text(f"""
INSERT INTO {schema}.meta (ident, description, hash)
     VALUES (:ident, :description, :hash)
;
    """).bindparams(ident, desc, hash),

}


@dataclass
class MigrationRecord:
    id: str | None
    description: str
    hash: bytes

    @override
    def __repr__(self) -> str:
        if self.id is None:
            return f'{self.description}.sql'
        return f'{self.id}__{self.description}.sql'


@dataclass
class MigrationCommit:
    id: str | None
    description: str
    _sql: str | None = None

    # TODO(BL) doesn't support stored procedure definitions
    def sql(self, path: str, fs_read: Callable[[str], str]) -> Iterator[str]:
        if self._sql is None:
            self._sql = fs_read(f'{path}/{self}')

        for stmt in self._sql.split(';'):
            st = stmt.strip()
            if len(st) > 0: yield st

    def hash(self, path: str, fs_read: Callable[[str], str]) -> bytes:
        if self._sql is None:
            self._sql = fs_read(f'{path}/{self}')

        return hashlib \
            .sha256(self._sql.encode('utf-8'), usedforsecurity=False) \
            .digest()

    @classmethod
    def gather(
        cls, path: str,
        fs_read: Callable[[str], str],
        fs_dir: Callable[[str], Iterator[str]]
    ) -> Iterator[tuple['MigrationCommit', Iterator['str']]]:
        for f in fs_dir(path):
            fp = f.rsplit('.', 1)
            if len(fp) != 2: continue
            elif fp[1] != 'sql': continue

            fname_parts = fp[0].split('__', 1)
            id = None
            print(fname_parts)
            if len(fname_parts) == 2:
                [idx, description] = fname_parts
                id = idx
            elif len(fname_parts) == 1:
                [description] = fname_parts
            else: continue

            print('id = ', id)

            mig = MigrationCommit(id, description)
            yield mig, mig.sql(path, fs_read)

    @override
    def __repr__(self) -> str:
        if self.id is None:
            return f'{self.description}.sql'
        return f'{self.id}__{self.description}.sql'


def env(*names: str) -> tuple[str, ...]:
    if len(names) == 0:
        raise ValueError("call this function with environment variable names")

    vs = tuple((os.getenv(k) for k in names))
    missing = [k for k, v in zip(names, vs) if v is None]

    if len(missing) > 0:
        raise ValueError('missing environment variables:\n{}'.format(
            '\n'.join([f'    - {k}' for k in missing])))

    return tuple((v for v in vs if v is not None))


def env_database_connection_str(prefix: str, visit_var: Callable[[str], str] | None = None) -> str:
    vv = visit_var or str.upper
    return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(*env(*(vv(f'{prefix}_{x}') for x in [
        "username",
        "password",
        "host",
        "port",
        "database",
    ])))


def fs_read(file: str) -> str:
    with open(file, 'r') as f:
        return f.read()


def fs_dir(file: str) -> Iterator[str]:
    yield from (x for x in os.listdir(file))


if __name__ == "__main__":
    eng = create_engine(env_database_connection_str('db'))



    mig_dir = f'{os.getcwd()}/{env('MIGRATIONS_DIR')[0]}'
    print(mig_dir)
    mig_commits = MigrationCommit.gather(mig_dir, fs_read, fs_dir)
    for mig, sql in mig_commits:
        print(mig, list(sql))

    exit(1)
