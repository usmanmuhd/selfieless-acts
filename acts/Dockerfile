# set the base image
FROM alpine:3.7
RUN apk add --update --no-cache py3-pip
RUN apk add py3-psycopg2

# environment variable
ENV TEAM_ID=CC_212_215_216_245

# Copy the current directory contents into the container
ADD . /project

#set directoty where CMD will execute
WORKDIR /project

# Get pip to download and install requirements:
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

ENTRYPOINT ["./entrypoint.sh"]
