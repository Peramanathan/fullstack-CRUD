from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = ""
                message += "<html><body>"
                message += "<a href='http://localhost:8080/restaurants/new'>Make a New Restaurant</a>"
                message += "</br>"
                for restaurant in restaurants:
                    message += restaurant.name
                    message += "</br>"
                    message += "<a href='#'>Edit<a> "
                    message += "</br>"
                    message += "<a href='#'>Delete<a>"
                    message += "</br></br>"

                message += "</body></html>"
                self.wfile.write(message)
                print message
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = ""
                message += "<html><body>"
                message += ''' <form method='POST' enctype='multipart/form-data' action='/restaurants/addMore'>
                    <h2>Type a restaurant name</h2>
                    <input name='message' type='text'><input type='submit' value='Submit' ></form> '''

                message += "</body></html>"
                self.wfile.write(message)
                print message
                return

        except IOError :
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                restaurant_name = messagecontent[0]                

            output = ""
            output += "<html><body>"
            output += " <h2> Your restaurant %s added successfully !</h2>" % restaurant_name
            output += "</br>"
            output += "<h2>Want to add more? </h2>"
            output += "</br>"
            output += ''' <form method='POST' enctype='multipart/form-data' action='/restaurants/addMore'>
                <h2>Type a restaurant name</h2>
                <input name='message' type='text'><input type='submit' value='Submit' ></form> '''
            output += "</body></html>"
            self.wfile.write(output)
            new_restaurant = Restaurant(name=restaurant_name)
            session.add(new_restaurant)
            session.commit()
            print output

        except:
            pass


def  main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except  KeyboardInterrupt :
        print "^C entered , stopping web server ..."
        server.socket.close()

if __name__ == '__main__':
    main()
