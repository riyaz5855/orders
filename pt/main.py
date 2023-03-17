from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from datetime import datetime
import random
import ast

# flask app and configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'JzLkRtNqGpXyFbIhVuZe'
db = SQLAlchemy(app)



# define the user data model
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)



# define the form data model
class Color(db.Model):
    __tablename__ = "color"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(7), nullable=False)

# define the size data model
class Size(db.Model):
    __tablename__ = "size"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# define the category data model
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# define the smry data model
class Smry(db.Model):
    __tablename__ = "smry"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    data = db.Column(db.String(2000), nullable=False)


# define the form data model
class Product(db.Model):
    __tablename__ = "roduct"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sizes_prices = db.Column(db.String(200), nullable=False)
    colors = db.Column(db.String(1500), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    imageAdd = db.Column(db.String(600), nullable=False)




# # create the database
# with app.app_context():
#     db.create_all()


# admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ModelView(Color, db.session))
admin.add_view(ModelView(Size, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Smry, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(User, db.session))

# # Manipulate the table
# @app.route('/delete-user-table')
# def delete_user_table():
#     query = text('DROP TABLE IF EXISTS user;')
#     db.session.execute(query)
#     db.session.commit()
#     return 'User table deleted'

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Set up the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Set up a login view
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:  # Check if user is already authenticated
        return redirect(url_for('sadmin'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('sadmin'))
        except ValueError as e:
            flash(str(e))
            return render_template('login.html')
    return render_template('login.html')



@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# admin login
@app.route('/sadmin')
@login_required
def sadmin():
    if not current_user.is_admin:
        return redirect(url_for('login'))
    return render_template('sadmin.html')


# home page
@app.route('/')
def home():
    products = Product.query.all()
    products_stl=[]
    for product in products:
        l = stl(product)
        products_stl.append(l)
    category_data = Category.query.all()
    return render_template('home.html',products=products_stl,category_data=category_data)


# contactus page
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')



# add product form
@app.route('/form', methods=['POST','GET'])
@login_required
def form():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        sizes = request.form.getlist('size')
        prices = [i for i in request.form.getlist('price') if i!='']
        sizes_prices = str(list(zip(sizes,prices)))

        colors = request.form.getlist('color')
        colors_list = []
        for color in colors:
            color_parts = color.split('-')
            colors_list.append(color_parts)
        colors_list = str(colors_list)

        description = str(request.form['description'])
        
        files = request.files.getlist('photo')
        # create a directory to store the files if it doesn't exist
        UPLOADS_FOLDER = os.path.join(app.static_folder, 'uploads')
        if not os.path.exists(UPLOADS_FOLDER):
            os.makedirs(UPLOADS_FOLDER)
        
        # loop through the files and save them to the server
        imageAdds = []
        for file in files:
            # generate a unique filename using timestamp and random string
            unique_filename = str(datetime.utcnow().timestamp()) + '_' + str(random.randint(1, 10000))
            file_path = os.path.join('static/uploads', unique_filename)
            file.save(file_path)
            imageAdds.append(unique_filename)
        
        imageAddss=str(imageAdds)
        product = Product(name=name,category=category,sizes_prices=sizes_prices,colors=colors_list,description=description,imageAdd=imageAddss)
        db.session.add(product)
        db.session.commit()


    color_data = Color.query.all()
    size_data = Size.query.all()
    category_data = Category.query.all()
    return render_template('form.html', color_data=color_data, size_data=size_data, category_data=category_data)


# color size form
@app.route('/colorsizeform', methods=['POST','GET'])
@login_required
def colorsizeform():
    if request.method == 'POST':
        if "color" in request.form.keys():
            # get the form values
            name = request.form['name']
            number = int(request.form['number'])
            color = request.form['color']

            # create a new form data object
            color_data = Color(name=name, number=number, color=color)

            # add the form data to the database
            db.session.add(color_data)
            db.session.commit()

        elif "size" in request.form.keys():
            name = request.form['size']
            size = Size(name=name)
            db.session.add(size)
            db.session.commit()
        
        elif "category" in request.form.keys():
            name = request.form['category']
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()

    # render a thank you message
    return render_template('colorsizeform.html')


# order page
@app.route('/order')
def order():
    id = request.args.get('id')
    productstr = Product.query.filter_by(id=id).first()
    product = stl(productstr)
    return render_template('order.html',product=product)


# summary page
@app.route('/summary', methods=['POST','GET'])
def summary():
    if request.method == 'POST':
        name=request.form['name']
        category=request.form['category']
        data=request.form.getlist('data')
        data2=request.form.getlist('ddata')
        ddata=[]
        for i in data2:
            x=i.split("-")
            ddata.append(x)
        l=[[x] + y for x, y in zip(data,ddata)]
        grouped_data = {}
        for item in l:
            color = item[1]  # extract the color from the item
            if color not in grouped_data:
                grouped_data[color] = []
            grouped_data[color].append(item)

        grouped_list = list(grouped_data.values())
        smry = [lst for lst in grouped_list if any(int(item[0]) > 0 for item in lst)]
        
        s= [[i[4],int(i[5])]for i in smry[0]]
        c= [[i[0][1],i[0][2],i[0][3]] for i in smry]
        q=[[int(j[0]) for j in i] for i in smry]
        cq=list(zip(c,q))

        
        # create a dictionary to store the size and quantity information
        size_dict = {}
        for i, size_info in enumerate(s):
            # get the size code and price from the size_info sublist
            size_code, price = size_info
            # get the corresponding quantity sublist from l2 and sum the values
            quantity = sum([sublist[i] for sublist in q])
            # store the size and quantity information in the dictionary
            size_dict[size_code] = {"quantity": quantity, "price": price}

        # calculate the total price
        amount_list=[]
        for info in size_dict.values():
            price = info["quantity"] * info["price"]
            amount_list.append(price)
        total_amount=sum(amount_list)
        l=str([s,cq,name,size_dict,total_amount,category])

    return render_template('summary.html',s=s,cq=cq,name=name,size_dict=size_dict,category=category,total_amount=total_amount,l=l)



# success page
@app.route('/success', methods=['POST','GET'])
def success():
    if request.method == "POST":
        name= str(datetime.utcnow().timestamp()) + '_' + str(random.randint(1, 10000))
        data = request.form['data']
        smry = Smry(name=name,data=data)
        db.session.add(smry)
        db.session.commit()
        url = url_for('receipt', odrname=name, _external=True)

    return render_template('success.html',url=url)



# receipt page
@app.route('/receipt/<odrname>')
def receipt(odrname):
    rpt=Smry.query.filter_by(name=odrname).first()
    smry=ast.literal_eval(rpt.data)
    s,cq,name,size_dict,total_amount,category = smry
    return render_template('receipt.html',s=s,cq=cq,name=name,size_dict=size_dict,total_amount=total_amount,category=category)


# dsb page
@app.route('/dsb')
@login_required
def dsb():
    products = Product.query.all()
    products_stl=[]
    for product in products:
        l = stl(product)
        products_stl.append(l)
    return render_template('dsb.html',products=products_stl)


# update page
@app.route('/update/<int:id>', methods=['POST','GET'])
@login_required
def update(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        new_name = request.form['name']
        product.name = new_name

        new_category = request.form['category']
        product.category = new_category

        sizes = request.form.getlist('size')
        prices = [i for i in request.form.getlist('price') if i!='']
        new_sizes_prices = str(list(zip(sizes,prices)))
        product.sizes_prices = new_sizes_prices

        colors = request.form.getlist('color')
        colors_list = []
        for color in colors:
            color_parts = color.split('-')
            colors_list.append(color_parts)
        new_colors_list = str(colors_list)
        product.colors = new_colors_list

        new_description = str(request.form['description'])
        product.description = new_description
        
        files = request.files.getlist('photo')
        
        if files[0].filename != '':
            # create a directory to store the files if it doesn't exist
            UPLOADS_FOLDER = os.path.join(app.static_folder, 'uploads')
            if not os.path.exists(UPLOADS_FOLDER):
                os.makedirs(UPLOADS_FOLDER)
            
            # loop through the files and save them to the server
            imageAdds = []
            for file in files:
                # generate a unique filename using timestamp and random string
                unique_filename = str(datetime.utcnow().timestamp()) + '_' + str(random.randint(1, 1000)) + '_' + file.filename
                file_path = os.path.join('static/uploads', unique_filename)
                file.save(file_path)
                imageAdds.append(unique_filename)
            
            new_imageAddss = str(imageAdds)

            # delete existing image
            old_images=ast.literal_eval(product.imageAdd)
            # loop through the files and delete each one
            for old_image in old_images:
                print(old_image)
                # if old_image in files:
                os.remove(os.path.join('static/uploads', old_image))
            product.imageAdd = new_imageAddss
        db.session.commit()
        return redirect(url_for('dsb'))


    productstr = Product.query.filter_by(id=id).first()
    product = stl(productstr)
    i=int(product["id"])
    name=product["name"]
    category=product["category"]
    s=[i[0] for i in product["sizes_prices"]]
    p=[i[1] for i in product["sizes_prices"]]
    c=[i[2] for i in product["colors"]]
    description=product["description"]
    imageAdd=product["imageAdd"]
    l=[s,p,c,i,name,description,imageAdd,category]
    color_data = Color.query.all()
    size_data = Size.query.all()
    category_data = Category.query.all()
    return render_template('update.html', l=l, color_data=color_data, size_data=size_data, category_data=category_data)



# delete page
@app.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    # delete existing image
    old_images=ast.literal_eval(product.imageAdd)
    # loop through the files and delete each one
    for old_image in old_images:
        print(old_image)
        # if old_image in files:
        os.remove(os.path.join('static/uploads', old_image))
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('dsb'))


# convert database product string into list
def stl(product):
    id = product.id
    name = product.name
    category = product.category
    sizes_prices = ast.literal_eval(product.sizes_prices)
    colors = ast.literal_eval(product.colors)
    description = product.description
    imageAdd = ast.literal_eval(product.imageAdd)
    l={'id':id,'name':name, 'category':category, 'sizes_prices':sizes_prices,'colors':colors,'description':description,'imageAdd':imageAdd}
    return l



# Define a Flask view for the '/admin' endpoint
@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated and current_user.is_admin:
        # Render the default Flask-Admin index template
        return redirect('/admin/')
    else:
        # Redirect non-admin users to the login page
        return redirect(url_for('login'))




if __name__ == '__main__':
    # db.create_all()
    app.run(debug=False,host="0.0.0.0")
