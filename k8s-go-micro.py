from diagrams import Diagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.podconfig import ConfigMap, Secret
from diagrams.onprem.gitops import Flux, ArgoCD
from diagrams.onprem.network import Istio, Consul

with Diagram("k8s go micro", show=False, direction="TB"):
	svc = Service("svc")
	dp = Deployment("dp")
	# istio = Istio("Istio")
	consul = Consul("Consul")
	
	net = Ingress("microbank.com") \
			>> consul >> svc
			# >> istio >> svc

	net >> [Pod("front-end"),
			Pod("auth"),
			Pod("broker"),
			Pod("listener"),
			Pod("logger"),
			Pod("mail")] << dp << HPA("hpa")
	dp << ConfigMap("Config")
	dp << Secret("Secret")
	# dp << Flux("Flux")
	dp << ArgoCD("ArgoCD")

	
