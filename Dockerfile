FROM mcr.microsoft.com/windows/servercore:ltsc2019

SHELL ["cmd", "/S", "/C"]

WORKDIR C:\app

ENV PYTHONUTF8=1
ENV PYTHONIOENCODING=utf-8

# Download embedded Python
ADD https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip C:\python.zip

# Extract Python (SINGLE LINE – IMPORTANT)
RUN powershell -Command "Expand-Archive C:\python.zip C:\Python; Remove-Item C:\python.zip"

# Enable pip
ADD https://bootstrap.pypa.io/get-pip.py C:\Python\get-pip.py
RUN C:\Python\python.exe C:\Python\get-pip.py

# Add Python to PATH
ENV PATH="C:\Python;%PATH%"

# Install dependencies
COPY requirements.txt .
RUN C:\Python\python.exe -m pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 3000

CMD ["C:\\Python\\python.exe", "app.py"]
