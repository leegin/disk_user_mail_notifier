#!/usr/bin/python
import os
import socket
import smtplib
import MySQLdb

def get_total_size(pathname):
    """Return total size of file/directory
    input: path to a directory or file
    outpt: total size in MiB
    """
    try:
        size_bytes = 0
        if not os.path.isdir(pathname):
            size_bytes = os.path.getsize(pathname)
        else:
            for root, dirs, files in os.walk(pathname):
                for file in files:
                    size_bytes += os.path.getsize(os.path.join(root, file))
        return size_bytes/(1024*1024)
    except OSError:
        pass

def get_home_usage(home_dir = '/home'):
    """Return a dictionary containing all home dirs and correponding size in MiB"""
    all_home = {}
    for home in os.listdir(home_dir):
        all_home[home] = get_total_size(os.path.join(home_dir, home))
    return all_home

def send_mail(username):
        # The folder containing files.
        directory = "/home/"+username

"""Get all files under the directory."""
        list1 = os.listdir(directory)
"""Loop and add files to list"""
        pairs = {}
        for file in list1:

        # Use join to get full file path.
                location = os.path.join(directory, file)

        # Get size and add to list of tuples.
                size = os.path.getsize(location)
                out = size/(1024*1024)
                pairs[file] = out

"""Sort list of tuples by the first element, size."""
        pairs = sorted(pairs.items(), key=lambda kv: kv[1], reverse=True)
        host = socket.gethostname()

        IP = "<HOST_IP>"
        user = "<USER>"
        password = "<PASSWORD>"
        db = "<DATABASE_NAME>"
        conn = MySQLdb.connect(IP, user, password, db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data WHERE SSH_Username = %s",[username])
        records = cursor.fetchall()
        for row in records:
                mail = row[1]+'@gmail.com'
                receiver = mail

"""Details for sending the mail"""
        sender = '<SENDER>'
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'ALERT!!!! Disk usage has exceeded'
        body = "The disk usage of your account in the" + host + "has exceeded the limit, please delete some files to free space.The files/folders consuming high disk usage are given below in MBs. \n\n"
        
        for k in pairs:
                body += k[0] + '     :        ' + str(k[1]) + '  MB \n'
        
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('smtp.gmail.com',25)
        s.starttls()
        text = msg.as_string(
        s.sendmail(sender, receiver, text)
        s.quit()



if __name__ == '__main__':
    all_home = get_home_usage()
    """Find users who are using the disk space above the treshold set and send mail to them."""
    for user_home, size in all_home.items():
        if size > 2000:
            send_mail(user_home)
