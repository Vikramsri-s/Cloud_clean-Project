from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.fernet import Fernet
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from flask import send_file
import numpy as np
import threading
import time
import shutil
import hashlib
import warnings

# Now you can use PendingDeprecationWarning
warnings.filterwarnings("default", category=PendingDeprecationWarning)

import librosa
from pydub import AudioSegment
import wave
from skimage.metrics import structural_similarity

import PyPDF2
#from docx import Documt
from docx import Document
#import tempfile
import fitz

import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="cloud_clean"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    act=request.args.get('act')
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()
    

    return render_template('web/index.html',msg=msg,act=act,data=data)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cu_owner where uname=%s && pass=%s && status=1",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('owner_home')) 
        else:
            msg="Invalid Username or Password!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/login_user',methods=['POST','GET'])
def login_user():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cu_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            msg="Invalid Username or Password!"
        

    return render_template('login_user.html',msg=msg,act=act)

@app.route('/login_csp',methods=['POST','GET'])
def login_csp():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cu_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('csp_home')) 
        else:
            msg="Invalid Username or Password!"
        

    return render_template('login_csp.html',msg=msg,act=act)



@app.route('/register',methods=['POST','GET'])
def register():
    msg=""
    act=""
    email=""
    mess=""
    bdata=""
    bc=""
    uid=""
    mycursor = mydb.cursor()
    
 
    
    if request.method=='POST':
        
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
        uname=request.form['uname']
        pass1=request.form['pass']

        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM cu_owner where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM cu_owner")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            adr=str(uname)
            rn=randint(50,90)
            v1=mobile[0:3]
            v2=str(rn)
            v3=adr[0:2]
            bkey=v3+str(maxid)+v2+v1

            
            uid=str(maxid)
            
            sql = "INSERT INTO cu_owner(id, name, gender, dob, mobile, email, location, uname, pass,rdate,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            val = (maxid, name, gender ,dob, mobile, email, location, uname, pass1,rdate,'0')
            act="success"
            mess="Dear "+name+", Username: "+uname+", Password: "+pass1
            
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            
            msg="success"
            
            #return redirect(url_for('reg',uid=str(maxid))) 
        else:
            msg="fail"
    return render_template('register.html',act=act,msg=msg,email=email,uid=uid)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    uname=""
    msg=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()
    
        
    
    return render_template('reg.html',act=act,data=data,uid=uid)

@app.route('/view_log',methods=['POST','GET'])
def view_log():
    msg=""
    act=""
    data=[]
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM cu_log")
    dat = mycursor.fetchall()
    ts=0
    tn=0
    for ds in dat:
        if ds[1]=='Owner':
            if ds[2]==uname:
                if ds[9]=="":
                    mycursor.execute("update cu_log set owner=%s where id=%s",(uname,ds[0]))
                    mydb.commit()
                    
                data.append(ds)
        if ds[1]=='User':
            mycursor.execute("SELECT count(*) FROM cu_user where uname=%s && owner=%s",(ds[2],uname))
            ds2 = mycursor.fetchone()[0]
            if ds2>0:
                if ds[9]=="":
                    mycursor.execute("update cu_log set owner=%s where id=%s",(uname,ds[0]))
                    mydb.commit()
                    
                data.append(ds)

    ###
    mycursor.execute("SELECT count(*) FROM cu_log where owner=%s && (status='Auto Deleted' or status='File Deleted')",(uname,))
    tot = mycursor.fetchone()[0]
    ####
    mycursor.execute("SELECT sum(tempsize),rdate FROM cu_log where owner=%s group by rdate",(uname,))
    datt = mycursor.fetchall()

    xx=[]
    yy=[]
    for datt1 in datt:
        ts+=datt1[0]
        xx.append(datt1[1])
        yy.append(datt1[0])

    ###
    ts=round(ts,2)
    g2=ts+2
    fig = plt.figure(figsize = (10, 8))

    # creating the bar plot
    plt.bar(xx, yy, width = 0.4)

    plt.ylim((1,g2))

    plt.xlabel("Date")
    plt.ylabel("Temp File Size (KB)")
    plt.title("")


    fn=uname+".png"
    plt.xticks(rotation=20)

    plt.savefig('static/graph/'+fn)
    plt.close()
    ###
    return render_template('view_log.html',msg=msg,act=act,value=value,data=data,ts=ts,tot=tot)


