FROM python:3

WORKDIR /bot
RUN pip install pipenv
COPY Pipfile .
#RUN pipenv lock --requirements > requirements.txt
#RUN pip install -r requirements.txt
RUN pipenv install --skip-lock --system

COPY bot.py .

CMD [ "python", "./bot.py" ]
