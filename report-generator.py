from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, Oracle
from diagrams.onprem.database import Mongodb
from diagrams.onprem.inmemory import Redis

with Diagram(name="Report Generator", show=False):
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
        postgres = PostgreSQL("PostgreSQL \n (TMON users)")
        auth \
            >> Edge(color="red", label="gRPC") \
            << postgres

    with Cluster("Listener"):
        listener = Server("Listener \n Microservice")
        asynq = Redis("asynq \n Redis")
        asynq \
            >> Edge(color="red", label="asynq") \
            >> listener 
    
    with Cluster("Report Generator"):
        rpt = Server("Report Generation \n Microservice")
        orcl = Oracle("Oracle DB")
        sap = Server("192.168.1.250 \n SAP Crystal Reports")
        rpt >> Edge(color="blue") << sap
        sap >> Edge(color="blue") << orcl

    user \
        >> Edge(color="black", label="http") \
        << broker \

    broker \
        >> Edge(color="darkgreen", label="gRPC") \
        << logger

    broker \
        >> Edge(color="darkgreen", label="gRPC") \
        >> asynq
  
    listener \
        >> Edge(color="darkgreen", label="gRPC") \
        >> mail \
        >> broker

    auth \
        >> Edge(color="darkgreen", label="gRPC") \
        << broker

    listener >> Edge(color="blue", label="gRPC") \
        << rpt
    