@app.route('/add_user',methods=['POST','GET'])
def add_user():
    msg=""
    act=""
    data=[]
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        user=request.form['uname']
        pass1=request.form['pass']

        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM cu_user where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM cu_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
         
            sql = "INSERT INTO cu_user(id, owner,name, mobile, email, uname, pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,uname, name, mobile, email, user, pass1)
            
            mess="Dear "+name+", Username: "+user+", Password: "+pass1
            
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            
            msg="success"
            
            #return redirect(url_for('reg',uid=str(maxid))) 
        else:
            msg="fail"

    mycursor.execute("SELECT * FROM cu_user where owner=%s",(uname,))
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cu_user where id=%s",(did,))
        mydb.commit()
        msg="ok"
        
    return render_template('add_user.html',act=act,msg=msg,email=email,mess=mess,data=data,value=value)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    uname=""
    msg=""
    st=""
    sdata=[]
    act = request.args.get('act')
    fid = request.args.get('fid')
    view=""
    fname=""
    textpdf=""
    textdoc=""
    ccode=""
    gg=""

    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_user where uname=%s",(uname,))
    value = mycursor.fetchone()

    mycursor.execute("SELECT count(*) FROM cu_share where user=%s",(uname,))
    cnt = mycursor.fetchone()[0]

    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM cu_files f,cu_share s where f.id=s.fid && s.user=%s",(uname,))
        sdata = mycursor.fetchall()

    
    if act=="view":
        mycursor.execute("SELECT * FROM cu_files where id=%s",(fid,))
        data1 = mycursor.fetchone()
        fname=data1[2]

        store_log("User",uname,fid,fname,"File Viewed",'0')

        f1=fname.split(".")
        if f1[1]=="jpg" or f1[1]=="jpeg" or f1[1]=="png":
            view="img"
            if f1[1]=="jpg" or f1[1]=="jpeg":
                gg="img_jpg.jpg"
            elif f1[1]=="png":
                gg="img_png.jpg"
            
        elif f1[1]=="wav" or f1[1]=="mp3":
            view="audio"
            if f1[1]=="wav":
                gg="img_wav.jpg"
            elif f1[1]=="mp3":
                gg="img_mp3.jpg"
                
        elif f1[1]=="mp4" or f1[1]=="avi":
            view="video"
            if f1[1]=="avi":
                gg="img_avi.jpg"
            elif f1[1]=="mp4":
                gg="img_mp4.jpg"
            
        elif f1[1]=="docx":
            view="docx"
            
            gg="img_doc.jpg"
            
            file2="static/upload/"+fname
    
            textdoc = extract_text_from_docx(file2)
    
        elif f1[1]=="pdf":
            view="pdf"
            gg="img_pdf.jpg"
            file2="static/upload/"+fname
            textpdf = extract_text_from_pdf(file2)

    
        else:
            view="text"
            if f1[1]=="txt":
                gg="img_txt.jpg"
            elif f1[1]=="css":
                gg="img_css.jpg"
            elif f1[1]=="html":
                gg="img_html.jpg"
            else:
                gg="img_def.jpg"


                
            file1 = open("static/upload/"+fname, 'r')
            Lines = file1.readlines()
             
            count = 0
            result=""
            # Strips the newline character
            for line in Lines:
                result = "".join(line for line in Lines if not line.isspace())
                count += 1
                #print("Line{}: {}".format(count, line.strip()))
            ccode=result

            
        
    return render_template('userhome.html',act=act,value=value,st=st,sdata=sdata,gg=gg,view=view,ccode=ccode,fname=fname,textpdf=textpdf,textdoc=textdoc)

@app.route('/user_upload', methods=['GET', 'POST'])
def user_upload():
    uname=""
    msg=""
    st=""
    sdata=[]
    act = request.args.get('act')
    fid = request.args.get('fid')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_user where uname=%s",(uname,))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM cu_files where id=%s",(fid,))
    data1 = mycursor.fetchone()
    fname=data1[2]

    if request.method=='POST':

        file = request.files['file']
        
        file_type = file.content_type
        filename = file.filename

        if fname==filename:
            
            os.remove("static/upload/"+fname)
            
            file.save(os.path.join("static/upload", filename))
            filesize1=os.path.getsize("static/upload/"+filename)
            print("fs=")
            print(filesize1)
            uf=float(filesize1)

            fs2=uf/1025
            fs3=fs2/1024
            fs4=round(fs3,3)
            filesize2=fs4

            mycursor.execute("update cu_files set filesize1=%s,filesize2=%s where id=%s",(filesize1,filesize2,fid))
            mydb.commit()
            msg="success"
            store_log("User",uname,fid,filename,"File Update and Uploaded",'0')
        else:
            msg="fail"
    
    
    return render_template('user_upload.html',msg=msg,act=act,value=value,st=st)


