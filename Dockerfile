FROM python:alpine
ARG tier
ARG port
ENV tier=${tier}
LABEL project="deploy" tier="${tier}"
WORKDIR /app
ADD src/${tier}/ /app
RUN python3 -m pip install -r requirements.txt
CMD /bin/sh -c "exec python3 ${tier}.py"
EXPOSE ${port}