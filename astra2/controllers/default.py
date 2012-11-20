# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    try:
        session.username
    except NameError:
        redirect(URL('show'))
    else:
        if(session.username==None):
            form=SQLFORM(db.kids)
            if form.process().accepted:
                session.username = form.vars.username
                response.flash= "Welcome "+str(session.name)
                session.logged=1
                redirect(URL('show'))
      #  response.flash = "Welcome to web2py!"
       # return dict(message=T('Hello World'))
            usr = db().select(db.kids.username,db.kids.password)
            return dict(usr=usr,form=form,message="yoo")
        else:
            redirect(URL('show'))
      
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
      
def draw():
    return dict()  
def show():
    try:
        session.username
    except NameError:
        redirect(URL('index'))
    else:
        response.flash= "Welcome "+str(session.name)
        if(session.username==None):
            redirect(URL('index'))
        else:
            response.flash= "Welcome "+str(session.username)
    #if(session.logged==0):
     #   redirect(URL('index'))
    return dict()

def logout():
    db(db.kids.username == session.username).delete()
    session.username=None
    redirect(URL('index'))
    
def cheat():
    session.username=None

def enter():
    hall = request.args(0)
    row = db(db.kids.username == session.username).select().first()
    row.update_record(rno=hall)
    redirect(URL('index'))
    
def upframe():
    kamra = db(db.kids.username == session.username).select().first().rno
    current = db(db.rooms.rnum == kamra).select().first()
    framenumber = current.framenum
    current.update_record(framenum=framenumber+1)
    return framenumber
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


        
def admin():
    pass    

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
    s
@auth.requires_membership('Administrator')
def moderate():
    form=SQLFORM(db.rooms)
    if form.process().accepted:
        redirect(URL('admin'))
    return dict(form=form)
