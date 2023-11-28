import os,random,string
from flask import render_template, abort, flash, request,redirect, make_response, session,jsonify
from werkzeug.security import generate_password_hash,check_password_hash

from pkg import app
from pkg import db
from pkg.models import Fos,Farmers,States,Lga

@app.route('/',methods=['GET','POST'])
def reg():
    if request.method=="GET":
        states=db.session.query(States).all()
        return render_template('index.html',states=states)
    else:
        fname=request.form.get('firstname')
        surname=request.form.get('surname')
        lname=request.form.get('othername')
        phone=request.form.get('phonenumbers')
        email=request.form.get('emails')
        gender=request.form.get('gender')
        state=request.form.get('state')
        lga=request.form.get('lga')
        village=request.form.get('village')
        password=request.form.get('password')
        enc_pwd = generate_password_hash(password)
        cert=request.form.get('edqualify')
        homeaddress=request.form.get('homeaddress')
        guarantorname=request.form.get('guarantorname')
        guarantorphone=request.form.get('guarantorphone')
        guarantoraddress=request.form.get('guarantoraddress')
        record=Fos(fo_phone=phone,fo_email=email,fo_fname=fname,fo_surname=surname,fo_lname=lname,fo_gender=gender,fo_state=state,fo_lga=lga,fo_village=village,fo_pass=enc_pwd,fo_cert=cert,fo_address=homeaddress,fo_guaname=guarantorname,fo_guaphone=guarantorphone,fo_guaaddress=guarantoraddress)
        db.session.add(record)
        db.session.commit()
        flash(f'Congrats {fname} {lname}. You can now login !')
        return redirect('/login')


