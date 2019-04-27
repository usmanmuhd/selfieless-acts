from threading import Thread

from .models import setup_db, initialize_db, get_db
from .tasks import check_containers_health
from .utils import start_container

if __name__ == '__main__':
    setup_db()
    initialize_db()
    cid = start_container(8000)
    cur, con = get_db()
    cur.execute("insert into instances (port, cont_id) values (?,?)", (
        8000, cid
    ))
    con.commit()
    con.close()
    Thread(target=check_containers_health).start()
