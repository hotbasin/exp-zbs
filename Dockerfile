FROM ubuntu:22.04
##### FROM python:3.10.13-alpine
##### ENV PATH /usr/local/bin:$PATH

###### COPY ./main.py /BACKEND/main.py
###### COPY ./srv_api.py /BACKEND/srv_api.py
###### COPY ./requirements.txt /BACKEND/requirements.txt
###### COPY ./sqlite /BACKEND/sqlite
###### COPY ./static /BACKEND/static
###### COPY ./tests /BACKEND/tests
# COPY ./BACK /BACKEND
COPY . /BACKEND

##### ADD "./certs" "/BACKEND/certs"

STOPSIGNAL SIGTERM
EXPOSE 7077

WORKDIR /BACKEND

RUN apt update
RUN apt install -y python3-pip

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements_model.txt

ENTRYPOINT ["python3"]
CMD ["main.py"]