#ajax route for lga to show
@app.route('/getlga/')
def getlga():
    empty = ""
    state = request.args.get('statee')
    all =db.session.execute(f"select * from lga where state_id='{state}'")
    for a in all:
        empty = empty + f"<option value='{a.lga_name}'>{a.lga_name}</option>"
    return empty

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('index.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        
        record = db.session.query(Fos).filter(Fos.fo_email==email).first()
    
        if record and check_password_hash(record.fo_pass,password):
            session['loggedin']= record.fo_id
            flash('welcome back')
            return redirect('/fo_dashboard')
        else:
            flash('Invalid login credentials. please try again')
            return redirect('/login')


@app.route('/fo_dashboard/')
def fo_dashboard():
    loggedin = session.get('loggedin')
    if loggedin:
        data= db.session.query(Fos).filter(Fos.fo_id==loggedin).first()
        return render_template('fo_dashboard.html',data=data)
    else:
        return redirect('/login')




# @app.route('/display-messages/',methods=['GET'])
# def display():
#     sp = db.session.execute("select * from contact")
#     names = sp.fetchmany(5)
#     return render_template('submit.html',names=names)


@app.route('/register/')
def register():
    loggedin = session.get('loggedin')
    if loggedin:
        if request.method=='GET':
            data= db.session.query(Fos).filter(Fos.fo_id==loggedin).first()
            return render_template('farmer_reg.html',data=data)
    else:
        return redirect('/login')


@app.route('/my farmers/')
def myfarmers():
    loggedin = session.get('loggedin')
    if loggedin:
        data= db.session.query(Fos).filter(Fos.fo_id==loggedin).first()
        famadata=db.session.query(Farmers).filter(Farmers.fo_id==loggedin).all()
        return render_template('my_farmers.html',data=data,famadata=famadata)
    else:
        return redirect('/login')

@app.route('/view farmer profile/')
def seefarmerprofile():
    loggedin = session.get('loggedin')
    data= db.session.query(Fos).filter(Fos.fo_id==loggedin).first()
    return render_template('seefarmers.html',data=data)

@app.route('/farmer_reg/',methods=['GET','POST'])
def regfarmers():
    loggedin =session.get('loggedin')
    if loggedin:
        if request.method == "GET":
            render_template('farmer_reg.html')
        else:
            fname=request.form.get('firstname')
            surname=request.form.get('surname')
            othernames=request.form.get('othernames')
            phonenumber=request.form.get('phonenumber')
            gender=request.form.get('gender')
            role=request.form.get('role')
            address=request.form.get('address')
            state=request.form.get('state')
            lga=request.form.get('lga')
            village=request.form.get('village')
            fos_id=request.form.get('officerid')
            farmsize=request.form.get('farmsize')
            tg=request.form.get('tg')
            verifstatus=request.form.get('verifstatus')
            contract=request.form.get('contract')
            croptype=request.form.get('croptype')

            record= Farmers(fam_fname=fname,fam_surname=surname,fam_lname=othernames,fam_gender=gender,fama_phone=phonenumber,fama_role=role,fama_address=address,fama_state=state,fama_lga=lga,fama_village=village,fo_id=fos_id,con_agreement=contract,fama_crop=croptype,fama_tg=tg,farm_size=farmsize,isverified=verifstatus)
            if record:
                db.session.add(record)
                db.session.commit()
                flash(f"You have signed up {fname} {surname} {othernames} successfully. Well done!")
                return redirect('/fo_dashboard/')
    else:
        return redirect('/login')    
    
            
@app.route('/profile',methods=['POST','GET'])
def profile():
    loggedin = session.get('loggedin')
    if loggedin:
        v=db.session.execute(f"select * from states join fos on states.state_id=fos.fo_state where fos.fo_id={loggedin}")
        j= db.session.execute(f'select * from fos where fos.fo_id="{loggedin}"')
        data=j.fetchone()    
        return render_template('profile.html', data=data,v=v)
    else:
        return redirect('/login')

@app.route('/update/',methods=['POST','GET'])
def update_settings():
    loggedin = session.get('loggedin')
    if loggedin:
        if request.method=="GET":
            states=db.session.query(States).all()
            j= db.session.execute(f'select * from fos where fos.fo_id={loggedin}')
            data=j.fetchone()  
            return render_template('update.html',data=data,states=states)
        else:
            allowed = ['.jpg','.png','.jpeg']
            fileobj=request.files['pix']
            new_file=""
            if fileobj.filename != "":
                original_name=fileobj.filename
                filename,ext = os.path.splitext(original_name)
                if ext.lower() in allowed:
                    xter_list=random.sample(string.ascii_letters,12)
                    new_file="".join(xter_list)+ext
                    fileobj.save(f'pkg/static/uploads/{new_file}')
                else:
                    msg="something went wrong with the file upload"
                    flash(msg)
                    return render_template('update.html',msg=msg)

            fname=request.form.get('fname')
            surname=request.form.get('surname')
            lname=request.form.get('lname')
            phone=request.form.get('phone')
            email=request.form.get('email')
            gender=request.form.get('gender')
            state=request.form.get('state')
            lga=request.form.get('lga')
            village=request.form.get('village')
            cert=request.form.get('cert')
            address=request.form.get('address')
            guaname=request.form.get('guaname')
            guaphone=request.form.get('guaphone')
            guaaddress=request.form.get('guaaddress')
            
            db.session.execute(f" update fos set fo_fname='{fname}',fo_lname='{lname}',fo_surname='{surname}',fo_phone='{phone}',fo_email='{email}',fo_gender='{gender}',fo_state='{state}',fo_lga='{lga}',fo_village='{village}',fo_cert='{cert}',fo_address='{address}',fo_guaname='{guaname}',fo_guaphone='{guaphone}',fo_guaaddress='{guaaddress}',fo_pic='{new_file}' where fo_id='{loggedin}'")
            db.session.commit()
            flash('You have successfully updated your profile')
            return redirect('/profile')
    else:
        return redirect("/login")


@app.route('/logout')
def logout():
    if session.get('loggedin') !=None:
        session.pop('loggedin')
        return redirect("/login")
 
 