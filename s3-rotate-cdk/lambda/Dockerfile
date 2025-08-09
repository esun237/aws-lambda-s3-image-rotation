FROM public.ecr.aws/lambda/python:3.12

# Native deps Pillow may use
RUN dnf -y install gcc gcc-c++ zlib-devel libjpeg-turbo-devel && dnf clean all

# Python deps into the Lambda task root
COPY requirements.txt .
RUN python -m pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# App code
COPY handler.py ${LAMBDA_TASK_ROOT}

# Lambda entrypoint
CMD ["handler.lambda_handler"]
