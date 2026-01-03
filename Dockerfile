FROM mcr.microsoft.com/windows/servercore:ltsc2019

WORKDIR C:/app

# Download Python installer
ADD https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe C:/python-installer.exe

# Install Python and delete installer (CMD context)
RUN cmd /S /C C:\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 ^&^& del C:\python-installer.exe

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
