from flask import Flask
import docker

app = Flask(__name__)
client = docker.from_env()

from . import views
