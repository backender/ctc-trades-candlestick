FROM python:2

ARG exchange
ENV exchange=$exchange

WORKDIR .

COPY * ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python $exchange
