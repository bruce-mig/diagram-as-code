# Diagram as Code (DaC)

This repo contains system design diagrams for various projects for [my GitHub account](https://github.com/bruce-mig), created using the diagram as code paradigm. Diagram as code is a way of drawing diagrams using code, which makes them easier to maintain, version control, and collaborate on. 

## How it works

The diagrams in this repo are created using the [Diagrams](https://diagrams.mingrammer.com/) Python library, which supports various providers, languages, and frameworks. 

To generate a diagram, you need to write a Python script that defines the nodes and edges of your system, using the Diagrams API. Then, you can run the script and it will produce a PNG image of your diagram. 

For example, here is a script that draws a simple web service architecture:

```python
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53

with Diagram("Clustered Web Services", show=False):
    dns = Route53("dns")
    lb = ELB("lb")

    with Cluster("Services"):
        svc_group = [ECS("web1"),
                     ECS("web2"),
                     ECS("web3")]

    with Cluster("DB Cluster"):
        db_primary = RDS("userdb")
        db_primary - [RDS("userdb ro")]

    memcached = ElastiCache("memcached")

    dns >> lb >> svc_group
    svc_group >> db_primary
    svc_group >> memcached

```

And here is the output image:

![Web Service](examples\clustered_web_services.png)

## How to use this repo

You can browse the existing diagrams in this repo, or create your own ones. To create a new diagram, follow these steps:

- Install Python 3.6 or higher and the Diagrams library. For more information, see the [Diagrams installation guide](https://diagrams.mingrammer.com/docs/getting-started/installation).
- Create a new Python file in the `diagrams` folder, with a descriptive name. For example, `invoicing_system.py`.
- Write your diagram code using the Diagrams API. You can use the [Diagrams documentation](https://diagrams.mingrammer.com/docs/guides/diagram) and the [examples](https://diagrams.mingrammer.com/docs/nodes/aws) for reference.
- Run your script to generate the image file. It will be saved in the same folder as your script, with the same name but with a `.png` extension. For example, `invoicing_system.png`.
- Add your script and image file to the repo, and commit your changes. Optionally, you can also update the `README.md` file to include a description and a preview of your diagram.

<!-- ## Contributing

If you want to contribute to this repo, please follow the [contribution guidelines](docs/CONTRIBUTING.md).

## License

This repo is licensed under the [MIT License](LICENSE). -->
