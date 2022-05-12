FROM python:3.8-slim-buster
COPY . . 
RUN python setup.py install
CMD ["python", "src/Project/Data_Collection_Pipeline.py"]