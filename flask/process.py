from flask import Flask, render_template, request
from flask import send_file
import subprocess
import pexpect
import sys
from multiprocessing import Value
import netmiko
from netmiko import ConnectHandler
import flask_monitoringdashboard as dashboard



counter = Value("i",0)
app = Flask(__name__)
dashboard.bind(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/')
def home():
    return render_template('home1.html')



@app.route('/genie')
def genie():
    output = ''
    return render_template('genie.html', len = len(output))

@app.route('/genie', methods=['POST'])


def genie_form():
    name = request.form['name']
    nodeip = request.form['nodeip']
    uname = request.form['username']
#    pword = request.form['pword']
    action = request.form['action']
    feature = request.form['feature']
    result = 'wonderful'
    folderName = uname+ "_"  + name

    pobj = pexpect.spawn('/bin/bash', timeout=120)

    if "precheck" in action:
        fout = open('static/genieprecheck.txt', 'w')
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect(['#'])
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#')
        pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName)
        pobj.expect('#')
        pobj.sendline("kill $(ps aux | grep 9888 | awk '{print $2}');kill $(ps aux | grep 9887 | awk '{print $2}');kill $(ps aux | grep 9888 | awk '{print $2}')")
        pobj.expect('#')
        pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/precheck")
        pobj.expect('#')
        pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/precheck")
        pobj.expect('#')
        pobj.sendline("python3.4 -m http.server 9887 &> /dev/null & pid=$!")
        pobj.expect('#')
        # pobj.sendline("cd /data/SunilB/genie/test/precheck/")
        # pobj.expect(['#'])
        # pobj.sendline("rm -rf *")
        # pobj.expect(['#'])
        # pobj.sendline("cd /data/SunilB/genie/test/postcheck/")
        # pobj.expect(['#'])
        pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/postcheck")
        pobj.expect('#')
        pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/postcheck")
        pobj.expect('#')
        pobj.sendline("python3.4 -m http.server 9888 &> /dev/null & pid=$!")
        pobj.expect('#')
        #pobj.sendline("rm -rf *")
        #pobj.expect(['#'])
        # pobj.sendline("cd /data/SunilB/genie/test/diff/")
        # pobj.expect(['#'])
        pobj.sendline("mkdir /data/SunilB/genie/test/"+folderName+"/diff")
        pobj.expect('#')
        pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/diff")
        pobj.expect('#')
        pobj.sendline("python3.4 -m http.server 9889 &> /dev/null & pid=$!")
        pobj.expect('#')
        # pobj.sendline("rm -rf *")
        # pobj.expect(['#'])
        pobj.sendline("cd /data/SunilB/genie/test/")
        pobj.expect(['#'])
        pobj.sendline("python genie_builder.py "+folderName+" "+nodeip)
        pobj.expect(['#'])
        fout = open('static/genieprecheck.txt', 'w')
        pobj.logfile = fout.buffer
        pobj.sendline("genie learn " +feature+" --testbed "+name+".yaml --output "+folderName+"/precheck/")
        pobj.expect(['#', pexpect.TIMEOUT])
        pobj.close()
        fin = open("static/genieprecheck.txt", "r")
        value1 = fin.read()
        with counter.get_lock():
            counter.value +=1
        fin.close()
        result1 = 'c'
        return render_template('pass.html', result=value1)
    
    elif "postcheck" in action:
        fout = open('static/geniepostcheck.txt', 'w')
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect('#')
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#')
        pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/")
        pobj.expect('#')
        pobj.logfile = fout.buffer
        pobj.sendline("genie learn " +feature+" --testbed "+name+".yaml --output postcheck/")
        pobj.expect(['#', pexpect.TIMEOUT])
        fin = open("static/geniepostcheck.txt", "r")
        value1 = fin.read()
        with counter.get_lock():
            counter.value +=1
        fin.close()
        result1 = 'c'
        return render_template('pass.html', result=value1)

    elif "diff" in action:

        fout = open('static/diff.txt', 'w')
        pobj.expect('$', timeout=10)
        pobj.sendline("sudo su root")
        pobj.expect('mpls', timeout=10)
        pobj.sendline("Airtel@123")
        pobj.expect('#')
        pobj.sendline("source /data/SunilB/genie/bin/activate")
        pobj.expect('#')
        pobj.sendline("cd /data/SunilB/genie/test/"+folderName+"/")
        pobj.expect('#')
        pobj.logfile = fout.buffer
        pobj.sendline("genie diff precheck postcheck --output diff/")
        pobj.expect(['#', pexpect.TIMEOUT])
        fin = open("static/diff.txt", "r")
        value1 = fin.read()
        with counter.get_lock():
            counter.value +=1
        fin.close()
        result1 = 'c'
        return render_template('pass.html', result=value1)


@app.route('/about/')
def about():
    output = ''
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

@app.route('/kpi-utility/')
def kpi():
    output = ''
    return render_template('kpi.html',len = len(output))

@app.route('/kpi-1') # this is a job for GET, not POST
def kpi_1():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-1.csv',mimetype='text/csv',attachment_filename='ISIS_LDP_Missing_Report.csv',as_attachment=True)

@app.route('/kpi-2') # this is a job for GET, not POST
def kpi_2():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-2.csv',mimetype='text/csv',attachment_filename='ISIS_IPv6_Missing_Report.csv',as_attachment=True)

@app.route('/kpi-3') # this is a job for GET, not POST
def kpi_3():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-3.csv',mimetype='text/csv',attachment_filename='Description_Deviation_Backbone_Report.csv',as_attachment=True)

@app.route('/kpi-4') # this is a job for GET, not POST
def kpi_4():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-4.csv',mimetype='text/csv',attachment_filename='ISIS_Metric_B2B_Deviation_Report.csv',as_attachment=True)

@app.route('/kpi-5') # this is a job for GET, not POST
def kpi_5():
    return send_file('/home/Python_Tool/Auto_Scripts/KPI-Files/kpi-5.csv',mimetype='text/csv',attachment_filename='ISIS_Metric_Deviation_10G_Report.csv',as_attachment=True)

if __name__ == '__main__':
    app.run(use_reloader= True,debug=True,host='0.0.0.0', port=8011)
