

selectUserByUsernameSQL = '''
    select username from users where username = ?
'''


insertUserSQL = '''
    insert into users(username,pwd,nickname)
    values(?,?,?)
'''