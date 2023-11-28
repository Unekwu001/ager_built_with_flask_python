import datetime
from pkg import db
 
class Fos(db.Model): 
    fo_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    fo_fname = db.Column(db.String(100), nullable=False)
    fo_surname = db.Column(db.String(100), nullable=False)
    fo_lname = db.Column(db.String(100), nullable=False)
    fo_gender = db.Column(db.String(100), nullable=False)
    fo_phone = db.Column(db.String(100), nullable=True)
    fo_state = db.Column(db.String(100), nullable=True)
    fo_lga = db.Column(db.String(100), nullable=True)
    fo_village = db.Column(db.String(100), nullable=True)
    fo_email = db.Column(db.String(100), nullable=False)
    fo_pass = db.Column(db.String(255), nullable=False)
    fo_cert = db.Column(db.String(100), nullable=True)
    fo_address = db.Column(db.String(100), nullable=True)
    fo_guaname = db.Column(db.String(100), nullable=True)
    fo_guaphone = db.Column(db.String(100), nullable=True)
    fo_guaaddress = db.Column(db.String(100), nullable=True)
    fo_regdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow())


class Farmers(db.Model): 
    fam_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    fam_fname = db.Column(db.String(100), nullable=False)
    fam_surname = db.Column(db.String(100), nullable=False)
    fam_lname = db.Column(db.String(100), nullable=False)
    fam_gender = db.Column(db.String(50), nullable=False)
    fama_phone = db.Column(db.String(100), nullable=True)
    fama_state = db.Column(db.String(100), nullable=True)
    fama_lga = db.Column(db.String(100), nullable=True)
    fama_village = db.Column(db.String(100), nullable=True)
    fama_address = db.Column(db.String(250), nullable=True)
    fama_tg = db.Column(db.String(100), nullable=True)
    fama_role = db.Column(db.String(50), nullable=True)
    fo_id = db.Column(db.Integer(), nullable=False)
    con_agreement= db.Column(db.String(100), nullable=False)
    fama_crop= db.Column(db.String(20), nullable=False)
    farm_size= db.Column(db.Integer(), nullable=False)
    isverified=db.Column(db.String(20), nullable=False)
    fama_regdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow())



class Lga(db.Model): 
    lga_id = db.Column(db.Integer(), primary_key=True)
    state_id = db.Column(db.Integer(), nullable=False)
    lga_name = db.Column(db.String(100), nullable=False)



class States(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True)
    state_name = db.Column(db.String(20), nullable=False)

class Transaction(db.Model): 
    cus_id = db.Column(db.Integer(), primary_key=True)
    cus_name = db.Column(db.String(100), nullable=True)
    cus_balance= db.Column(db.String(100), nullable=True)
    cus_email = db.Column(db.String(100), nullable=True)
    cus_pwd = db.Column(db.String(100), nullable=True)