# Dockerfile para Backend-Data
FROM python:3.11-slim

# Crear usuario no-root para OpenShift
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py .

# Cambiar permisos
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD ["python", "app.py"]