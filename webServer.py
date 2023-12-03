from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
from datetime import datetime

# 메모장에 저장될 파일 경로
file_path = "C:/Users/KIN/Desktop/memo.txt"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 입력 폼 제공
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><meta charset='utf-8'></head><body><form method='post'>"
                          "제품명: <input type='text' name='name'><br>"
                          "남은유통기한: <input type='text' name='date'><br>"
                          "<input type='submit' value='저장'></form></body></html>".encode('utf-8'))

    def do_POST(self):
        # POST 요청 처리
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        # 이름, 날짜를 추출
        name = parsed_data.get('name', [''])[0]
        date = parsed_data.get('date', [''])[0]

        # 현재 날짜 및 시간을 추가
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        memo = f"{name} | {date}Day({current_datetime}\n"

        # 입력된 데이터를 파일에 저장
        with open(file_path, 'a') as memo_file:
            memo_file.write(memo)

        # 응답 전송
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<html><head><meta charset='utf-8'></head><body><p>저장되었습니다.</p></body></html>".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"서버가 포트 {port}에서 시작되었습니다.")
    httpd.serve_forever()

if __name__ == '__main__':
    # 서버 실행
    run(port=8000)
