from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import http.cookies
import uuid
import sqlite3
from export import yahoo, create_table

sessions = {}

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            header_info = self.headers.get('User-Agent')

            #get Cookie
            cookie_header = self.headers.get('cookie')
            cookies = http.cookies.SimpleCookie(cookie_header)
            session_id = cookies.get('session_id')

            print(f'Cookie_header: {cookie_header}')
            print(f'Coockes: {cookies}')
            print(f'Session: {session_id}')

            if session_id is None:
                session_id = str(uuid.uuid4())
                sessions[session_id] = {}
            else:
                session_id = session_id.value
            
            #Get session
            session_data = sessions.get(session_id, {})
            session_data.update({'session_id': session_id})
            session_data.update({'user_agent': header_info})
            sessions[session_id] = session_data

            print(f'Session Data: {session_data}')

            # rootファイルを読み込む
            file_path = 'userauth/index.html'

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    content = file.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', f'session_id={session_id}')
            self.send_header('Content-length', len(content))
            self.end_headers()

            self.wfile.write(content)
        
        elif self.path == '/yahoo':
            yahoo()
            self.send_response(200)
            self.end_headers()

        elif self.path == '/user':
            create_table()
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            c.execute('SELECT * FROM user')
            users = c.fetchall()
            conn.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(users).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        if self.path == '/':
            # Create table
            create_table()

            #get Cookie
            cookie_header = self.headers.get('cookie')
            cookies = http.cookies.SimpleCookie(cookie_header)
            session_id = cookies.get('session_id')

            if session_id is None:
                session_id = str(uuid.uuid4())
                sessions[session_id] = {}
            else:
                session_id = session_id.value
            
            #Get session
            session_data = sessions.get(session_id, {})
            headers = self.headers
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            parsed_data = {key: value[0] for key, value in parsed_data.items()}

            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            c.execute('INSERT INTO user (name, password) VALUES (?, ?)', (parsed_data['name'], parsed_data['password']))
            conn.commit()
            conn.close()

            self.send_response(200)
            # self.send_header('Set-Cookie', f'session_id={session_id}')
            self.end_headers()
            self.wfile.write(b'POST request for the homepage')

        elif self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            parsed_data = {key: value[0] for key, value in parsed_data.items()}

            create_table()
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            c.execute('SELECT * FROM user WHERE name = ? AND password = ?', (parsed_data['name'], parsed_data['password']))
            user = c.fetchone()
            conn.close()

            if user:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(str(user).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=AuthHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()