import flask
import flask_login
import sqlite3

#Database connection
def connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except con.Error as e:
        print(e)
    
    return con

#close connection
def close_con(con):
    con.close()

#fetch user info
def fetch(con):
    try:
        usr = []
        pas = []
        ids = []
        curs = con.cursor()
        curs.execute("SELECT UserID, Username, Password FROM user")
        rows = curs.fetchall()
        for i in rows:
            if len(i) > 1:
                ids.append(i[0])
                usr.append(i[1])
                pas.append(i[2])
        return usr, pas, ids
    except con.Error as e:
        print(e)
        close_con(con)

#main function
def main():
    program = flask.Flask(__name__)
    program.secret_key = 'Her!9931124'

    logman = flask_login.LoginManager()
    logman.init_app(program)
    
    db = 'Flickermeter.db'
    con = connection(db)
    [usr, pas, ids] = fetch(con)
    close_con(con)

    class User(flask_login.UserMixin):
        id = ids
        username = usr

    @logman.user_loader
    def usrload(usern):
        if usern not in usr:
            return

        user = User()
        user.id = usern
        return user    
    
    @logman.request_loader
    def reqload(req):
        usern = req.form.get('email')
        if usern not in usr:
            return

        user = User()
        user.id = usern

        user.is_authenticated = req.form['password'] == pas

        return user

    @program.route('/login', methods=['GET', 'POST'])
    def login():
        if flask.request.method == 'GET':
            return '''
                   <form action='login' method='POST'>
                   <input type='text' name='email' id='email' placeholder='email'/>
                   <input type='password' name='password' id='password' placeholder='password'/>
                   <input type='submit' name='submit'/>
                   <form/>
                   '''
        usern = flask.request.form['email']
        if flask.request.form['password'] == pas:
            user = User()
            user.id = usern
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))
        
        return 'Bad Login'
    
    @program.route('/protected')
    @flask_login.login_required
    def protected():
        return 'Logged in as: ' + flask_login.current_user.id

    @program.route('/logout')
    def logout():
        flask_login.logout_user()
        return 'Logged out'

    @logman.unauthorized_handler
    def unauthorized_handler():
        return 'Unauthorized'

if __name__ == '__main__':
    main()
    

