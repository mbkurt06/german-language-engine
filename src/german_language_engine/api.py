from __future__ import annotations
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .engine import GermanLanguageEngine

def make_handler(engine: GermanLanguageEngine):
 class Handler(BaseHTTPRequestHandler):
  def _headers(self,status=200):
   self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8")
   self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type")
   self.send_header("Access-Control-Allow-Methods","POST, OPTIONS"); self.end_headers()
  def do_OPTIONS(self): self._headers(204)
  def do_GET(self):
   if self.path=="/health":
    self._headers(); self.wfile.write(b'{"status":"ok"}'); return
   self._headers(404); self.wfile.write(b'{"error":"not_found"}')
  def do_POST(self):
   if self.path!="/analyze":
    self._headers(404); self.wfile.write(b'{"error":"not_found"}'); return
   try:
    length=int(self.headers.get("Content-Length","0")); payload=json.loads(self.rfile.read(length) or b"{}")
    text=payload.get("text","").strip()
    if not text: raise ValueError("text is required")
    result=engine.analyze(text).model_dump(mode="json")
    body=json.dumps(result,ensure_ascii=False).encode("utf-8"); self._headers(); self.wfile.write(body)
   except Exception as exc:
    body=json.dumps({"error":str(exc)},ensure_ascii=False).encode("utf-8"); self._headers(400); self.wfile.write(body)
  def log_message(self,format,*args): return
 return Handler

def serve(host="127.0.0.1",port=8765,model="de_core_news_md"):
 engine=GermanLanguageEngine()
 server=ThreadingHTTPServer((host,port),make_handler(engine))
 print(f"German Language Engine listening on http://{host}:{port}")
 server.serve_forever()

def main():
 parser=argparse.ArgumentParser(); parser.add_argument("--host",default="127.0.0.1"); parser.add_argument("--port",type=int,default=8765)
 parser.add_argument("--model",default="de_core_news_md"); args=parser.parse_args(); serve(args.host,args.port,args.model)

if __name__=="__main__": main()
