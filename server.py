#*-* coding utf-8 *-*
import socket, random, sys, threading, time
from datetime import date

run = 1

HOST = sys.argv[1] if len(sys.argv) > 1 else ''
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 44444
usuariosA = ['beto', 'alex']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Server(object):
	def __init__(self, s):
		self.usuarios = []
		self.run = 1
		self.s = s
		self.lock = threading.RLock()
		try:
			self.s.bind((HOST, PORT))
			self.s.listen(5)
		except Exception, e:
			print "Error al preparar el socket\n%s" % e
			return
		self.date_display("Servidor escuchando en %s..." % str(s.getsockname()))

		while self.run:
			try:
				socket, address = self.s.accept()
				usuario = socket.recv(100)

				if self.establecer_conexion(socket, usuario) == None:
					pass

			except Exception, e:
				print "Error al recibir una conexion\n%s" % e


	def establecer_conexion(self, socket, usuario):
			self.date_display("Se ha conectado un nuevo cliente desde %s" % str(socket.getsockname()))
			print "Autenticando al usuario %s..." % usuario
			if not self.autenticar(usuario):
				print "Datos incorrectos"
				return None
			print "Usuario logeado con exito"
			conexion = control_cliente(self, socket, usuario)
			conexion.start()
			self.usuarios.append(conexion)

	def autenticar(self, usuario):
		if usuario in usuariosA:
			return True

	def date_display(self, msg):
		hour = time.gmtime()
		mensaje = '['+str(hour.tm_hour)+':'+str(hour.tm_min)+':'+str(hour.tm_sec)+'] '+ msg
		print mensaje


	def broadcast(self, msg, name):
		with self.lock:
			hour = time.gmtime()
			mensaje = '['+str(hour.tm_hour)+':'+str(hour.tm_min)+':'+str(hour.tm_sec)+'] '+name+': '+ msg
			print mensaje
			for usuario in self.usuarios:
				if not usuario.escribir_mensaje(mensaje):
					self.usuarios.remove(usuario)

		def desconectar(self, usuario):
			self.date_display("%s se ha desconectado" % usuario)
			self.usuarios.remove(usuario)

class control_cliente (threading.Thread):
	def __init__(self, server, socket, name):
		threading.Thread.__init__(self)
		self.server = server
		self.socket = socket
		self.name = name
	def run(self):
		self.server.broadcast("Se ha conectado", self.name)
		while True:
			try:
				mensaje = self.socket.recv(200)
				if mensaje == '/q':
					self.exit.desconectar(self)
					thread.exit()
			except Exception, e:
				print "Error al recibir mensaje de %s" % str(self.socket.getsockname())
				break
			self.server.broadcast(mensaje, self.name)
		self.cerrar_socket()

	def cerrar_socket(self):
		try:
			self.socket.close()
		except:
			print "Error al cerrar la conexion con %s" % str(self.socket.getsockname())

	def escribir_mensaje(self, msg):
		try:
			mensaje = msg + "\n> "
			self.socket.sendall(mensaje)
		except Exception, e:
			print "Error al enviar mensaje a %s" % str(self.socket.getsockname())
			self.cerrar_socket()
			return False
		return True


if __name__ == '__main__':
	Server(s)
