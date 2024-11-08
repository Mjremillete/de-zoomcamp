# Start with FROM to define what base image we want to use
FROM python:3.9
# The image will be based on python 3.9 version and will run whatever tasks we have below in python 3.9

# next is RUN command where we will define what docker will run automatically on the based image

RUN pip install pandas sqlalchemy psycopg2 pyarrow

# we can define what directory the copied python script will be placed. use WORKDIR and define the relative path

WORKDIR /app

# run the python script by copying it. the script needs to be on the same directory as well

COPY ingest_data.py ingest_data.py

# ingest_data.py was defined 2 times. first is because we want to define what file is to be copied and the next
# definition is what will be its name on docker destination (name retained in this case)


# old ENTRYPOINT [ "bash"  ]

# define that the docker container will run the python right away and execute python script 'ingest_data.py'
ENTRYPOINT [ "python" , "ingest_data.py" ]

# build this dockerfile as image using this. refer to your notes for details
# docker build -t taxi_ingest:v001 .