def store_log(utype,uname,fid,fname,status,tempsize):
    
    msg=""
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM cu_log")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    sql = "INSERT INTO cu_log(id,utype,uname,fname,fid,status,tempsize,rdate,rtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    val = (maxid,utype,uname,fname,fid,status,tempsize,rdate,rtime)
    act="success"
    mycursor.execute(sql, val)
    mydb.commit()


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    uname=""
    msg=""
    bdata=""
    uid = request.args.get('uid')
    pid = request.args.get('pid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")
    
    if request.method=='POST':        
        card=request.form['card']
        mycursor.execute("update cu_owner set status=1 where id=%s",(uid,))
        mydb.commit()

        mycursor.execute("SELECT * FROM cu_plan where id=%s",(pid,))
        value = mycursor.fetchone()

        mycursor.execute("SELECT * FROM cu_owner where id=%s",(uid,))
        value1 = mycursor.fetchone()
        uname=value1[7]
    
        mycursor.execute("SELECT max(id)+1 FROM cu_storage")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cu_storage(id,uname,pid,storage,stype,price,rdate,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, uname, pid, value[1],value[2],value[3],rdate,'1')
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()

        pid=str(maxid)
        mycursor.execute("update cu_owner set plan_id=%s where id=%s",(pid,uid))
        mydb.commit()
        #pie--appliances
        bval=['Disk Space']

        vv=int(value[1])
        gdata = [vv]
         
        # Creating plot
        colors = ['#66b3ff']
        fig = plt.figure(figsize =(10, 7))
        plt.pie(gdata, labels = bval, colors=colors)
         
        # show plot
        #plt.show()
        
        fn="g"+pid+".png"
        plt.savefig('static/graph/'+fn)
        plt.close()
        
        msg="ok"

       
    return render_template('pay.html',msg=msg,act=act,data=data,uid=uid,pid=pid)


@app.route('/csp_home', methods=['GET', 'POST'])
def csp_home():
    uname=""
    msg=""
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner")
    data = mycursor.fetchall()

    if act=="ok":
        uid = request.args.get('uid')
        mycursor.execute("update cu_owner set status=1 where id=%s", (uid,))
        mydb.commit()
        return redirect(url_for('csp_home')) 
        
    
    return render_template('csp_home.html',act=act,data=data)

@app.route('/csp_server', methods=['GET', 'POST'])
def csp_server():
    uname=""
    msg=""
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_admin")
    value = mycursor.fetchone()

    if request.method=='POST':
        
        status=request.form['status']
        mycursor.execute("update cu_admin set server_st=%s where username='cloud'", (status,))
        mydb.commit()
        return redirect(url_for('csp_server')) 
    
    return render_template('csp_server.html',act=act,value=value)


def calculate_hash(file_path):
    # Calculate the hash value of a file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # Read the file in chunks to avoid loading it entirely into memory
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def hash_difference_percentage(hash1, hash2):
    # Calculate the percentage difference between two hash values
    if len(hash1) != len(hash2):
        raise ValueError("Hash values must have the same length")
    
    difference_count = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
    total_length = len(hash1)
    percentage_difference = (difference_count / total_length) * 100
    return percentage_difference


def sha256_hash(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Read the entire file
            data = file.read()
            # Calculate the SHA-256 hash
            sha256_hash = hashlib.sha256(data).hexdigest()
            return sha256_hash
    except FileNotFoundError:
        print("File not found")
        return None

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = ""
    for para in doc.paragraphs:
        full_text += para.text + "\n"
    return full_text

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def compare_audio(audio_path1, audio_path2):
    # Load audio files
    audio1, sr1 = librosa.load(audio_path1, sr=None)
    audio2, sr2 = librosa.load(audio_path2, sr=None)

    # Resample if sample rates are different
    if sr1 != sr2:
        audio2 = librosa.resample(audio2, sr2, sr1)
        sr2 = sr1

    # Compute waveforms
    waveform1, _ = librosa.effects.trim(audio1)
    waveform2, _ = librosa.effects.trim(audio2)

    # Ensure both waveforms have the same length
    min_length = min(len(waveform1), len(waveform2))
    waveform1 = waveform1[:min_length]
    waveform2 = waveform2[:min_length]

    # Calculate difference between waveforms
    difference = np.abs(waveform1 - waveform2)

    # Calculate percentage difference
    percentage_difference = np.mean(difference) / np.max(np.abs(waveform1)) * 100

    return waveform1, waveform2, percentage_difference



@app.route('/owner_home', methods=['GET', 'POST'])
def owner_home():
    uname=""
    msg=""
    msg2=""
    bdata=""
    bdata2=""
    edd=""
    fid=""
    email=""
    mess=""
    pfile=""
    efile=""
    tsize=0
    dfid=0
    sh=0
    ddata=[]
    act = request.args.get('act')
    fid=request.args.get("fid")
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    
    
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    uid=str(value[0])
    pid=value[11]

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")

    rd=rdate.split("-")
    edd=rd[2]+"-"+rd[1]+"-"+rd[0]
    ################
    mycursor.execute("SELECT * FROM cu_storage where id=%s",(pid,))
    value1 = mycursor.fetchone()

    fn="g"+str(pid)+".png"
    sh=value1[8]
    tsize=value1[3]
    if sh>0:
        pid=value1[8]
    
    used=0
    used1=0
    used2=0
    fnrr=[]
    farr=[]
    colors=[]
    
    mycursor.execute("SELECT count(*) FROM cu_files where uname=%s && pid=%s",(uname,pid))
    cnt1 = mycursor.fetchone()[0]
    if cnt1>0:
        
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where uname=%s && pid=%s",(uname,pid))
        used = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM cu_files where uname=%s && pid=%s",(uname,pid))
        dat1 = mycursor.fetchall()
        i=1
        for ds1 in dat1:
            
            fnrr.append("F"+str(ds1[0]))
            farr.append(ds1[6])
            colors.append("#99ff99")
            '''if ds1[7]>0:
                colors.append("#FF0000")
            else:
                colors.append("#99ff99")'''
            i+=1
    
    if sh==0:
        
        mycursor.execute("SELECT count(*) FROM cu_files where share_st=1 && pid=%s",(pid,))
        cnt1 = mycursor.fetchone()[0]
        if cnt1>0:
            
            mycursor.execute("SELECT sum(filesize2) FROM cu_files where share_st=1 && pid=%s",(pid,))
            used2 = mycursor.fetchone()[0]

            mycursor.execute("SELECT * FROM cu_files where share_st=1 && pid=%s",(pid,))
            dat11 = mycursor.fetchall()
            i=1
            for ds11 in dat11:
                print(ds11)
                fnrr.append("F"+str(ds11[0]))
                farr.append(ds11[6])
                colors.append("#FF0000")

                
                '''if ds11[7]>0:
                    colors.append("#FF0000")
                else:
                    colors.append("#99ff99")'''
                i+=1

            ##
            #bdata2="ID:"+uid+", Data Owner:"+uname+", Attack Disk Space by "+owner+" , Date:"+rdate+", "+rtime
            ##

    print(colors)   
    dsize=tsize-used
    print("used+tsize")
    print(used)
    print(tsize)
    
    ##################
        
    if request.method=='POST':
        
        detail=request.form['detail']
        ehour=request.form['ehour']
        emin=request.form['emin']
        edate=request.form['edate']

        mycursor.execute("SELECT max(id)+1 FROM cu_files")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        fid=str(maxid)            
        
        
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        file_type = file.content_type
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = "F"+str(maxid)+file.filename
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/test", filename))
            filesize1=os.path.getsize("static/test/"+filename)
            print("fs=")
            print(filesize1)
            uf=float(filesize1)

            fs2=uf/1025
            fs3=fs2/1024
            fs4=round(fs3,3)
            filesize2=fs4

            fst1=filename.split(".")
            fst=fst1[1]
            efile=filename

            '''####temp file
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file_path = "static/temp/"+temp_file.name
            
            try:
                # Save the uploaded file to the temporary file
                file.save(temp_file_path)
                # You can now use temp_file_path to access the uploaded file temporarily
                # Do whatever you need to do with the file
                print("Temporary file saved at:", temp_file_path)
            finally:
                temp_file.close()'''
        

            ##Deduplication
            print("xx")
            x=0
            mycursor.execute("SELECT count(*) FROM cu_files where uname=%s",(uname,))
            cn1 = mycursor.fetchone()[0]
            if cn1>0:
                xn=0
                print("aaaa")
                mycursor.execute("SELECT * FROM cu_files where uname=%s",(uname,))
                ds1 = mycursor.fetchall()
                for ds11 in ds1:
                    pfile=ds11[2]
                    df2=pfile.split(".")
                    if fst==df2[1]:
                        xn+=1
                        if fst=="jpg" or fst=="jpeg" or fst=="png":
                            d=1

                            hash1 = calculate_hash("static/upload/"+pfile)
                            hash2 = calculate_hash("static/test/"+efile)

                            percentage_difference = hash_difference_percentage(hash1, hash2)
                            print("img diff")
                            print(percentage_difference)
                            if percentage_difference==0.0:
                                print("duplicate")
                                dfid=ds11[0]
                                x+=1
                            
                        elif fst=="docx":
                            d=1
                            hash1 = calculate_hash("static/upload/"+pfile)
                            hash2 = calculate_hash("static/test/"+efile)

                            percentage_difference = hash_difference_percentage(hash1, hash2)
                            print("docx diff")
                            print(percentage_difference)
                            if percentage_difference==0.0:
                                dfid=ds11[0]
                                x+=1
                            
                        elif fst=="pdf":
                            d=1
                            hash1 = calculate_hash("static/upload/"+pfile)
                            hash2 = calculate_hash("static/test/"+efile)
                            
                            percentage_difference = hash_difference_percentage(hash1, hash2)
                            print("pdf diff")
                            print(percentage_difference)
                            if percentage_difference==0.0:
                                dfid=ds11[0]
                                x+=1
                            
                        elif fst=="wav" or fst=="mp3":
                            d=1
                            
                            res=compare_audio("static/upload/"+pfile,"static/test/"+efile)
                            print("audio per")
                            print(res[2])
                            if res[2]==0.0:
                                dfid=ds11[0]
                                x+=1
                            
                        elif fst=="mp4" or fst=="avi":
                            d=1
                            hash1 = calculate_hash("static/upload/"+pfile)
                            hash2 = calculate_hash("static/test/"+efile)

                            percentage_difference = hash_difference_percentage(hash1, hash2)
                            print(percentage_difference)
                            if percentage_difference==0.0:
                                dfid=ds11[0]
                                x+=1

                        else:
                            print("other")
                            hash1 = calculate_hash("static/upload/"+pfile)
                            hash2 = calculate_hash("static/test/"+efile)

                            percentage_difference = hash_difference_percentage(hash1, hash2)
                            print(percentage_difference)
                            if percentage_difference==0.0:
                                dfid=ds11[0]
                                x+=1
                            
                            
                if xn==0:
                    x=0

            else:
                x=0
            
            ##
            if x==0:
                if dsize>filesize2:

                    shutil.copy("static/test/"+efile,"static/upload/"+efile)

                    os.remove("static/test/"+efile)

                    ##
                    rn=randint(1,6)
                    tp="t"+str(rn)+".temp"
                    tt="t"+str(maxid)+".temp"
                    shutil.copy("static/assets/t1/"+tp,"static/temp/"+tt)

                    tsize1=os.path.getsize("static/temp/"+tt)
                    tsize=tsize1/1024
                    tsize=round(tsize,2)

                    ##
                    
                    print("used1")
                    used1=used+filesize2
                    print(used1)
                    
                    mycursor.execute("update cu_storage set used=%s where id=%s",(used1,pid))
                    mydb.commit()

                    sql = "INSERT INTO cu_files(id, uname,filename,detail,rdate,filesize1,filesize2,pid,share_st,ehour,emin,edate,tsize,rtime) VALUES (%s,%s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
                    val = (maxid, uname, filename, detail, rdate, filesize1,filesize2,pid,sh,ehour,emin,edate,tsize,rtime)
                    act="success"
                    mycursor.execute(sql, val)
                    mydb.commit()

                    store_log("Owner",uname,maxid,filename,"Outsourced Data",'0')
                    store_log("Owner",uname,maxid,tt,"Temp File Created",tsize)

                    gdata=[]
                    bval=[]

                    fnrr.append("Disk Space")
                    bval=fnrr
                    colors.append("#66b3ff")

                    farr.append(dsize)
                    gdata=farr

                    #pie--appliances
                    #bval=['Uploaded File','Available Space']
                     
                    #gdata = [v1,v2]
                     
                    # Creating plot
                    #colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
                    fig = plt.figure(figsize =(10, 7))
                    plt.pie(gdata, labels = bval, colors=colors)
                     
                    # show plot
                    #plt.show()
                    fn="g"+str(pid)+".png"
                    plt.savefig('static/graph/'+fn)
                    plt.close()

                    msg="success"
                    
                else:
                    msg="fail"
            
            else:
                msg="duplicate"
                mycursor.execute("SELECT * FROM cu_files where id=%s",(dfid,))
                ddata = mycursor.fetchone()

                store_log("Owner",uname,dfid,ddata[2],"Deduplication Detected",'0')
                
                
            #return redirect(url_for('owner_home',act=act))

    mycursor.execute("SELECT * FROM cu_files where uname=%s",(uname,))
    data = mycursor.fetchall()
    
    return render_template('owner_home.html',msg=msg,value=value,act=act,data=data,fn=fn,msg2=msg2,mess=mess,email=email,edd=edd,tsize=tsize,fid=fid,ddata=ddata)


@app.route('/page1', methods=['GET', 'POST'])
def page1():
    msg=""
    fid=request.args.get("fid")
    act=request.args.get("act")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_files where id=%s",(fid,))
    value = mycursor.fetchone()

    if act=="2":
        print("remove temp")
        tfile="t"+fid+".temp"
        os.remove("static/temp/"+tfile)
    
    

    return render_template('page1.html',msg=msg,act=act,fid=fid,value=value)


#RegEX Algortihm - Automated Cleanup
class RegEx:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_end = True
    
    def addstate(self, state, state_set): # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)
    
    def pretty_print(self):
        '''
        print using Graphviz
        '''
        pass
    
    def match(self,s):
        current_states = set()
        self.addstate(self.start, current_states)
        
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
           
            current_states = next_states

        for s in current_states:
            if s.is_end:
                return True
        return False


    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))
    
    def handle_char(self, t, nfa_stack):
        s0 = self.create_state()
        s1 = self.create_state()
        s0.transitions[t.value] = s1
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)
    
    def handle_concat(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        n1.end.is_end = False
        n1.end.epsilon.append(n2.start)
        nfa = NFA(n1.start, n2.end)
        nfa_stack.append(nfa)
    
    def handle_alt(self, t, nfa_stack):
        n2 = nfa_stack.pop()
        n1 = nfa_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [n1.start, n2.start]
        s3 = self.create_state()
        n1.end.epsilon.append(s3)
        n2.end.epsilon.append(s3)
        n1.end.is_end = False
        n2.end.is_end = False
        nfa = NFA(s0, s3)
        nfa_stack.append(nfa)
  
    
    def print_tokens(tokens):
        for t in tokens:
            print(t)

        lexer = Lexer(p)
        parser = Parser(lexer)
        tokens = parser.parse()

        handler = Handler()
        
        if debug:
            print_tokens(tokens) 

        nfa_stack = []
        
        for t in tokens:
            handler.handlers[t.name](t, nfa_stack)
        
        assert len(nfa_stack) == 1
        return nfa_stack.pop() 
###

@app.route('/expire_time', methods=['GET', 'POST'])
def expire_time():
    msg=""
    st=""
    name=""
    mobile=""
    email=""
    mess=""
    mess1=""
    act=request.args.get("act")

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")

    rh=now.strftime("%H")
    rm=now.strftime("%M")

    rh=int(rh)
    rm=int(rm)

    rd=rdate.split("-")
    edd=rd[2]+"-"+rd[1]+"-"+rd[0]

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_files where edate=%s",(edd,))
    dat = mycursor.fetchall()

    for dat1 in dat:
        edate=dat1[13]
        eh=dat1[11]
        em=dat1[12]
        
        print(dat1[2])

        print(rh)
        print(rm)
        print(eh)
        print(em)

        if rh==eh:
            if rm<em:
            
                t=em-5
                if rm>=t:
                    if dat1[15]==0:
                        st="1"
                        print("sms")
                        uu=dat1[1]

                        mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uu,))
                        dat2 = mycursor.fetchone()
                        mobile=dat2[4]
                        email=dat2[5]
                        name=dat2[1]

                        print(mobile)
                        print(email)

                        mess="File: "+dat1[2]+", File will be Deleted"
                        mess1="Dear "+name+", File:"+dat1[2]+", File will be Deleted within 5 minutes"
                        print(mess)
                        print(mess1)

                        mycursor.execute("update cu_files set sms_st=1 where id=%s",(dat1[0],))
                        mydb.commit()
                        break
            
            if rm>=em:

                fname=dat1[2]
                store_log("Owner",dat1[1],dat1[0],fname,"Auto Deleted",'0')
                
                os.remove("static/upload/"+fname)

                mycursor.execute("delete from cu_share where fid=%s",(dat1[0],))
                mydb.commit()
                mycursor.execute("delete from cu_files where id=%s",(dat1[0],))
                mydb.commit()
                
                print("deleted")

        if rh>eh:
            fname=dat1[2]

            store_log("Owner",dat1[1],dat1[0],fname,"Auto Deleted",'0')
            
            os.remove("static/upload/"+fname)

            mycursor.execute("delete from cu_share where fid=%s",(dat1[0],))
            mydb.commit()
            mycursor.execute("delete from cu_files where id=%s",(dat1[0],))
            mydb.commit()
            
            print("deleted..")
                
        

    return render_template('expire_time.html',msg=msg,act=act,name=name,mobile=mobile,email=email,mess=mess,mess1=mess1,st=st)

