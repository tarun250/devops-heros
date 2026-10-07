FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# tests run inside the image too, so a broken build can't produce an image
RUN python -m pytest -q

RUN useradd --uid 10001 calc
USER 10001

# interactive calculator: docker run -it <image>
CMD ["python", "app/calculator.py"]
