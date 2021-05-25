# BluePI_test_matching_API

######################################
# Requirements
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

# Install Virtualenvironments

<div class="termy">

```console
$ pip install virtualenv

---> 100%
```

</div>

# Create new environment
<div class="termy">

```console
$ virtualenv {{env_name}}

---> 100%
```

</div>

# How to Use environment

<div class="termy">

```console
$ source {{env_name}}/bin/activate

---> 100%
```

</div>

# Install package

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

#### Deploy manually with Uvicorn ####
uvicorn app.main:app --host {{your_host}} --port {{your_port}} --reload <br>
eg.<br>
<div class="termy">

```console
$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

---> 100%
```

</div>
<br>
######################################

#### Deploy with Docker ####
# Build docker container
## Installation

<div class="termy">

```console
$ docker build -t bluepi_api .

---> 100%
```

</div>

# Run container
<div class="termy">

```console
$ docker run -d --name bluepi_api_container -p {{your_port}}:8000 bluepi_api

---> 100%
```

</div>

# API Documents
go to <a href="http://{{your_host}}:{{your_port}}/docs">http://{{your_host}}:{{your_port}}/docs</a>