from micropythonserver import MicroPyServer

server = MicroPyServer("0.0.0.0", 8000)




def landing_page(request):
    server.send("Welcome!")

def start_server():
    server.add_route("/home", landing_page)
    server.start()
    print("Started Server")