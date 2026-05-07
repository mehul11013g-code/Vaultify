# Vaultify — Python Flask Website

## How to Run on Your Computer

### Step 1 — Install Python
Download Python from https://python.org (version 3.10 or above)

### Step 2 — Install required packages
Open terminal/command prompt in the vaultify folder and run:
```
pip install flask werkzeug
```

### Step 3 — Run the website
```
python app.py
```

### Step 4 — Open in browser
Go to: http://localhost:5000

---

## Your Two Panels

### 🛍️ Customer Store
URL: http://localhost:5000
This is what your customers see — all products, categories, product detail pages with DM to Order button.

### 🔐 Owner Dashboard
URL: http://localhost:5000/owner/login
Password: vaultify@owner2026

From here you can:
- ✅ Add new products
- ✅ Edit name, price, MRP, discount, description
- ✅ Upload real product photos
- ✅ Add/remove specifications
- ✅ Show or hide products
- ✅ Delete products
- ✅ All changes reflect INSTANTLY on the customer store!

---

## How to Host Online (Free)

### Option 1 — Render.com (Recommended)
1. Create free account at render.com
2. Upload this folder to GitHub
3. Connect GitHub to Render
4. Deploy — you get a free live link like: https://vaultify.onrender.com

### Option 2 — Railway.app
1. Create free account at railway.app
2. Upload folder, deploy
3. Get a live link instantly

---

## Folder Structure
```
vaultify/
├── app.py              ← Main Python file (the brain)
├── requirements.txt    ← Python packages needed
├── vaultify.db         ← Database (created automatically)
├── static/
│   └── uploads/        ← Your product images go here
└── templates/
    ├── base.html
    ├── index.html          ← Customer homepage
    ├── product.html        ← Product detail page
    ├── owner_login.html    ← Owner login
    ├── owner_dashboard.html← Owner dashboard
    └── owner_product_form.html ← Add/Edit product form
```
