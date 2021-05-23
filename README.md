#### BluePI_matching_API ####

#### Play with Uvicorn ####
# Virtualenvironments
sudo pip install virtualenv
# Create env
virtualenv {{env_name}}
# Use env
source {{env_name}}/bin/activate

# Install package
pip install -r requirements.txt

#### Play with Docker ####
# Build docker container
docker build -t bluepi_api .
# Run container
docker run -d --name bluepi_api_container -p {{port}}:8000 bluepi_api
