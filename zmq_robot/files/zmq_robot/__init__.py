'''
Created on 26.05.2013

@author: kkirsanov
'''

NSRUN = True
import json  # , simplejson
simplejson = json
PORT = 15701
import multiprocessing
from multiprocessing import Pool
        
import zmq
import time

import thread

import threading
def checkNS(ip):
    if tryConnect(ip, PORT):
        return True
    return False

import multiprocessing.dummy


def getNS():
    ip = getLocalIp()
    ip = ".".join(ip.split(".")[:3])
    ips = []
    for x in range(255):
        ips.append("%s.%s" % (ip, str(x)))
    p = multiprocessing.dummy.Pool(50)
    ns = p.map(checkNS, ips)
    okIp = []
    for i, x in enumerate(ns):
        if x:
            okIp.append("%s.%d" % (ip, i))
    return okIp

def getLocalIp():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.153', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def tryConnect(ip=getLocalIp(), port=PORT, timeout=10, dt=0.01):
    ok = None
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://" + str(ip) + ":" + str(port))
    socket.send_json({"action": "list"})
    # print "send at ", time.time()
    t = time.time()
    while t + timeout > time.time():
        try:
            socket.recv_json(zmq.DONTWAIT)
            ok = (ip, port)
        except Exception, e:
            time.sleep(dt)
            continue
    socket.setsockopt(zmq.LINGER, 0)
    return ok
    
