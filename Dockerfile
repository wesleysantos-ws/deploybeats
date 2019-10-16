FROM python:3.7.4-alpine
ARG TIER
ARG PORT
ENV TIER=${TIER}
LABEL project="deploy" TIER="${TIER}"
WORKDIR /app
ADD src/${TIER}/ /app
RUN python3 -m pip install -r requirements.txt
CMD /bin/sh -c "exec python3 ${TIER}.py"
EXPOSE ${PORT}
