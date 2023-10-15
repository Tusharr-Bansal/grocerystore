from flask import current_app as app
from flask import render_template, request, session, redirect
from applications.database import db
from applications.models import * 

class Userinfo():
    username = None

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method=="GET":
        return render_template("USERLOGIN.html", message="Welcome! Please Login.")
    elif request.method=="POST":
        rows = Users.query.all()
        username=request.form["username"]
        password=request.form["password"]
        flag = 0
        for row in rows:
            if row.Username == username and row.Password == password:
                flag = 1
                break
            elif row.Username == username and row.Password != password:
                flag = 2
                break
        if flag == 1:
            session['user'] = username
            cat = Categories.query.all()
            return redirect("/userstore")
            #return render_template("USERSTORE.html", message="Feel free to shop!", categories=cat)
        elif flag == 0:
            return redirect("/register")
            #return render_template("REGISTER.html", message="Seems like you have not yet Signed up! Please Sign up first!")
        elif flag == 2:
            return render_template("USERLOGIN.html", message="The password was incorrect. Please Try again.")
            


@app.route("/adminlogin", methods=["GET", "POST"])
def admin():
    if request.method=="GET":
        return render_template("ADMINLOGIN.html", message="Please Enter your Details")
    elif request.method=="POST":
        #print("=================IN POST===================")
        rows = Admins.query.all()
        username=request.form["username"]
        password=request.form["password"]
        flag = False
        #print("-----------------Flag----------------")
        print(flag)
        for row in rows:
            if row.Username == username and row.Password == password:
                flag = True
                break
        if flag == True:
            session['user'] = username
            return redirect("/adminstore")
        else:
            return render_template("ADMINLOGIN.html", message="Incorrect Details! Please try again.")




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("REGISTER.html", message="Become a part of our family!")
    elif request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        rows = Users.query.all()
        flag = False
        for row in rows:
            if row.Username == username:
                flag = True
        if flag == False:
            user = Users(Username=username, Password=password)
            db.session.add(user) 
            db.session.commit()
        else:
            return render_template("REGISTER.html", message="OOPS! This username is taken! Please choose anther.")
        
        return redirect("/")
        #return render_template("USERLOGIN.html", message="YAY! You are a new member.")

@app.route("/adminstore", methods=["GET", "POST"])
def adminstore():
    if session.get('user', None)!=None:
        admins = Admins.query.filter(Admins.Username.like(session.get('user'))).all()
        if admins!=[]:
            return render_template("ADMINSTORE.html")
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/createcategory", methods=["GET", "POST"])
def createcategory():
    if session.get('user', None)!=None:
        admins = Admins.query.filter(Admins.Username.like(session.get('user'))).all()
        if admins!=[]:
            if request.method=="GET":
                return render_template("CREATECATEGORY.html", message="It is a Brand new day for a Brand Category!")
            elif request.method=="POST":
                cname=request.form["catname"]
                img=request.form["image"]
                categories = Categories.query.all()
                for category in categories:
                    if category.cname == cname:
                        return render_template("CREATECATEGORY.html", message="OH NO! This Category already exits! \U0001f609")
                cat = Categories(cname=cname, cimage=img)
                db.session.add(cat)
                db.session.commit()
                return redirect('/createproducts')
        else:
            return redirect("/")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")

@app.route("/editcategory", methods=["GET", "POST"])
def editcategory():
    if session.get('user', None)!=None:
        admins = Admins.query.filter(Admins.Username.like(session.get('user'))).all()
        if admins!=[]:
            if request.method=="GET":
                rows = Categories.query.all()
                return render_template("EDITCATEGORY.html", categories=rows)
            elif request.method=="POST":
                cname=request.form["catname"]
                cat = Categories.query.filter_by(cname=cname).first()
                if 'submit2' in request.form:
                    #print("==================in delete===============")
                    # delete a category
                    db.session.delete(cat)
                    db.session.commit()
                    prods = Products.query.filter_by(cname=cname).all()
                    for prod in prods:
                        db.session.delete(prod)
                        db.session.commit()
                elif 'submit1' in request.form:
                    #print("==================in edit===================")
                    rows = Categories.query.all()
                    newname = request.form["newname"]
                    img=request.form['image']
                    for row in rows:
                        if row.cname == cname:
                            if newname!='':
                                row.cname = newname
                            if img!='':
                                row.cimage = img
                            db.session.commit()
                            prods = Products.query.filter_by(cname=cname).all()
                            for prod in prods:
                                prod.cname = newname
                                db.session.commit()
                            break
                return redirect("/adminstore")
        else:
            return redirect("/")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")



