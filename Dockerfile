# https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry
FROM python:3.10-slim as requirements-stage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tmp

RUN apt-get update && \
  pip install --upgrade pip && \
  pip install poetry==1.4 && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./poetry.lock* ./pyproject.toml /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

WORKDIR /src

COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

EXPOSE 80
EXPOSE 443

# This equals with onnxruntime inter_op_num_threads
# Google cloud run은 GPU 병렬 실행을 지원하지 않으므로, inter_op_num_threads를 설정하는 것은 의미가 없습니다.
# ENV OMP_NUM_THREADS=4
COPY ./src /src/

ENV U2NET_HOME .u2net
RUN python -c 'from rembg.sessions.u2net import U2netSession; U2netSession.download_models()'
# https://cloud.google.com/run/docs/tips/python#optimize_the_wsgi_server
CMD exec gunicorn -k uvicorn.workers.UvicornWorker main:app --bind :$PORT --workers 4 --threads 8 --preload --timeout 120