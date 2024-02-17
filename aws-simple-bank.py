from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import RouteTable, VPCRouter
from diagrams.aws.network import Route53, VPC, InternetGateway
from diagrams.aws.network import PrivateSubnet, PublicSubnet
from diagrams.onprem.security import Vault
from diagrams.aws.security import SecretsManager
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.analytics import Spark
from diagrams.onprem.queue import Kafka
from diagrams.onprem.aggregator import Fluentd

with Diagram("aws simple bank", show=False):
    dns = Route53("dns")

    with Cluster("VPC"):
        vpc = VPC("VPC \n CIDR: 10.0.0.0/16 \n (IPv4)")
        metrics = Prometheus("metric")
        metrics << Edge(color="firebrick", style="dashed") \
            << Grafana("monitoring")
        aggregator = Fluentd("logging")
        aggregator >> Edge(label="parse") \
            >> Kafka("stream") \
            >> Edge(color="black", style="bold") \
            >> Spark("analytics")

        igw = InternetGateway("Internet Gateway")
        router = VPCRouter("Router")
        rt1 = RouteTable("Route Table")
        rt2 = RouteTable("Route Table")
        # lb = ELB("lb")

        with Cluster("(Network ACL) \n Public Subnet"):
            pubsub = PublicSubnet("Public Subnet \n CIDR: 10.0.0.0/24 \n (IPv4)")

            with Cluster("Services"):
                svc_group = [EKS("simple-bank1")]

        with Cluster("(Network ACL) \n Private Subnet"):
            pvsub = PrivateSubnet("Private Subnet \n CIDR: 10.0.1.0/24 \n (IPv4)")
            redis = ElastiCache("redis")
            redis - ElastiCache("replica") << Edge(label="collect") << metrics

            with Cluster("Secret Store"):
                ec2 = EC2("ec2")
                vault = Vault("vault")
                ec2 - vault
                ss = SecretsManager("secrets")

            with Cluster("DB Cluster"):
                db_primary = RDS("postgres")
                db_primary - [RDS("replica")] \
                    << Edge(label="collect") << metrics

        dns >> igw \
            >> Edge(color="darkgreen") \
            << router \
            >> Edge(color="darkgreen") \
            << rt1 \
            >> Edge(color="darkgreen") \
            << svc_group \
            >> Edge(color="red") \
            << db_primary
        svc_group \
            >> Edge(color="red") \
            << redis
        router \
            >> Edge(color="darkgreen") \
            << rt2
        rt2 >> Edge(color="darkgreen") << pvsub

        svc_group >> Edge(color="blue") \
            << ss
        svc_group >> Edge(color="darkorange") >> aggregator
