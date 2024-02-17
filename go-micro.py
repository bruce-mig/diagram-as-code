from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.database import Mongodb
from diagrams.onprem.queue import Rabbitmq

with Diagram(name="Go Micro", show=False):
    user = Client("User")
    broker = Server("Broker \n Microservice")
    mail = Server("Mail \n Microservice")

    with Cluster("Logger"):
        logger = Server("Logger \n Microservice")
        mongo = Mongodb("MongoDB")
        logger \
            >> Edge(color="red", label="gRPC") \
            << mongo

    with Cluster("Authentication"):
        auth = Server("Auth \n Microservice")
        postgres = PostgreSQL("PostgreSQL")
        auth \
            >> Edge(color="red", label="gRPC") \
            << postgres

    with Cluster("Listener"):
        listener = Server("Listener \n Microservice")
        rabbitmq = Rabbitmq("RabbitMQ(DB)") 
        rabbitmq \
            >> Edge(color="red", label="gRPC") \
            >> listener

    user \
        >> Edge(color="black", label="http") \
        << broker \

    broker \
        >> Edge(color="darkgreen", label="gRPC") \
        << logger

    broker \
        >> Edge(color="darkgreen", label="gRPC") \
        >> rabbitmq
  
    listener \
        >> Edge(color="darkgreen", label="gRPC") \
        >> auth

    auth \
        >> Edge(color="darkgreen", label="gRPC") \
        >> mail
    auth \
        >> Edge(color="darkgreen", label="gRPC") \
        >> broker
