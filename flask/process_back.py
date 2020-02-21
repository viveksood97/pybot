from flask import Flask, render_template, request
import subprocess
import pexpect
import sys
from multiprocessing import Value
counter = Value("i",0)
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('layout.html')
@app.route('/genie')
def genie():
    output = ''
    return render_template('genie.html', len = len(output))

@app.route('/genie', methods=['POST'])
def genie_form():
    hostname = request.form['hostname']
    nodeip = request.form['nodeip']
    action = request.form['action']
    user = request.form['user']
    passw = request.form['pass']
    feature = request.form['feature']
    if "precheck" in action:
        
        pobj = pexpect.spawn ('/bin/bash')
        pobj.setwinsize(400,400)
        fout = open('static/genieprecheck.txt', 'w')
        fout.close()
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect('#',timeout=10)
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#', timeout=10)
        pobj.sendline("cd /data/SunilB/genie/test/")
        pobj.expect('#', timeout=10)
        pobj.sendline("rm -rf * precheck/")
        pobj.expect('#', timeout=10)
        pobj.sendline("rm -rf * postcheck/")
        pobj.expect('#', timeout=10)
        pobj.sendline("rm -rf * diff/")
        pobj.expect('#', timeout=10)
        pobj.sendline("python bgp_builder.py hostname nodeip user passw")
        pobj.expect('#', timeout=10)
        pobj.logfile = fout.buffer
        pobj.sendline("genie learn " +feature+" --testbed rtest.yaml --output precheck/")
        pobj.expect('#', timeout=300)


        fin = open("static/genieprecheck.txt", "r")
        contents = []
        value1 = fin.read()

        pobj.close()
        with counter.get_lock():
            counter.value +=1

        fin.close()


        return render_template('pass.html')
    
    elif "postcheck" in action:

        pobj = pexpect.spawn ('/bin/bash')
        pobj.setwinsize(400,400)
        fout = open('static/geniepostcheck.txt', 'w')
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect('#',timeout=10)
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#', timeout=10)
        pobj.sendline("cd /data/SunilB/genie/test/")
        pobj.expect('#', timeout=10)
        pobj.logfile = fout.buffer
        pobj.sendline("genie learn " +feature+" --testbed rtest.yaml --output postcheck/")
        pobj.expect('#', timeout=300)


        fin = open("static/genieprecheck.txt", "r")
        contents = []
        value1 = fin.read()

        pobj.close()
        with counter.get_lock():
            counter.value +=1

        fin.close()


        return render_template('pass.html')

    elif "diff" in action:

        pobj = pexpect.spawn ('/bin/bash')
        pobj.setwinsize(400,400)
        fout = open('static/geniediff.txt', 'w')
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect('#',timeout=10)
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#', timeout=10)
        pobj.sendline("cd /data/SunilB/genie/test/")
        pobj.expect('#', timeout=10)
        pobj.logfile = fout.buffer
        pobj.sendline("genie diff precheck postcheck")
        pobj.expect('#', timeout=300)

        fin = open("static/genieprecheck.txt", "r")
        contents = []
        value1 = fin.read()

        pobj.close()
        with counter.get_lock():
            counter.value +=1

        fin.close()


        return render_template('pass.html')    



@app.route('/about/')
def about():
    output = ''
    
    # # input1  = request.form['data_array']
    # # print(input1)
    # pobj = pexpect.spawn ('/bin/bash', maxread=100000000)
    
    # pobj.sendline("python test.py")
    # pobj.expect("Enter Ip address to ping")
    # # a = 10
    # pobj.sendline("8.8.8.8")
    
    # # pobj.sendline()
    
    # pobj.expect('end')
    # #
    # # pobj.expect('[root@localhost test2]#')
    
    # output = pobj.before.decode()
    # output = output.split(" ", 2)
    
    # pobj.close()
    
    # # output = subprocess.check_output(["test.py", str(a)], shell = True).decode('UTF-8')
    # #print(output)
    return render_template('home.html', len = len(output))
@app.route('/about/', methods=['POST'])
def about_form():   
    username = request.form['form']
    password = request.form['form1']
    Source_IP = request.form['form2']
    Destination_IP = request.form['form3']
    ping_count = request.form['form4']
   # print(input2)
    # input1  = request.form['data_array']
    # print(input1)
    pobj = pexpect.spawn ('/bin/bash')
    pobj.setwinsize(400,400)
    fout = open('static/mylog.txt', 'w')
    
    #result = StringIO() 
    #sys.stdout = result 

    pobj.expect('$', timeout=10)
    pobj.sendline("sudo su root")
    pobj.expect('mpls', timeout=10)
    pobj.sendline("Airtel@123")
    pobj.expect('#',timeout=10)
    pobj.sendline("cd /root/ts")
    pobj.expect('#', timeout=10)
    
    pobj.sendline("python3.4 Route_Analyser.py")
   
    pobj.expect("username")
    pobj.sendline(username)
    while True:		
        try:
            pobj.expect("Password", timeout=1)
            pobj.sendline(password)
            break
        except pexpect.TIMEOUT:
            value2 = 'Error: Password is a mandatory field'
            return render_template('home.html', value2 = value2) 
    pobj.logfile = fout.buffer
    pobj.expect("Enter Source IP", timeout=10)
    pobj.sendline(Source_IP)
    pobj.expect("Enter Destination IP", timeout=10)
    pobj.sendline(Destination_IP)
    
    pobj.expect("Input ping repeat count", timeout=10)
    pobj.sendline(ping_count)
    

    
    pobj.expect('root@', timeout=600)
   
    
    
    #output = result.getvalue().decode
    fin = open("static/mylog.txt", "r")
    contents = []
    value1 = fin.read()

    pobj.close()
    with counter.get_lock():
        counter.value +=1
    
    fin.close()
    #print(result.getvalue())
    #pobj.close()
    
    # output = subprocess.check_output(["test.py", str(a)], shell = True).decode('UTF-8')
    #print(output)
    return render_template('home.html', len = len(contents), value = value1, value1 = counter.value)
if __name__ == '__main__':
    app.run(use_reloader= True,debug=True,host='172.30.1.129', port=9011)
