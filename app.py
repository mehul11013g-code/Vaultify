from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
import os, json
import cloudinary
import cloudinary.uploader
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'vaultify_secret_2026'

# ─── CLOUDINARY CONFIG ──────────────────────────────────
cloudinary.config(
    cloud_name = 'dzrz5ptgn',
    api_key    = '818831473748646',
    api_secret = 'CEt8_eWQo-SMSA21GVRO4tZaqo0',
    secure     = True
)

OWNER_PASSWORD = 'vaultify@owner2026'

# ─── POSTGRESQL DATABASE ────────────────────────────────
DATABASE_URL = 'postgresql://postgres:Manish_20100@db.jxbskhyoeuffnvwssqgs.supabase.co:5432/postgres'

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id          SERIAL PRIMARY KEY,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            price       TEXT NOT NULL,
            mrp         TEXT NOT NULL,
            discount    TEXT NOT NULL,
            badge       TEXT DEFAULT '',
            description TEXT NOT NULL,
            specs       TEXT DEFAULT '[]',
            image       TEXT DEFAULT '',
            emoji       TEXT DEFAULT '💛',
            bg          TEXT DEFAULT 'linear-gradient(140deg,#e8ddd0,#c4b49f)',
            visible     INTEGER DEFAULT 1
        )
    ''')
    cur.execute('SELECT COUNT(*) FROM products')
    count = cur.fetchone()['count']
    if count == 0:
        defaults = [
            ('Gold Chain Necklace','Jewellery','₹2,199','₹3,499','37% off','New In',
             'A delicate 18K gold-plated chain necklace designed to be worn alone or layered. Lightweight, skin-friendly, and built to last through every season.',
             json.dumps([['Material','18K Gold-Plated Brass'],['Length','45 cm + 5 cm extender'],['Clasp','Lobster Claw'],['Finish','Polished Gold'],['Skin Safe','Yes, Nickel-free']]),
             '','💛','linear-gradient(140deg,#e8ddd0,#c4b49f)'),
            ('Obsidian Mesh Watch','Watches','₹5,499','₹8,999','39% off','',
             'A sleek matte-black mesh band watch with sapphire-coated glass. Minimal dial, maximum impact.',
             json.dumps([['Movement','Japanese Quartz'],['Case Size','40mm'],['Glass','Sapphire Coated'],['Strap','Stainless Mesh'],['Water Resistant','3 ATM']]),
             '','🖤','linear-gradient(140deg,#2c2c28,#1a1a16)'),
            ('Pearl Drop Earrings','Jewellery','₹1,499','₹2,299','35% off','Bestseller',
             'Freshwater pearl drops on sterling silver posts. Elegant for work, stunning for evenings.',
             json.dumps([['Material','Sterling Silver + Freshwater Pearl'],['Pearl Size','8mm'],['Backing','Push-back'],['Finish','Rhodium-plated'],['Skin Safe','Yes, Hypoallergenic']]),
             '','🤍','linear-gradient(140deg,#ddd5c8,#bfb3a0)'),
            ('Amber Glow Serum','Beauty','₹899','₹1,499','40% off','Limited',
             'A lightweight vitamin C serum with bakuchiol. Gives a natural glow without irritation.',
             json.dumps([['Volume','30ml'],['Key Ingredients','Vit C, Bakuchiol, Niacinamide'],['Skin Type','All Skin Types'],['Fragrance','Free'],['Cruelty Free','Yes']]),
             '','🧴','linear-gradient(140deg,#c9a96e,#9e7a3e)'),
            ('Diamond Stud Earrings','Jewellery','₹3,299','₹4,999','34% off','',
             'Classic solitaire CZ diamond studs set in sterling silver. Timeless and brilliant.',
             json.dumps([['Material','Sterling Silver + CZ Stone'],['Stone Size','5mm'],['Backing','Screw-back'],['Finish','Rhodium-plated'],['Skin Safe','Yes, Hypoallergenic']]),
             '','💎','linear-gradient(140deg,#f0e6d3,#d4c4a8)'),
            ('Rose Gold Dial Watch','Watches','₹4,199','₹6,499','35% off','New In',
             'A warm rose gold dial watch with genuine leather strap. The perfect blend of classic and contemporary.',
             json.dumps([['Movement','Japanese Quartz'],['Case Size','38mm'],['Glass','Mineral'],['Strap','Genuine Leather'],['Water Resistant','3 ATM']]),
             '','🥇','linear-gradient(140deg,#e8e0d0,#c8baa0)'),
            ('Rose Petal Lip Tint','Beauty','₹499','₹799','38% off','',
             'A buildable lip tint with hyaluronic acid. Keeps lips soft and kissable all day.',
             json.dumps([['Volume','8ml'],['Finish','Glossy Tint'],['Key Ingredient','Hyaluronic Acid'],['Shade','Rose Petal 01'],['Cruelty Free','Yes']]),
             '','💄','linear-gradient(140deg,#f5e6e8,#e8c4c8)'),
            ('Emerald Bangle Set','Jewellery','₹1,899','₹2,999','37% off','New In',
             'A set of 3 stackable gold-plated bangles with emerald green stone accents.',
             json.dumps([['Material','Gold-Plated Brass + Glass Stone'],['Set Of','3 Bangles'],['Stone','Emerald Green Glass'],['Inner Diameter','2.4 inches'],['Skin Safe','Yes, Nickel-free']]),
             '','💚','linear-gradient(140deg,#d4e8d4,#a8c8a8)'),
        ]
        cur.executemany('''INSERT INTO products
            (name,category,price,mrp,discount,badge,description,specs,image,emoji,bg)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', defaults)
    conn.commit()
    cur.close()
    conn.close()

