from flask import Flask, render_template, request
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
app.secret_key = 'secret_key'
db = SQLAlchemy(app)


# define the form data model
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(7), nullable=False)

# define the size data model
class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


# define the form data model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sizes_prices = db.Column(db.String(500), nullable=False)
    colors = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    imageAdd = db.Column(db.String(2000), nullable=False)


# # create the database
# with app.app_context():
#     db.create_all()


# admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ModelView(FormData, db.session))
admin.add_view(ModelView(Size, db.session))
admin.add_view(ModelView(Product, db.session))


# home page
@app.route('/')
def home():
    products = Product.query.all()
    products_stl=[]
    for product in products:
        l = stl(product)
        products_stl.append(l)

    print(products_stl)
    return render_template('home.html',products=products_stl)

# contactus page
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

# product form
@app.route('/form', methods=['POST','GET'])
def form():
    if request.method == 'POST':
        name = request.form['name']

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
            unique_filename = str(datetime.utcnow().timestamp()) + '_' + str(random.randint(1, 1000)) + '_' + file.filename
            file_path = os.path.join('static/uploads', unique_filename)
            file.save(file_path)
            imageAdds.append(unique_filename)
        
        imageAddss=str(imageAdds)
        product = Product(name=name,sizes_prices=sizes_prices,colors=colors_list,description=description,imageAdd=imageAddss)
        db.session.add(product)
        db.session.commit()


    form_data = FormData.query.all()
    size_data = Size.query.all()
    return render_template('form.html', form_data=form_data, size_data=size_data)


# color size form
@app.route('/colorsizeform', methods=['POST','GET'])
def colorsizeform():
    if request.method == 'POST':
        if "color" in request.form.keys():
            # get the form values
            name = request.form['name']
            number = int(request.form['number'])
            color = request.form['color']

            # create a new form data object
            form_data = FormData(name=name, number=number, color=color)

            # add the form data to the database
            db.session.add(form_data)
            db.session.commit()

        elif "size" in request.form.keys():
            name = request.form['size']
            size = Size(name=name)
            db.session.add(size)
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
        
        s= [[i[4],i[5]]for i in smry[0]]
        c= [[i[0][1],i[0][2],i[0][3]] for i in smry]
        q=[[j[0] for j in i] for i in smry]
        cq=list(zip(c,q))

    return render_template('summary.html',s=s,cq=cq)


# convert database product string into list
def stl(product):
    id = product.id
    name = product.name
    sizes_prices = ast.literal_eval(product.sizes_prices)
    colors = ast.literal_eval(product.colors)
    description = product.description
    imageAdd = ast.literal_eval(product.imageAdd)
    l={'id':id,'name':name,'sizes_prices':sizes_prices,'colors':colors,'description':description,'imageAdd':imageAdd}
    return l



if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
