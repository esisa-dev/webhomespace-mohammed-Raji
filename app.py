from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
from services import Services_User

import logging

logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('logger.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('SignIn.html')

@app.route('/SignIn', methods=['GET', 'POST'])
def SignIn():
    if request.method == 'POST':
        username = request.form['n_user']
        password = request.form['p_user']
        if(Services_User().checkUser(username, password)):
            session['username'] = username
            session['path'] = username
            flash('logged in')
            logger.info(f'{username} logged in')
            return render_template('dashboard.html')
        else:
            flash('Invalid username or password')
            logger.warning(f'Invalid login attempt for user {username}')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    if request.method == 'POST':
        path = session['path']
        button = request.form['button']
        print('**************************************')
        print(button)
        if button == 'user':
            session['path'] = session['username']
            path = session['path']
            return render_template('dashboard.html', dirs=Services_User().getDirectories(path))
        if button == 'directories':
            dirs = str(Services_User().getDirectories(path))
            return render_template('dashboard.html',dirs=Services_User().getDirectoriesall(path), var='nombre des dossiers : '+str(len(dirs)))
        if button == 'files':
            files = str(Services_User().getFiles(path))
            return render_template('dashboard.html',dirs=Services_User().getDirectoriesall(path), var='nombre des fichiers : '+str(len(files)))
        if button == 'space':
            total = Services_User().total_size(path)
            return render_template('dashboard.html',dirs=Services_User().getDirectoriesall(path), var='nombre Total : '+str(total))
        if button == 'find':
            path = session['username']
            search = request.form['search']
            return render_template('dashboard.html', dirs=Services_User().rechercher(path, search))
        if button == 'download':
            path = session['username']
            Services_User().download(path)
            send_file('/home/'+path+'/'+path+'.zip',as_attachment=True)
        else:
            if('/home/' in button):
                comment = button.split("/home/")[1].strip()
                session['path'] = comment
            else:
                session['path'] += '/'+button
            path = session['path']
            if os.path.isdir('/home/'+path):
                return render_template('dashboard.html', dirs=Services_User().getDirectories(path))
            else:
                user_dir = '/home/'+path
                with open(user_dir,'r') as f:
                    file_content = f.readlines()
                return render_template('file.html', file_content=file_content)
        return render_template('dashboard.html')




if __name__ == '__main__':
    app.run(debug=True)