# ─── OWNER REQUIRED DECORATOR ───────────────────────────
def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('owner'):
            return redirect(url_for('owner_login'))
        return f(*args, **kwargs)
    return decorated

# ─── CONSUMER ROUTES ────────────────────────────────────
@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE visible=1')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:pid>')
def product(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id=%s', (pid,))
    p = cur.fetchone()
    cur.execute('SELECT * FROM products WHERE id!=%s AND visible=1 LIMIT 3', (pid,))
    related = cur.fetchall()
    cur.close()
    conn.close()
    if not p: return redirect('/')
    specs = json.loads(p['specs']) if p['specs'] else []
    return render_template('product.html', p=p, related=related, specs=specs)

@app.route('/api/products')
def api_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE visible=1')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ─── OWNER ROUTES ───────────────────────────────────────
@app.route('/owner/login', methods=['GET','POST'])
def owner_login():
    if request.method == 'POST':
        if request.form.get('password') == OWNER_PASSWORD:
            session['owner'] = True
            return redirect(url_for('owner_dashboard'))
        return render_template('owner_login.html', error='Incorrect password. Try again.')
    return render_template('owner_login.html', error=None)

@app.route('/owner/logout')
def owner_logout():
    session.clear()
    return redirect('/')

@app.route('/owner')
def owner_redirect():
    if not session.get('owner'):
        return redirect(url_for('owner_login'))
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/dashboard')
@owner_required
def owner_dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('owner_dashboard.html', products=products)

@app.route('/owner/product/add', methods=['GET','POST'])
@owner_required
def owner_add_product():
    if request.method == 'POST':
        specs = []
        keys   = request.form.getlist('spec_key')
        values = request.form.getlist('spec_val')
        for k, v in zip(keys, values):
            if k.strip(): specs.append([k.strip(), v.strip()])
        image = ''
        if 'image' in request.files:
            f = request.files['image']
            if f and f.filename:
                result = cloudinary.uploader.upload(f, folder='vaultify')
                image = result['secure_url']
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO products
            (name,category,price,mrp,discount,badge,description,specs,image,emoji,bg,visible)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)''', (
            request.form['name'], request.form['category'],
            request.form['price'], request.form['mrp'],
            request.form['discount'], request.form.get('badge',''),
            request.form['description'], json.dumps(specs), image,
            request.form.get('emoji','🛍️'),
            request.form.get('bg','linear-gradient(140deg,#e8ddd0,#c4b49f)')
        ))
        conn.commit()
        cur.close()
        conn.close()
        flash('Product added successfully! ✓')
        return redirect(url_for('owner_dashboard'))
    return render_template('owner_product_form.html', product=None, specs=[], action='Add')

@app.route('/owner/product/edit/<int:pid>', methods=['GET','POST'])
@owner_required
def owner_edit_product(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id=%s', (pid,))
    p = cur.fetchone()
    if not p:
        cur.close(); conn.close()
        return redirect(url_for('owner_dashboard'))
    if request.method == 'POST':
        specs = []
        keys   = request.form.getlist('spec_key')
        values = request.form.getlist('spec_val')
        for k, v in zip(keys, values):
            if k.strip(): specs.append([k.strip(), v.strip()])
        image = p['image']
        if 'image' in request.files:
            f = request.files['image']
            if f and f.filename:
                result = cloudinary.uploader.upload(f, folder='vaultify')
                image = result['secure_url']
        cur.execute('''UPDATE products SET
            name=%s, category=%s, price=%s, mrp=%s, discount=%s, badge=%s,
            description=%s, specs=%s, image=%s, emoji=%s, bg=%s, visible=%s
            WHERE id=%s''', (
            request.form['name'], request.form['category'],
            request.form['price'], request.form['mrp'],
            request.form['discount'], request.form.get('badge',''),
            request.form['description'], json.dumps(specs), image,
            request.form.get('emoji', p['emoji']),
            request.form.get('bg', p['bg']),
            1 if request.form.get('visible') else 0, pid
        ))
        conn.commit()
        cur.close(); conn.close()
        flash('Product updated successfully! ✓')
        return redirect(url_for('owner_dashboard'))
    specs = json.loads(p['specs']) if p['specs'] else []
    cur.close(); conn.close()
    return render_template('owner_product_form.html', product=p, specs=specs, action='Edit')

@app.route('/owner/product/delete/<int:pid>', methods=['POST'])
@owner_required
def owner_delete_product(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id=%s', (pid,))
    conn.commit()
    cur.close(); conn.close()
    flash('Product deleted.')
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/product/toggle/<int:pid>', methods=['POST'])
@owner_required
def owner_toggle_product(pid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT visible FROM products WHERE id=%s', (pid,))
    p = cur.fetchone()
    cur.execute('UPDATE products SET visible=%s WHERE id=%s', (0 if p['visible'] else 1, pid))
    conn.commit()
    cur.close(); conn.close()
    return redirect(url_for('owner_dashboard'))

# ─── RUN ────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
