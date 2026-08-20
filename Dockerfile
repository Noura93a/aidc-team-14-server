FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install --no-cache-dir -r requirements.txt

ENV HF_HOME=/opt/hf

RUN python -c "from huggingface_hub import snapshot_download; \
 snapshot_download('HuggingFaceTB/SmolLM2-360M-Instruct', \
 ignore_patterns=['onnx/*'])"

COPY . .

CMD ["python", "server.py"]