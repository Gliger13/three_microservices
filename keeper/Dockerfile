# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /three_microservices/keeper/

# copy the dependencies file to the working directory
COPY ./ ./
# copy the content of the local src directory to the working directory
COPY keeper/ ./

# install dependencies
RUN python setup.py install


CMD [ "python", "./bot.py" ]