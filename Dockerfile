FROM mcr.microsoft.com/windows/servercore:ltsc2019

WORKDIR C:/app

ENV PYTHONUTF8=1
ENV PYTHONIOENCODING=utf-8

ADD https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe C:/python-installer.exe

RUN cmd /S /C C:\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 && del C:\python-installer.exe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
