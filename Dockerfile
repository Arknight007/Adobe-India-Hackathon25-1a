FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY process_pdfs.py .
COPY sample_dataset/ sample_dataset/
CMD ["python", "process_pdfs.py"]
