# Dockerfile extending the generic Python image with application files for a
# single application. This is only used for pre- env: 2 deployments.

# The name of this image is for historical reasons 'python-compat', but it
# refers to a version of the runtime separate from the 'runtime: python-compat'
# image.

FROM beta.gcr.io/google_appengine/python-compat

ADD . /app

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN add-apt-repository ppa:transmissionbt/ppa
RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install transmission-cli transmission-common transmission-daemon python-libtorrent

RUN wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py 
RUN python get-pip.py

EXPOSE 9091
RUN pip install transmissionrpc

RUN service transmission-daemon start