def getDays(date1,date2):
    from datetime import datetime

    sd=date1.split("-")
    sd1=int(sd[0])
    sd2=int(sd[1])
    sd3=int(sd[2])

    ed=date2.split("-")
    ed1=int(ed[0])
    ed2=int(ed[1])
    ed3=int(ed[2])

    date1 = datetime(sd1, sd2, sd3)  # Start date
    date2 = datetime(ed1, ed2, ed3)    # End date
    difference = date2 - date1
    num_days = difference.days
    return num_days


@app.route('/view_files', methods=['GET', 'POST'])
def view_files():
    act=request.args.get("act")
    fid=request.args.get("fid")
    uname=""
    msg=""
    attk=0
    per=0
    used=0
    data=[]
    view=""
    fname=""
    textpdf=""
    textdoc=""
    ccode=""
    gg=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    pid=str(value[11])

    mycursor.execute("SELECT * FROM cu_storage where id=%s",(pid,))
    value1 = mycursor.fetchone()
    
    tsize=value1[3]

    used=0
    used2=0
    used3=0

    mycursor.execute("SELECT count(*) FROM cu_files where uname=%s && pid=%s",(uname,pid))
    cn1 = mycursor.fetchone()[0]
    if cn1>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where uname=%s && pid=%s",(uname,pid))
        used = mycursor.fetchone()[0]

    mycursor.execute("SELECT count(*) FROM cu_files where share_st=1 && pid=%s",(pid,))
    cn1 = mycursor.fetchone()[0]
    if cn1>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where share_st=1 && pid=%s",(pid,))
        used2 = mycursor.fetchone()[0]

    if used2>0:
        used3=used+used2
    else:
        used3=used

    if used3>0:
        pp=(used3/tsize)*100
        per=round(pp,2)
    else:
        pp=(used/tsize)*100
        per=round(pp,2)
        

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")
    rdt=now.strftime("%Y-%m-%d")
    
    rtt=rtime.split("-")
    rh=int(rtt[0])
    rm=int(rtt[1])
    
    
    mycursor.execute("SELECT count(*) FROM cu_files where  share_st=1 && pid=%s",(pid,))
    cn = mycursor.fetchone()[0]
    if cn>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where pid=%s && share_st=1",(pid,))
        attk = mycursor.fetchone()[0]

    ##########
    
        
    mycursor.execute("SELECT * FROM cu_files where uname=%s order by id desc",(uname,))
    dw = mycursor.fetchall()

    for dw1 in dw:
        dt=[]
        dt.append(dw1[0])
        dt.append(dw1[1])
        dt.append(dw1[2])
        dt.append(dw1[3])
        dt.append(dw1[4])
        dt.append(dw1[5])
        dt.append(dw1[6])
        dt.append(dw1[7])
        dt.append(dw1[8])
        dt.append(dw1[9])
        dt.append(dw1[10])
        dt.append(dw1[11])
        dt.append(dw1[12])
        dt.append(dw1[13])
        dt.append(dw1[14])
        dt.append(dw1[15])
        dt.append(dw1[16])


        ms=""
        vs=""
        if rdt==dw1[13]:
            eh=dw1[11]
            em=dw1[12]
            hh=eh-rh
            vs="1"
            if rh==eh:
                mm=em-rm
                ms=str(hh)+" hour(s) "+str(mm)+" minutes remaining"
            else:
                ms=str(hh)+" hour(s) remaining"
        else:
            vs="2"
            num_days=getDays(rdt,dw1[13])
            ms=str(num_days)+" day(s) remaining"
        dt.append(ms)
        dt.append(vs)

        
        data.append(dt)
        

    
    ##########
    if act=="del":
        did=request.args.get("did")

        mycursor.execute("SELECT * FROM cu_files where id=%s",(did,))
        dd = mycursor.fetchone()
    
        store_log("Owner",uname,did,dd[2],"File Deleted",'0')
        
        mycursor.execute("delete from cu_files where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_files'))


    ###Total size and amount
    totmb=0
    pay_amt=0
    tempsize=0
    temps=""
    mycursor.execute("SELECT count(*) FROM cu_files where uname=%s",(uname,))
    pn1 = mycursor.fetchone()[0]
    if pn1>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where uname=%s",(uname,))
        totmb = mycursor.fetchone()[0]
        used=totmb
        pamt=totmb*10
        pay_amt=round(pamt,2)

        mycursor.execute("SELECT sum(tsize) FROM cu_files where uname=%s",(uname,))
        tss = mycursor.fetchone()[0]
        tempsize=tss/1024
        tempsize=round(tempsize,2)

        if tempsize<1:
            temps=str(tss)+" KB"
        else:
            temps=str(tempsize)+" MB"
        
    if act=="view":
        mycursor.execute("SELECT * FROM cu_files where id=%s",(fid,))
        data1 = mycursor.fetchone()
        fname=data1[2]

        store_log("Owner",uname,fid,fname,"File Viewed",'0')

        f1=fname.split(".")
        if f1[1]=="jpg" or f1[1]=="jpeg" or f1[1]=="png":
            view="img"
            if f1[1]=="jpg" or f1[1]=="jpeg":
                gg="img_jpg.jpg"
            elif f1[1]=="png":
                gg="img_png.jpg"
            
        elif f1[1]=="wav" or f1[1]=="mp3":
            view="audio"
            if f1[1]=="wav":
                gg="img_wav.jpg"
            elif f1[1]=="mp3":
                gg="img_mp3.jpg"
                
        elif f1[1]=="mp4" or f1[1]=="avi":
            view="video"
            if f1[1]=="avi":
                gg="img_avi.jpg"
            elif f1[1]=="mp4":
                gg="img_mp4.jpg"
            
        elif f1[1]=="docx":
            view="docx"
            
            gg="img_doc.jpg"
            
            file2="static/upload/"+fname
    
            textdoc = extract_text_from_docx(file2)
    
        elif f1[1]=="pdf":
            view="pdf"
            gg="img_pdf.jpg"
            file2="static/upload/"+fname
            textpdf = extract_text_from_pdf(file2)

    
        else:
            view="text"
            if f1[1]=="txt":
                gg="img_txt.jpg"
            elif f1[1]=="css":
                gg="img_css.jpg"
            elif f1[1]=="html":
                gg="img_html.jpg"
            else:
                gg="img_def.jpg"


                
            file1 = open("static/upload/"+fname, 'r')
            Lines = file1.readlines()
             
            count = 0
            result=""
            # Strips the newline character
            for line in Lines:
                result = "".join(line for line in Lines if not line.isspace())
                count += 1
                #print("Line{}: {}".format(count, line.strip()))
            ccode=result



    return render_template('view_files.html',value=value,act=act,data=data,tsize=tsize,used=used,attk=attk,per=per,temps=temps,gg=gg,view=view,ccode=ccode,fname=fname,textpdf=textpdf,textdoc=textdoc)


@app.route('/share', methods=['GET', 'POST'])
def share():
    msg=""
    act=request.args.get("act")
    fid=request.args.get("fid")
    uname=""
    msg=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM cu_files where id=%s",(fid,))
    data = mycursor.fetchone()
    fname=data[2]

    mycursor.execute("SELECT * FROM cu_user where owner=%s",(uname,))
    udata = mycursor.fetchall()

    s1="0"
    s2="0"
    s3="0"
    if request.method=='POST':
        
        user=request.form['user']
        ch=request.form['ch']
        #ch=request.form.getlist('ch[]')
        print(ch)
        l=len(ch)
        '''if l==1:
            if ch[0]=="1":
                s1="1"
            elif ch[0]=="2":
                s2="1"
            elif ch[0]=="3":
                s3="1"
        elif l==2:
            if ch[0]=="1":
                s1="1"
            if ch[1]=="2":
                s2="1"
            if ch[0]=="2":
                s2="1"
            if ch[1]=="3":
                s3="1"
        elif l==3:            
            s1="1"           
            s2="1"           
            s3="1"'''
                
  
        mycursor.execute('SELECT count(*) FROM cu_share WHERE user=%s && fid=%s', (user,fid))
        c1 = mycursor.fetchone()[0]
        if c1==0:

            mycursor.execute("SELECT max(id)+1 FROM cu_share")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO cu_share(id,owner,user,fid,view_st) VALUES (%s,%s,%s,%s,%s)"
            val = (maxid,uname,user,fid,ch)
            mycursor.execute(sql, val)
            mydb.commit()

            
        else:
            mycursor.execute("update cu_share set view_st=%s where user=%s && fid=%s", (ch,user,fid))
            mydb.commit()
           
        store_log("Owner",uname,fid,fname,"Shared to "+user,'0')
        msg="share"

    mycursor.execute("SELECT * FROM cu_share where owner=%s && fid=%s",(uname,fid))
    sdata = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")

        mycursor.execute('SELECT * FROM cu_share WHERE id=%s', (did,))
        dd = mycursor.fetchone()

        mycursor.execute('SELECT * FROM cu_files WHERE id=%s', (dd[3],))
        dd2 = mycursor.fetchone()
        
        store_log("Owner",uname,did,dd2[2],"Share Removed in "+dd[2],'0')
        mycursor.execute("delete from cu_share where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('share',fid=fid)) 
        
    
    return render_template('share.html',msg=msg,value=value,act=act,data=data,fid=fid,udata=udata,sdata=sdata)


@app.route('/view_store', methods=['GET', 'POST'])
def view_store():
    uname=""
    msg=""
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        
        space=request.form['space']
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        
        mycursor.execute("SELECT max(id)+1 FROM cu_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        sql = "INSERT INTO cu_request(id,uname,space,rdate,status) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid, uname,space,rdate,'0')
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()            
        msg="ok"

    mycursor.execute("SELECT * FROM cu_storage where uname=%s",(uname,))
    data = mycursor.fetchall()
    
    return render_template('view_store.html',value=value,act=act,data=data)






@app.route('/reg1', methods=['GET', 'POST'])
def reg1():
    uname=""
    msg=""
    uid = request.args.get('uid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()

    
    
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()
    
    return render_template('reg1.html',msg=msg,value=value,act=act,data=data,uid=uid)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    uname=""
    msg=""
    mess=""
    email=""
    pid = request.args.get('pid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    email=value[5]
    uid=str(value[0])
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")

    ###Total size and amount
    totmb=0
    pay_amt=0
    mycursor.execute("SELECT count(*) FROM cu_files where uname=%s && pay_st=0",(uname,))
    pn1 = mycursor.fetchone()[0]
    if pn1>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where uname=%s && pay_st=0",(uname,))
        totmb = mycursor.fetchone()[0]

        pamt=totmb*10
        pay_amt=round(pamt,2)
    
    if request.method=='POST':        
        card=request.form['card']

    
        mycursor.execute("SELECT max(id)+1 FROM cu_payment")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cu_payment(id,uname,total_size,amount,rdate,rtime) VALUES (%s, %s, %s, %s,%s,%s)"
        val = (maxid, uname, totmb, pay_amt,rdate,rtime)
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()

        mycursor.execute("update cu_files set pid=%s,pay_st=1 where uname=%s && pay_st=0",(maxid,uname))
        mydb.commit()

        msg="ok"
        ##
        bdata="ID:"+str(maxid)+", Data Owner:"+uname+", Disk Space Request: "+str(value[1])+" MB , Date:"+rdate+", "+rtime
        ##
        mess="Dear "+uname+", Amount Paid: Rs."+str(pay_amt)+", Total File Size: "+str(totmb)+" MB"
    
    return render_template('payment.html',msg=msg,value=value,act=act,data=data,uid=uid,pid=pid,pay_amt=pay_amt,mess=mess,email=email)

@app.route('/view_payment', methods=['GET', 'POST'])
def view_payment():
    uname=""
    msg=""
    mess=""
    per=0
    tsize=0
    used=0
    email=""
    pid = request.args.get('pid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    uid=str(value[0])
    pid=str(value[11])
    mycursor.execute("SELECT * FROM cu_payment where uname=%s",(uname,))
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM cu_storage where id=%s",(pid,))
    value1 = mycursor.fetchone()
    
    tsize=value1[3]

    ###Total size and amount
    totmb=0
    pay_amt=0
    mycursor.execute("SELECT count(*) FROM cu_files where uname=%s && pay_st=0",(uname,))
    pn1 = mycursor.fetchone()[0]
    if pn1>0:
        mycursor.execute("SELECT sum(filesize2) FROM cu_files where uname=%s && pay_st=0",(uname,))
        totmb = mycursor.fetchone()[0]
        used=totmb
        pamt=totmb*10
        pay_amt=round(pamt,2)
    


    return render_template('view_payment.html',msg=msg,value=value,act=act,data=data,per=per,tsize=tsize,used=used)


@app.route('/pay1', methods=['GET', 'POST'])
def pay1():
    uname=""
    msg=""
    mess=""
    email=""
    pid = request.args.get('pid')
    act = request.args.get('act')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    value = mycursor.fetchone()
    uid=str(value[0])
    mycursor.execute("SELECT * FROM cu_plan")
    data = mycursor.fetchall()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H-%M-%S")
    
    if request.method=='POST':        
        card=request.form['card']
        mycursor.execute("update cu_owner set status=1 where id=%s",(uid,))
        mydb.commit()

        mycursor.execute("SELECT * FROM cu_plan where id=%s",(pid,))
        value = mycursor.fetchone()

        mycursor.execute("SELECT * FROM cu_owner where id=%s",(uid,))
        value1 = mycursor.fetchone()
        uname=value1[7]
    
        mycursor.execute("SELECT max(id)+1 FROM cu_storage")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cu_storage(id,uname,pid,storage,stype,price,rdate,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        val = (maxid, uname, pid, value[1],value[2],value[3],rdate,'0')
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()

        msg="ok"
        ##
        bdata="ID:"+str(maxid)+", Data Owner:"+uname+", Disk Space Request: "+str(value[1])+" MB , Date:"+rdate+", "+rtime
        ##
        
    
    return render_template('pay1.html',msg=msg,value=value,act=act,data=data,uid=uid,pid=pid)


@app.route('/csp_req', methods=['GET', 'POST'])
def csp_req():
    act=request.args.get("act")
    uname=""
    msg=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_storage where status=0")
    data = mycursor.fetchall()
   


    return render_template('csp_req.html',msg=msg,act=act,data=data)

@app.route('/csp_allot', methods=['GET', 'POST'])
def csp_allot():
    act=request.args.get("act")
    rid=request.args.get("rid")
    sid=request.args.get("sid")
    uname=""
    msg=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_storage where status=1")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM cu_storage where status=1")
    data = mycursor.fetchall()

 
    if act=="share":
        mycursor.execute("SELECT * FROM cu_storage where id=%s",(rid,))
        dd = mycursor.fetchone()
        user=dd[1]
    
        mycursor.execute("update cu_storage set share=%s,status=1 where id=%s",(sid,rid))
        mydb.commit()

        mycursor.execute("update cu_owner set plan_id=%s where uname=%s",(rid,user))
        mydb.commit()
        
        msg="ok"
    if act=="yes":
        mycursor.execute("SELECT * FROM cu_storage where id=%s",(rid,))
        dd = mycursor.fetchone()
        user=dd[1]
        
        mycursor.execute("update cu_storage set status=1 where id=%s",(rid,))
        mydb.commit()

        mycursor.execute("update cu_owner set plan_id=%s where uname=%s",(rid,user))
        mydb.commit()
        msg="ok"
   


    return render_template('csp_allot.html',msg=msg,act=act,data=data,rid=rid)

@app.route('/csp_view', methods=['GET', 'POST'])
def csp_view():
    act=request.args.get("act")
    
    uname=""
    msg=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_storage where status=1")
    data = mycursor.fetchall()

 

    return render_template('csp_view.html',msg=msg,act=act,data=data)

@app.route('/view_block', methods=['GET', 'POST'])
def view_block():
    msg=""
    cnt=0
    uname=""
    mess=""
    data2=[]
    act=request.args.get("act")
    st=""
    pmode=""
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cu_owner where uname=%s",(uname,))
    data = mycursor.fetchone()
    vid=data[0]
    key=data[12]

 
    
    return render_template('view_block.html',msg=msg,data=data,mess=mess,act=act,uname=uname,key=key)


@app.route('/down', methods=['GET', 'POST'])
def down():
    fname = request.args.get('fname')
    utype = request.args.get('utype')
    uname = request.args.get('uname')
    fid = request.args.get('fid')

    store_log(utype,uname,fid,fname,"File Downloaded",'0')
    
    path="static/upload/"+fname
    return send_file(path, as_attachment=True)



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
