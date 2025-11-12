
selectChatContentSQL = '''
    select chatrole role,content 
    from aichat
    where userid = ?
    order by chatid
'''


insertChatContentSQL = '''
    insert into aichat(userid,chatrole,content,thinkcontent)
    values(?,?,?,?),(?,?,?,?)
'''

selectChatContentSQL2 = '''
    select chatrole role,content ,thinkcontent thinkContent , chatid
    from aichat
    where userid = ?
    order by chatid
'''