@app.route("/createproducts", methods=["GET", "POST"])
def createproducts():
    if session.get('user', None)!=None:
        admins = Admins.query.filter(Admins.Username.like(session.get('user'))).all()
        if admins!=[]:
            if request.method=="GET":
                rows = Categories.query.all()
                return render_template("CREATEPRODUCTS.html", categories=rows, message="Add a Product!")
            elif request.method=="POST":
                cname=request.form["catname"]
                pname=request.form["prodname"]
                price=request.form["price"]
                quantity=request.form["quantity"]
                manufacturing_date=request.form["mandate"]
                expdate=request.form["expdate"]
                img = request.form["image"]
                prods= Products.query.all()
                rows = Categories.query.all()
                for product in prods:
                    if product.pname == pname:
                        return render_template("CREATEPRODUCTS.html", categories=rows, message="The Product already exists!")
                prod = Products(pname=pname, price=price, quantity=quantity, manufacturing_date=manufacturing_date, expdate=expdate, cname=cname, pimage=img)
                db.session.add(prod)
                db.session.commit()
                return render_template("CREATEPRODUCTS.html", categories=rows, message="Add another Product!")
        else:
            return redirect("/")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")


@app.route("/editproducts", methods=["GET", "POST"])
def editproducts():
    if session.get('user', None)!=None:
        admins = Admins.query.filter(Admins.Username.like(session.get('user'))).all()
        if admins!=[]:
            #valudate for admin
            prods = Products.query.all()
            if request.method=="GET":
                return render_template("EDITPRODUCTS.html", prods = prods)
            elif request.method=="POST":
                pname = request.form["prodname"]
                if 'submit1' in request.form:
                    #print("=================in edit======================")
                    newname = request.form["newname"]
                    price = request.form["price"]
                    quantity = request.form["quantity"]
                    mandate = request.form["mandate"]
                    expdate = request.form["expdate"]
                    prod = Products.query.filter_by(pname=pname).first()
                    if newname!='':
                        prod.pname = newname
                    if price!='':
                        prod.price = price
                    if quantity!='':
                        prod.quantity = quantity
                    if mandate!='':
                        prod.manufacturing_date = mandate
                    if expdate!='':
                        prod.expdate = expdate
                    db.session.commit()
                elif 'submit2' in request.form:
                    prod = Products.query.filter_by(pname=pname).first()
                    db.session.delete(prod)
                    db.session.commit()
                return redirect("/adminstore")
        else:
            return redirect("/")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")


