from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EKS, EC2
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import RouteTable, VPCRouter, Nacl, NATGateway
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
        rt_dev = RouteTable("Route Table")
        rt_staging = RouteTable("Route Table")
        rt_prod = RouteTable("Route Table")
        rt2 = RouteTable("Route Table")
        # lb = ELB("lb")
        pvt_acl = Nacl("Pvt Sub \n Network ACL")
        dev_acl = Nacl("Dev Network ACL")
        staging_acl = Nacl("Staging Network ACL")
        prod_acl = Nacl("Prod Network ACL")

        with Cluster("(Network ACL) \n Dev Public Subnet"):
            pubsub = PublicSubnet("Dev Public Subnet \n CIDR: 10.0.0.0/24 \n (IPv4)")
        
            with Cluster("Services"):
                dev_svc_group = [EKS("dev-simple-bank1")]

        with Cluster("Staging Public Subnet"):
            pubsub = PublicSubnet("Staging Public Subnet \n CIDR: 10.0.1.0/24 \n (IPv4)")

            with Cluster("Services"):
                staging_svc_group = [EKS("staging-simple-bank1")]
        
        with Cluster("Prod Public Subnet"):
            pubsub = PublicSubnet("Prod Public Subnet \n CIDR: 10.0.2.0/24 \n (IPv4)")

            with Cluster("Services"):
                prod_svc_group = [EKS("prod-simple-bank1")]

        with Cluster("(Network ACL) \n Private Subnet"):
            pvsub = PrivateSubnet("Private Subnet \n CIDR: 10.0.3.0/24 \n (IPv4)")
            nat = NATGateway("NAT Gateway")


            with Cluster("Prod Redis"):
                redis = ElastiCache("prod_redis")
                redis - ElastiCache("replica") << Edge(label="collect") << metrics

            with Cluster("Dev/Staging DB"):
                qa_db = RDS("dev/staging_postgres")
                qa_redis = ElastiCache("qa_redis")

            with Cluster("Secret Store"):
                ec2 = EC2("ec2")
                vault = Vault("vault")
                ec2 - vault
                ss = SecretsManager("secrets")

            with Cluster("Prod DB Cluster"):
                db_primary = RDS("prod_postgres")
                db_primary - [RDS("replica")] \
                    << Edge(label="collect") << metrics

            

        dns >> igw \
            >> Edge(color="black") \
            << router \
            >> Edge(color="darkgreen") \
            << rt_dev \
            >> Edge(color="darkgreen") \
            << dev_acl \
            >> Edge(color="darkgreen") \
            << dev_svc_group \
            >> Edge(color="darkgreen") \
            << qa_db
        dev_svc_group \
            >> Edge(color="darkgreen") \
            << qa_redis
        router \
            >> Edge(color="darkorange") \
            << rt2 >> Edge(color="darkorange") \
            << pvt_acl \
            >> Edge(color="darkorange") << pvsub

        dev_svc_group >> Edge(color="darkgreen") \
            << ss
        
        router \
            >> Edge(color="red") \
            << rt_staging \
            >> Edge(color="red") \
            << staging_acl \
            >> Edge(color="red") \
            << staging_svc_group \
            >> Edge(color="red") \
            << qa_db
        staging_svc_group \
            >> Edge(color="red") \
            << qa_redis
        staging_svc_group >> Edge(color="red") \
            << ss

        router \
            >> Edge(color="blue") \
            << rt_prod \
            >> Edge(color="blue") \
            << prod_acl \
            >> Edge(color="blue") \
            << prod_svc_group \
            >> Edge(color="blue") \
            << db_primary
        prod_svc_group \
            >> Edge(color="blue") \
            << redis
        prod_svc_group >> Edge(color="blue") \
            << ss
        prod_svc_group >> Edge(color="blue") >> aggregator