FROM python:3.6.8
WORKDIR /test
COPY . /test
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "store_demo.py"]
