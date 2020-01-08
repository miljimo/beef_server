
from setuptools import setup;

setup(
     name ="beef_servers",
     packages=["beef_servers", "beef_servers.events","beef_servers.pipelines", "beef_servers.servers", "beef_servers.editors"],
     version='1.0.12032020',
     description="beef_server implementation",
     url="https://github.com/miljimo/PyNodeGraph.git",
     author_email="johnson.obaro@hotmail.com",
     author ="Obaro I. Johnson",
     license='Apache Licence 2.0',
     install_requires=["mpi4py>=2.0",'messaging'],
     classifiers=["Target Users : Developers"]
     );
