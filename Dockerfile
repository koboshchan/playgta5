FROM python:3.13-slim AS builder
WORKDIR /build
COPY homepage.html loader.js game.js io_worker.js wgpu_worker.js data-manifest.json shader-index.json ./
COPY docker/prepare_site.py ./docker/prepare_site.py
COPY serve_local.py ./
RUN python docker/prepare_site.py && python -m py_compile serve_local.py

FROM python:3.13-slim AS runner
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MIRROR_ROOT=/mirror
WORKDIR /app
COPY --from=builder /build/site ./site
COPY --from=builder /build/serve_local.py ./serve_local.py
USER 65534:65534
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2).close()"
CMD ["python", "serve_local.py", "--host", "0.0.0.0", "--port", "8000"]
