FROM rasa/rasa:3.6.2

WORKDIR /app
COPY . /app

USER root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Train the model
RUN rasa train

USER 1001
EXPOSE 5005

CMD [ "run", "--enable-api", "--port", "5005", "--cors", "*" ]