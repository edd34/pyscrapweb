FROM python:3.10

RUN apt install -y g++

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN g++ -c -fPIC add.cpp -o add.o

RUN g++ -shared -Wl,-soname,libadd.so -o libadd.so  add.o

ENTRYPOINT ["python3", "main.py"]

CMD [ "--help" ]