@app.route("/userstore", methods=["GET", "POST"])
def userstore():
    if session.get('user', None)!=None:
        cat = Categories.query.all()
        products=Products.query.all()
        print(products)
        if request.method=="GET":
            return render_template("USERSTORE.html", categories=cat, products=products, message="You won't be disappointed!")
        elif request.method=="POST":
            if 'formcategory' in request.form:
                catname = request.form["catname"]
                if catname=='all':
                    prods = Products.query.all()
                    return redirect("/userstore")
                else:
                    prods = Products.query.filter_by(cname=catname).all()
                    category=Categories.query.filter_by(cname=catname).first()
                    return render_template("USERSTORE.html", categories=cat, cimage=category.cimage, products=prods, message="Feel Free to shop!")
            elif 'formproduct' in request.form:
                pname = request.form["prodname"]
                if pname!="All":
                    prod = Products.query.filter_by(pname=pname).all()
                    return render_template("USERSTORE.html", categories=cat, products=prod, message="You made a selection!")
                return redirect("/userstore")
            elif 'search' in request.form:
                value = request.form['textsearch']
                value = "%"+value+"%"
                cats = Categories.query.filter(Categories.cname.like(value)).all()
                if cats==[]:
                    prods = Products.query.filter(Products.pname.like(value)).all()
                    if prods==[]:
                        return render_template("USERSTORE.html", categories=cat, products=products, message="There are no such categories or products")
                    else:
                        return render_template("USERSTORE.html", categories=cat, products=prods, message="These are your desires")
                else:
                    prods=[]
                    for category in cats:
                        prod = Products.query.filter_by(cname=category.cname).all()
                        prods = prods + prod
                    return render_template("USERSTORE.html", categories=cat, products=prods, message="These are your desires")
            elif 'desiredprice' in request.form:
                dprice = request.form['dprice']
                prods = []
                if dprice == '1-200':
                    for product in products:
                        if int(product.price) <= 200:
                            prods = prods + [product]
                elif dprice == '200-400':
                    for product in products:
                        if int(product.price) > 200 and int(product.price) <= 400:
                            prods = prods + [product]
                elif dprice == '400+':
                    for product in products:
                        if int(product.price) > 400:
                            prods= prods + [product]
                return render_template("USERSTORE.html", message='these are your desires', categories=cat, products=prods)
            
            elif 'availability' in request.form:
                prods=[]
                for product in products:
                    if int(product.quantity) > 0:
                        prods = prods + [product]
                return render_template("USERSTORE.html", message='these are your desires', categories=cat, products=prods)


                
            for prod in products:
                if prod.pname in request.form:
                    if (Cart.query.filter(Cart.pname.like(prod.pname)).all()==[]):
                        quant = request.form[prod.pname+"quant"]
                        if quant!='':
                            if int(quant) > int(prod.quantity):
                                message="Oops! Sorry, we do not have the desired amount of "+prod.pname+"! The available Quantity is: "+str(prod.quantity)
                                return render_template("USERSTORE.html", categories=cat, products=products, message=message)
                            item = Cart(username=session.get('user'), pid=prod.pid, pname=prod.pname, price=prod.price, quantity=quant, cname=prod.cname)
                            db.session.add(item)
                            db.session.commit()
                            return render_template("USERSTORE.html", categories=cat, products=products, message="Don't be shy! Add another!")
                        else:
                            return render_template("USERSTORE.html", categories=cat, products=products, message="Smart huh! If I were you I would add quantity")   
                    else:
                        message = "You like "+prod.pname+" that much? \U0001F602 \n You can't add the same product twice \U0001FAE0 \n If you wanna change the quantity, remove it from your cart, and add it again!"
                        return render_template("USERSTORE.html", categories=cat, products=products, message=message)       
    else:
        return redirect('/')
        # return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")


@app.route("/viewcart", methods=["GET", "POST"])
def viewcart():
    if session.get('user', None)!=None:
        if request.method=='GET':
            items = Cart.query.filter_by(username=session.get('user')).all()
            amount=0
            for item in items:
                amount = amount + (int(item.price)*int(item.quantity))
            return render_template("CHECKOUT.html", message="Your Beautiful Cart!", items=items, amount=amount)
        if request.method=='POST':
            #print("===============IN POST==================")
            items = Cart.query.filter_by(username=session.get('user')).all()
            pname = request.form['remove']
            item = Cart.query.filter_by(pname=pname).first()
            db.session.delete(item)
            db.session.commit()
            return redirect("/viewcart")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if session.get('user', None)!=None:
            items = Cart.query.filter_by(username=session.get('user')).all()
            amount=0
            for item in items:
                prod = Products.query.filter_by(pname=item.pname).first()
                prod.quantity = int(prod.quantity) - int(item.quantity)
                amount = amount + (int(item.price)*int(item.quantity))
            db.session.commit()
            for item in items:
                db.session.delete(item)
            db.session.commit()
            return render_template("THANKYOU.html")
            #return render_template("USERLOGIN.html", message="Welcome! Please Login.")
    else:
        return redirect("/")
        #return render_template("USERLOGIN.html", message="Seems like you are logged out, please login!")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method=='GET':
        session['user']=None
        return redirect("/")
