# استخدم صورة Python الرسمية كصورة أساس
FROM python:3.9-slim

# تعيين دليل العمل
WORKDIR /app

# نسخ جميع ملفات المشروع إلى حاوية Docker
COPY . /app

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# الأمر لتشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
