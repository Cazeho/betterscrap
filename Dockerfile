FROM python:slim-buster

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

# Update the system and install required dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl gnupg --no-install-recommends

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends


RUN google-chrome-stable --version

# Assuming a successful fetch of Chrome version, proceed to get ChromeDriver

# Install ChromeDriver (Separated commands for debugging)
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d'.' -f1) && \
    echo $CHROME_VERSION


RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip -P ~/ && \
    unzip ~/chromedriver-linux64.zip -d ~/ && \
    mv -f ~/chromedriver-linux64 /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

# Cleanup to reduce image size
RUN apt-get purge --auto-remove -y curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* ~/chromedriver_linux64.zip




ENTRYPOINT ["streamlit","run"]
CMD ["app.py" ]
EXPOSE 8501

