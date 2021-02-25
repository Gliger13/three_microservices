# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /three_microservices/master/

# copy the dependencies file to the working directory
COPY ./ ./

# install dependencies
RUN python setup.py install

CMD [ "python", "./master/app.py" ]