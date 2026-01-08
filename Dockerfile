# Windows Server Core base
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Use cmd shell
SHELL ["cmd", "/S", "/C"]

# App directory
WORKDIR C:\app

# UTF-8 support
ENV PYTHONUTF8=1
ENV PYTHONIOENCODING=utf-8

# ---------- Install Python (EMBED VERSION – FAST & STABLE) ----------
ADD https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip C:\python.zip

RUN powershell -Command ^
    "Expand-Archive C:\python.zip C:\Python; Remove-Item C:\python.zip"

# Enable pip
ADD https://bootstrap.pypa.io/get-pip.py C:\Python\get-pip.py
RUN C:\Python\python.exe C:\Python\get-pip.py

# Add Python to PATH
ENV PATH="C:\Python;%PATH%"

# ---------- Install App Dependencies ----------
COPY requirements.txt .
RUN C:\Python\python.exe -m pip install --no-cache-dir -r requirements.txt

# ---------- Copy Application ----------
COPY . .

# ---------- App Port ----------
EXPOSE 3000

# ---------- Run Flask App ----------
CMD ["C:\\Python\\python.exe", "app.py"]
