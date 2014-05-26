#
# Python Dockerfile
#

# Pull base image.
FROM dockerfile/ubuntu

# Install Python.
RUN apt-get install -y python python-dev python-pip python-virtualenv

ADD . /src

# Define default command.
CMD ["bash"]
