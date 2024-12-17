Hello, this is my first step in learning data engineering. 

In this repo, I have ingested Green NY taxi data from this link https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet containing NY Green taxi trips for the month of september on year 2019.

this already has a dockerfile having python as base image, and having different libraries installed 
this also has an ingest python script where it will require parameters like the URLs of the data to be ingested 
and postgre configurations 

additionally, there is also a docker-compose yaml file with defined services which is for postgre database since this is
where we will upload the ingested data from a script within the dockerfile and also another service for pgadmin which is
a tool to access the postgre providing a gui for it. 

building on this, what we need is to build and up the docker-compose first before building and running the dockerfile.

we can do this by inputting the following command on the terminal

first:
docker-compose up --build -d

second:
docker build -t taxi_ingest:v1

third: 
URL_GREEN="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"
URL_ZONE="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
docker run -it \
--network=pg-network \
taxi_ingest:v1 \
    --user=root \
    --password=root \
    --host=dataingestiontopostgrescoderepo-pgdatabase-1 \
    --port=5432 \
    --db=ny_taxi \
    --table-name-green=green_taxi_trips \
    --table-name-zones=zones \
    --url-green=${URL_GREEN} \
    --url-zone=${URL_ZONE}



why do we need to run in this order?
- it is because we need to setup first the postgres and the pgadmin where we will store and explore the ingested data 
from the ingestion script within the dockerfile. within the docker compose is also the network where the created 
containers/services it can be accessed by the script provided as the network parameter on the docker run command 
argument. 


is this the optimal way? 
- no. i think id like to stay it like this to record my progress while learning some concepts within data engineering
a more optimal way is to include the ingestion script or even the docker file within the docker compose so we 
dont need to have to define a network when running the docker run command. in addition, we dont even need to 
do the docker build > docker run as it will also be included in docker compose up --build command


Moving away from this, we also have a terraform file within the terraform folder. With this, we can automate working 
with gcp (google could platform) as stated in the .tf files, we have defined variables which we can use in defining 
informations needed to create storage buckets and big queries. 

all we need is to run this command in order within the terminal whilst inside the terraform directory
- terraform init
- terraform plan
- terraform apply
- terraform destroy
