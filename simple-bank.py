from diagrams import Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis

with Diagram(name="Simple Bank", show=False):
    user = Client("User")
    simplebank = Server("Simple Bank")
    postgres = PostgreSQL("PostgreSQL")
    redis = Redis("Redis")
    mail = Server("Mail")
    asynq = mail >> Edge(label="asynq") << redis

    user \
        >> Edge(color="darkgreen", label="gRPC/httpGateway") \
        << simplebank \

    simplebank \
        >> Edge(color="brown", label="message broker") \
        << asynq

    simplebank \
        >> Edge(color="red", label="database") \
        << postgres