class RoboConnector:
    def __init__(self, ip, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.addr = "tcp://" + ip + ":" + str(port)
        self.socket.connect(self.addr)
        self.t0 = time.time() - 10000
        self.dataReady = False
    def get(self, dt=0.05):
        if (self.t0 + dt > time.time()) and (self.dataReady):
            return self.cache
        else:
            # print 'call'
            self.socket.send_json(dict(action='get', count=1))
            self.cache = self.socket.recv_json()
            self.t0 = time.time()
            self.dataReady = True
            return self.cache
    def set(self, data=None):
        self.socket.send_json(dict(action='set', data=data, count=1))
        return self.socket.recv_json()
    def stop(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        # self.socket.disconnect(self.addr)
class RoboWorker(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self.ns_ip = getLocalIp()
        self.src = ""
        self.command = []
        self.ns = None
        time.sleep(0.1)
#    def pubSource(self, fname):
#        self.wcontext.socket(zmq.PUB)
#        socket.bind("tcp://127.0.0.1:5556")
    def add(self, data):
        self.data.append((time.time(), data))
        self.command.append((time.time(), data))
        if len(self.data) > 100:
            self.data = self.data[-100:]
        return data
    def get(self, cnt=1):
        import types
        try:
            return self.command[-cnt:]
        except:
            return None    
        
    def run(self):
        self.canGo = True
        self.command = []
        cnt = 0
        try:
            while self.canGo:
                try:
                    data = self.wsocket.recv(zmq.DONTWAIT)
                except:
                    time.sleep(0.001)
                    continue
                
                data = simplejson.loads(data)
                try:
                    if data['action'] == 'call':
                        pass
                    if data['action'] == 'source':
                        if self.src:
                            self.wsocket.send_json(dict(source=self.src))
                    if data['action'] == 'line':
                        if self.src:
                            self.wsocket.send_json(dict(line=self.src_line))
                        
                    if data['action'] == 'get':
                        self.wsocket.send_json(self.data[-1])
                    if data['action'] == 'set':
                        self.command.append((time.time(), data['data']))
                        self.wsocket.send_json(dict(status='ok'))
                except:
                    self.wsocket.send_json(dict(status='wrong params'))
                time.sleep(self.dt)
            self.wsocket.close()
            self.wcontext.term()
        except Exception as e:
            print e
            self.wsocket.send_json(dict(status='error', error=str(e)))
            
    def _start(self, name, fname=None):
        ip = getLocalIp()
        z = tryConnect(ip, PORT, 1)
        print z, "NS"
        global NSRUN
        print "NS =", NSRUN
        if NSRUN:
            NSRUN = False
            self.ns = NameServer()
            self.ns.start()
            
        self.dt = 0.001
        self.canGo = True
        self.lastSSend = time.time()
        self.data = [(time.time(), 0)]
        self.wcontext = zmq.Context()
        self.wsocket = self.wcontext.socket(zmq.REP)
        self.port = self.wsocket.bind_to_random_port("tcp://*")
        self._register(name, self.port)
        self.start()

    def _startSource(self, fname):
        try:
            self.src = "".join(open(fname).readlines())
            self.fname = fname
                        
            def traceit(frame, event, arg):
                co = frame.f_code
                line_no = frame.f_lineno
                filename = co.co_filename
                print fname, filename
                if event == "line":
                    # func_name = co.co_name
                    if fname in filename:
                        self.src_line = line_no
                return traceit
            return traceit
        except Exception, e:
            print e
    def stop(self):
        print "STOP"
        if self.ns:
            self.ns.stop()
        self.wsocket.setsockopt(zmq.LINGER, 0)
        self.canGo = False
        time.sleep(0.01)
    def _register(self, name, port):
        self.data = []
        self.name = name
        self.rcontext = zmq.Context()
        self.rsocket = self.rcontext.socket(zmq.REQ)
        s = "tcp://" + self.ns_ip + ":" + str(PORT)
        print 'connecting', s
        self.rsocket.connect(s)
        self.rsocket.send_json(dict(action='register', name=name, port=port, ip=self.ns_ip))
        return self.rsocket.recv_json()
    def list(self, ns_ip=getLocalIp(), name=""):
        self.lcontext = zmq.Context()
        self.lsocket = self.lcontext.socket(zmq.REQ)
        self.lsocket.connect("tcp://" + ns_ip + ":" + str(PORT))
        self.lsocket.send_json(dict(action='list'))
        d = self.lsocket.recv_json()
        
        ret = []
        if name:
            for x in d:
                if x['name'].lower() == name.lower():
                    ret.append(x)
            return ret
        else:
            return d
                
class NameServer(threading.Thread):
    def stop(self):
        self.canGo = False
        while not self.isStopped:
            time.sleep(0.1)
    def run(self):
        self.isStopped = False

        print "Starting nameserver on", getLocalIp(), str(PORT)
        time.sleep(1)
        self.canGo = True
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        # socket.bind("tcp://" + config.local_ip + ":" + str(config.name_port))
        socket.bind("tcp://*:" + str(PORT))
        programs = {}
        counter = 0
        
        import SimpleHTTPServer, SocketServer
        WPORT = 8080
        import pprint, StringIO
        class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
            def do_GET(self):    
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write("<html><body>");
                self.wfile.write("<h1>Programs</h1><pre>");
                s = StringIO.StringIO()
                pprint.pprint(programs, s)
                self.wfile.write(s.getvalue()) 
                self.wfile.write("</pre>");
                
                self.wfile.write("</body></html>");
                self.wfile.close();
        Handler = MyHandler

        # self.httpd = SocketServer.ThreadingTCPServer(("", WPORT), Handler)
        
        
        print "serving WWW at port", WPORT
        # self.www = threading.Thread(target=self.httpd.serve_forever).start()

        while self.canGo:
            data = {}
            try:
                data = socket.recv_json(zmq.DONTWAIT)
                print data
            except Exception, e:
                time.sleep(0.01)
                continue
            print 'NS recive at', time.time()
            try:
                data['action']
            except:
                data['action'] = 'ping'
            try:
                if data['action'] == 'register':
                    try:
                        data['location']
                    except:
                        data['location'] = 'local'
                    programs[data['name']] = dict(time=time.time(), ip=data['ip'], port=data['port'], location=data['location'])
                    print "registrating ", data['name'], programs[data['name']] 
                    socket.send_json(dict(status='ok'))
                    continue
                if data['action'] == 'list':
                    d = []
                    for k, v in programs.iteritems():
                        d.append(dict(name=k, data=v)) 
                    socket.send_json(d)
                    print 'send at', time.time()
                    continue
                if data['action'] == 'ping':
                    socket.send_json(dict(status='ok'))
                    continue
            except Exception, e:
                print e
                socket.send_json(dict(status='fail', text=str(e)))
                continue
        
            socket.send_json(dict(status='fail', text='wrong action'))
        
        socket.close()
        context.term()
        # self.httpd.shutdown()
        print "closing nameserver"
        self.isStopped = True
