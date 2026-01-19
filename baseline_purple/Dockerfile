FROM python:3.11-slim
WORKDIR /app
RUN pip install flask numpy
COPY agent.py .
CMD ["python", "agent.py"]
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
