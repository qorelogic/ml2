import web
#import view, config
import view
#from view import render
import devigetconnect4 as d

urls = (
    '/', 'index',
    '/games/1', 'games1',
    '/games/2', 'games2',
    '/games/3', 'games3',
    '/reset',   'reset',
    '/sreset',   'sReset',
    '/scount',   'sCount',
)

class index:
    def GET(self):
        #return render.base(view.listing())
        return render.base('qwe123')

class games1:
    def GET(self):
        #c4.play(4)
        c4.playRandom()
        """
        c4.play(3)
        c4.play(5)
        c4.play(3)
        c4.resetBoard()	
        """
        return (c4.grid.to_html())

class games2:
    def GET(self):
        #return render.base(view.listing())
        c4.playRandom()
        """        
        c4.play(4)
        c4.play(3)
        c4.play(5)
        c4.play(3)
        c4.resetBoard()	
        """
        #return render.base('qwe')
        return c4.grid.to_html()

class games3:
    def GET(self):
        #s = web.ctx.session
        c4.playRandom()
        """
        c4.play(3)
        c4.play(5)
        c4.play(3)
        c4.resetBoard()	
        """
        #return render.base('qwe')
        return c4.grid.to_html()

class reset:
    def GET(self):
        c4.resetBoard()
        return (c4.grid.to_html())
        
class sCount:
    def GET(self):
        session.count += 1
        return str(session.count)

class sReset:
    def GET(self):
        session.kill()
        return ""


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

#app = web.application(urls, globals())
app = MyApplication(urls, globals())
render = web.template.render('templates/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
c4 = d.connectfour()

if __name__ == "__main__":
    app.internalerror = web.debugerror
    #app.run()
    import os
    port = int(os.environ.get('PORT', 8080))
    print port
    app.run(port=port)
    
