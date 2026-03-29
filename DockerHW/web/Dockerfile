FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 將 web 資料夾內的所有檔案複製到容器中
COPY . .

# 安裝 flask 等依賴套件
RUN pip install --no-cache-dir -r requirements.txt

# 執行 main.py
CMD ["python", "main.py"]