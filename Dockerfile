FROM python:3.13

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi","run","backend/api.py"]
