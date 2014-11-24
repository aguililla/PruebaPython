import socket, sys, threading, time

HOST = sys.argv[1] if len(sys.argv) > 1 else ''
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 44444
NOMBRE = sys.argv[3] if len(sys.argv) > 3 else 'ANON'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Cliente(object):
	def __init__(self, s):
		self.s = s
		self.run = 1
		try:
			self.s.connect((HOST, PORT))
		except Exception, e:
			print "Excepcion al conectar al servidor %s\n%s" % (HOST, e)
			return
		print "Conectado al servidor %s" % HOST
		self.login(NOMBRE)
		escuchador = threading.Thread(target=self.init_listener)
		escuchador.start()

		while self.run:
			mensaje = raw_input('> ')
			self.enviar_mensaje(mensaje)
			if mensaje[0] == '/':
				if mensaje[1] == 'q':
					self.run = 0
					#self.enviar_mensaje('')
					self.desconectar()


	def display(self, msg):
		print msg,
		sys.stdout.flush()


	def date_display(self, msg):
		hour = time.gmtime()
		mensaje = '['+str(hour.tm_hour)+':'+str(hour.tm_min)+':'+str(hour.tm_sec)+'] '+ msg
		print mensaje

	def enviar_mensaje(self, msg):
		try:
			self.s.sendall(msg)
		except Exception, e:
			self.date_display("Error al enviar el mensaje")
		return

	def login(self, nombre):
		try:
			self.s.sendall(nombre)
		except Exception, e:
			print "Excepcion al logearse\n%s" % e
			return

	def desconectar(self):
		try:
			self.s.close()
		except Exception, e:
			print "Error al intentar desconectar\n%s" % e
		return

	def init_listener(self):
		while True:
			try:
				mensaje = self.s.recv(200)
				self.display(mensaje)
			except Exception, e:
				print "Error al recibir un mensaje\n%s" % e
				break


if __name__ == '__main__':
	Cliente(s)
