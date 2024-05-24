# VlanTraffic


```markdown
# مراقبة واستخدام تقارير الـ VLAN باستخدام Flask

هذا المشروع عبارة عن تطبيق Flask لمراقبة واستخدام تقارير الـ VLAN، مع بوت تلجرام للتفاعل مع المستخدم.

## هيكل المشروع

```
my-flask-app/
│
├── app.py
├── requirements.txt
├── telegram_bot.py
├── scheduler.py
├── Dockerfile
└── README.md
```

## إعداد المشروع

### 1. استنساخ المستودع

أولاً، استنسخ المستودع إلى جهازك المحلي:

```bash
git clone https://github.com/yourusername/my-flask-app.git
cd my-flask-app
```

### 2. الإعداد والتشغيل محليًا

#### تثبيت المتطلبات

تأكد من تثبيت Python، ثم قم بتثبيت المتطلبات اللازمة:

```bash
pip install -r requirements.txt
```

#### تشغيل تطبيق Flask

لتشغيل تطبيق Flask:

```bash
python app.py
```

#### تشغيل بوت تلجرام

لتشغيل بوت تلجرام:

```bash
python telegram_bot.py
```

#### تشغيل المجدول

لتشغيل المجدول:

```bash
python scheduler.py
```

### 3. النشر على Render

لنشر هذا التطبيق على Render، اتبع الخطوات التالية:

#### إنشاء حساب على Render

إذا لم يكن لديك حساب على Render، قم بالتسجيل في [Render](https://render.com/).

#### إنشاء خدمة ويب جديدة

1. اذهب إلى لوحة التحكم في Render.
2. اضغط على زر "New" واختر "Web Service".
3. اربط مستودع GitHub الخاص بالمشروع.
4. استخدم الإعدادات التالية:
   - **Environment**: اختر `Docker`.
   - **Build Command**: (اتركه فارغًا، حيث سيستخدم Render ملف `Dockerfile`).
   - **Start Command**: (اتركه فارغًا، حيث يحدد ملف `Dockerfile` أمر التشغيل).

#### إعداد متغيرات البيئة

أضف متغيرات البيئة اللازمة في لوحة التحكم في Render:
- `BOT_TOKEN`: رمز التوكن الخاص ببوت تلجرام.
- `CHAT_ID`: معرف الدردشة الخاص بك.

#### النشر

اضغط على "Create Web Service" وسيقوم Render ببناء ونشر التطبيق الخاص بك.

### 4. إعداد سكربت MikroTik

تأكد من أن سكربت MikroTik مضبوط لإرسال البيانات إلى واجهة Flask API المنشورة. حدّث `apiUrl` في سكربت MikroTik برابط خدمة الويب الخاصة بك على Render:

```rsc
:local apiUrl "https://your-flask-api.onrender.com/vlan_data"
```

### 5. التحقق من النشر

1. تأكد من ضبط راوتر MikroTik لإرسال البيانات إلى واجهة Flask API.
2. استخدم بوت تلجرام للتفاعل مع النظام، إضافة ملاحظات VLAN، وتحديد مواعيد إرسال التقارير.

## وصف ملفات المشروع

### `app.py`

هذا هو ملف تطبيق Flask الرئيسي الذي:
- يعرف تطبيق Flask ومساراته.
- يحتوي على نماذج SQLAlchemy لتخزين بيانات VLAN والملاحظات.
- يوفر نقاط النهاية لاستقبال بيانات VLAN والملاحظات.
- ينشئ تقارير بناءً على البيانات المخزنة.

### `requirements.txt`

هذا الملف يحتوي على قائمة بالاعتمادات المطلوبة للمشروع.

### `telegram_bot.py`

هذا السكربت يحدد بوت تلجرام الذي:
- يتفاعل مع المستخدمين لإضافة ملاحظات لـ VLANs.
- يسمح للمستخدمين بتحديد تردد التقارير.
- يرسل التقارير الدورية بناءً على الجدول المحدد.

### `scheduler.py`

هذا السكربت يتولى جدولة التقارير باستخدام مكتبة `schedule` ويرسلها عبر بوت تلجرام.

### `Dockerfile`

هذا الملف يحتوي على التعليمات لبناء صورة Docker للتطبيق، مما يضمن تشغيله في بيئة متسقة.

## تشغيل المشروع محليًا

إذا كنت تفضل تشغيل المشروع محليًا بدلاً من نشره على Render، اتبع هذه الخطوات:

1. **تثبيت المتطلبات**:
   ```bash
   pip install -r requirements.txt
   ```

2. **تشغيل تطبيق Flask**:
   ```bash
   python app.py
   ```

3. **تشغيل بوت تلجرام**:
   ```bash
   python telegram_bot.py
   ```

4. **تشغيل المجدول**:
   ```bash
   python scheduler.py
   ```

5. **إعداد Docker** (اختياري):
   إذا كنت تفضل استخدام Docker، قم ببناء وتشغيل حاوية Docker:
   ```bash
   docker build -t my-flask-app .
   docker run -p 5000:5000 my-flask-app
   ```

## المطور

خالد الغيلي


## المساهمة

لا تتردد في تقديم مشاكل أو طلبات سحب إذا وجدت أي أخطاء أو كانت لديك اقتراحات لتحسينات.

## الترخيص

هذا المشروع مرخص بموجب رخصة MIT.
```

هذا الملف يقدم توجيهات شاملة لكيفية تثبيت وتشغيل المشروع محليًا وعلى Render، ويضمن إعداد بيئة متكاملة لتشغيل التطبيق والبوت. تأكد من تعديل `yourusername` و`your-flask-api.onrender.com` لتناسب اسم المستخدم ورابط خدمة الويب الخاصة بك على Render.
