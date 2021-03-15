FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt --no-cache

# Copy inference code
COPY predict.py utils.py ${LAMBDA_TASK_ROOT}/


CMD [ "predict.handler" ]
