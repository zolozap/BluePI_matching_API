#### BluePI_test_matching_API ####

######################################
# Virtual environments
sudo pip install virtualenv
# Create environment
virtualenv {{env_name}}
# Use environment
source {{env_name}}/bin/activate
# Install package
pip install -r requirements.txt
#### Deploy manually with Uvicorn ####
uvicorn app.main:app --host {{your_host}} --port {{your_port}} --reload
eg.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
######################################

#### Deploy with Docker ####
# Build docker container
docker build -t bluepi_api .
# Run container
docker run -d --name bluepi_api_container -p {{your_port}}:8000 bluepi_api
# API Documents
go to http://{{your_host}}:{{your_port}}/docs