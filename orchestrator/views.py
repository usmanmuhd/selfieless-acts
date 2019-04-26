from threading import Thread
from flask import request, jsonify
import requests

from . import app
from .models import get_db
from .tasks import auto_scale

methods_dict = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete,
}

req_url = "http://127.0.0.1:%d/%s"


@app.route("/<slug>")
def act_reroute(slug):
    if not slug.startswith("api/v1/"):
        return "The given URL does not belong to any containers"
    # re-route the request to acts container
    cur, con = get_db()
    cur.execute("select auto_scale_started from meta")
    auto_scale_started = cur.fetchone()[0]
    if auto_scale_started == 0:
        Thread(target=auto_scale).start()
        cur.execute("update meta set auto_scale_started=1")
        con.commit()
    caller = methods_dict[request.method]
    cur.execute("select count(*) from instances")
    max_port = cur.fetchone()[0]
    cur.execute("select robin from meta")
    robin = cur.fetchone()[0]
    robin = robin % max_port
    port = 8000 + robin
    robin = (robin + 1) % max_port
    cur.execute("update meta set robin=?", (robin,))
    con.commit()
    if slug not in ["api/v1/_health", "api/v1/_crash"]:
        cur.execute("update meta set n_requests = n_requests + 1")
        con.commit()
    con.close()
    addr = req_url % (port, slug)
    resp = caller(addr, json=request.get_json())
    return jsonify(resp.json())
