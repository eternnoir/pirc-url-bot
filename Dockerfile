#
# Python Dockerfile
#

# Pull base image.
FROM dockerfile/ubuntu

# Install Python.
RUN apt-get install -y python python-dev python-pip python-virtualenv

ADD . /src

RUN pip install -r /src/requirements.txt

# Define default command.
CMD ["python","/src/urlBot.py"]
