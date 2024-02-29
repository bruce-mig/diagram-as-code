from diagrams import Diagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.podconfig import ConfigMap, Secret
from diagrams.onprem.gitops import ArgoCD
from diagrams.onprem.network import Consul

with Diagram("k8s micro bank", show=False):
	svc = Service("svc")
	dp = Deployment("dp")
	consul = Consul("Consul")
	rs = ReplicaSet("rs")

	net = Ingress("api.microbank.com \n gapi.microbank.com") \
			>> consul >> svc

	net >> [Pod("bank-app1"),
			Pod("bank-app2"),
			Pod("bank-app3")] << rs << dp << HPA("hpa")
	dp << ConfigMap("Config")
	dp << Secret("Secret")
	dp << ArgoCD("ArgoCD")
	
