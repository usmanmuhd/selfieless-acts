from . import client
from .models import get_db

IMAGE = ""


def start_container(port):
    cont = client.containers.run(IMAGE, detach=True, ports={80: port})
    return cont.id


def stop_container(port):
    cur, con = get_db()
    cur.execute("select cont_id from instances where port=?", (port,))
    cid = cur.fetchone()[0]
    client.containers.get(cid).stop()


def handle_image(image):
    client.containers.run(image)
