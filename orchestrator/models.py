import sqlite3


def get_db():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    return cur, con


def setup_db():
    cur, con = get_db()
    cur.execute("drop table if exists instances")
    cur.execute("drop table if exists meta")
    cur.execute(
        """
        create table instances (
            id integer primary key,
            cont_id varchar(400),
            port integer unique,
        )
        """
    )
    cur.execute(
        """
        create table meta (
            id integer primary key,
            n_requests integer,
            robin integer default 0,
            auto_scale_started integer default 0
        )
        """
    )
    con.commit()
    con.close()


def initialize_db():
    cur, con = get_db()
    cur.execute("insert into meta (n_requests) values (?)", (0,))
    con.commit()
    con.close()
