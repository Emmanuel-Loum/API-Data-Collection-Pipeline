FROM python:3.8
COPY . .

RUN apt-get update && \
      apt-get -y install sudo

# Installing Selenium
# RUN sh -c 'curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/googlechrom-keyring.gpg' \
#     sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
#     apt-get -y update\
#     apt-get install -y google-chrome-stable\
#     wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip\
#     apt-get  install -yqq unzip\
#     unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/\
# Installing python dependencies

RUN python setup.py install
RUN pip install -r requirements.txt


# Running Python Application
CMD ["python", "src/Project/Data_Collection_Pipeline.py"]
