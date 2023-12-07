FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install greenlet

COPY . .

ENV FLASK_APP=url_shortener
ENV FLASK_ENV=development
ENV SECRET_KEY=MY_SECRET_KEY
ENV DATABASE_URI=sqlite:///db.sqlite3

CMD ["flask", "run", "--host=0.0.0.0"]

