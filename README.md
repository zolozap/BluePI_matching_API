# Requirements

<a href="https://www.python.org/" target="new">
    <img src="https://img.shields.io/badge/python-v3.7-blue" alt="Python 3.6+">
</a>
<a href="https://pypi.org/project/fastapi" target="new">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://ubuntu.com/" target="new">
    <img src="https://img.shields.io/badge/ubuntu-v18.04.1--0ubuntu1-blue" alt="Ubuntu">
</a>
<a href="https://www.uvicorn.org" target="new">
    <img src="https://raw.githubusercontent.com/tomchristie/uvicorn/master/docs/uvicorn.png" width="40px" height="40px" alt="Uvicorn">
</a>
<a href="https://www.docker.com/" target="new">
    <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/horizontal-logo-monochromatic-white.png?itok=SBlK2TGU" width="80px" height="40px" alt="Docker">
</a>

# Install Virtualenvironments

<div class="termy">

```console
$ pip install virtualenv

```

</div>

# Create new environment
<div class="termy">

```console
$ virtualenv {{env_name}}

```

</div>

# How to Use environment

<div class="termy">

```console
$ source {{env_name}}/bin/activate

```

</div>

# Install package

<div class="termy">

```console
$ pip install -r requirements.txt

```

</div>

# Deploy manually with Uvicorn
uvicorn app.main:app --host {{your_host}} --port {{your_port}} --reload <br>
eg.<br>
<div class="termy">

```console
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```

</div>
<br>

# Deploy with Docker
#### Build docker container ####

<div class="termy">

```console
$ docker build -t bluepi_api .

```

</div>

#### Run container ####
<div class="termy">

```console
$ docker run -d --name bluepi_api_container -p {{your_port}}:8080 bluepi_api

```

</div>

#### Re-Run container ####
<div class="termy">

```console
$ docker start bluepi_api_container

```

</div>

# API Documents
go to <a href="http://{{your_host}}:{{your_port}}/docs">http://{{your_host}}:{{your_port}}/docs</a>