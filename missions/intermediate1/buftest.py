import socket
import threading

BIND_IP = '0.0.0.0'
BIND_PORT = 9091


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "[*] Received: " + request
    if len(request) > 500:
    	client_socket.send('password is overflowyourmomsbox \n\n\n')
    	client_socket.close()
    else:
	client_socket.send('This server is unhackable. Fuck off!\n\n\n')

def tcp_server():
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    server.bind(( BIND_IP, BIND_PORT))
    server.listen(5)
    print"[*] Listening on %s:%d" % (BIND_IP, BIND_PORT)

    while 1:
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    tcp_server()
