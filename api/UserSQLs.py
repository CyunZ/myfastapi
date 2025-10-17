

selectUserByUsernameSQL = '''
    select username from users where username = ?
'''


insertUserSQL = '''
    insert into users(username,pwd,nickname)
    values(?,?,?)
'''

selectLoginUserSQL = '''
    select userid,cast(pwd as varbinary(max)) pwd,nickname
    from users
    where username=?
'''