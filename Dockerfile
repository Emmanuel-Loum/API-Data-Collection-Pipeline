FROM python:3.8-slim-buster
COPY . .

# Installing python dependencies
RUN pip install -r requirements.txt
RUN python setup.py install

# Running Python Application
CMD ["python", "src/Project/Data_Collection_Pipeline.py"]
