FROM python:3.11-slim

WORKDIR /app

# העתקת requirements בלבד
COPY requirements.txt .



# עדכון pip והתקנת תלותות
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר הקוד
COPY . .

# חשיפת פורט Flask
EXPOSE 5000

# הפעלת Flask
CMD ["python", "app.py"]

