import time
import requests

from .models import get_db
from .utils import start_container, stop_container


def check_containers_health():
    while True:
        cur, con = get_db()
        cur.execute(
            """
            select port from instances
            """
        )
        ports = [i[0] for i in cur.fetchall()]
        for port in ports:
            res = requests.get("http://127.0.0.1:%d/api/v1/_health" % port)
            if res.status_code == 500:
                requests.post("http://127.0.0.1:%d/api/v1/_crash" % port)
                stop_container(port)
                cid = start_container(port)
                cur.execute(
                    "update instances set cont_id=? where port=?",
                    (cid, port)
                )
                con.commit()
        time.sleep(1)


def auto_scale():
    while True:
        time.sleep(120)
        cur, con = get_db()
        cur.execute(
            """
            select n_requests from meta
            """
        )
        n_requests = cur.fetchone()[0]
        cur.execute(
            """
            update meta set n_requests = 0
            """
        )
        con.commit()
        con.close()
        n_conts = (n_requests // 20) + 1
        cur.execute("select count(*) from instances")
        cur_conts = cur.fetchone()[0]
        while cur_conts > n_conts:
            cur.execute("select max(port) from instances")
            port = cur.fetchone()[0]
            cur.execute("delete from instances where port=?", (port,))
            requests.post("http://127.0.0.1:%d/api/v1/_crash" % port)
            stop_container(port)
            cur_conts -= 1
        while cur_conts < n_conts:
            cur.execute("select max(port) from instances")
            port = cur.fetchone()[0]
            port += 1
            cid = start_container(port)
            cur.execute(
                "insert into instances (port, cont_id) values (?,?)", (
                    port, cid
                )
            )
            cur_conts += 1
        con.commit()
        con.close()
