FROM python:3.14

RUN apt-get update && apt-get upgrade -y && apt-get install vim -y

# Add dev requirements
ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

# Help avoid "unsupported locale setting" in Sphinx
RUN echo "export LC_ALL=C.UTF-8" > ~/.bashrc
