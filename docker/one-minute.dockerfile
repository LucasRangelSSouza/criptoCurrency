FROM python:3
WORKDIR /usr/src/app
COPY ./config/requirements.txt ./
COPY ./config/databaseParams.json ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./jobs/perMinute.py .
CMD [ "python", "./perMinute.py","1","True","Falso" ]