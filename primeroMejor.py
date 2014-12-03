#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, sys, math

distancias = {}
N = 10
vecinosGenerados = []
listaVecinos = []
soluciones = []

def num_vecinos():
	return (N - 1) * (N - 2) / 2

def carga_fichero_distancias(nombre_fichero):

	global distancias
  	f = open(nombre_fichero, 'r')
  	lines = f.readlines()
  	for i in range(len(lines)):
		dists = lines[i].strip('\r\n').split('\t')
		distancias[i + 1] = []
		for dist in dists:
			distancias[i + 1].append(dist)
	f.close()

def genera_lista_vecinos(nombre_fichero):

	global listaVecinos
	Sinicial = []
	f = open(nombre_fichero, 'r')
	lines = f.readlines()
	for i in range(0, 9):
		index = 1 + math.floor(float(lines[i].strip('\n')) * 9.0)
		Sinicial.append(int(index))
	for i in range(9, len(lines)):
		index = math.floor(float(lines[i].strip('\n')) * 9.0)
		listaVecinos.append(int(index))
	f.close()
	return Sinicial

def genera_vecino(solucion, fichero = None):

	vecino = list(solucion)
	index1_perm = index2_perm = 0
	valoresPerm = [0, 0]
	while True:
		if fichero == None:
  			index_perm = random.sample(range(0, 9), 2)
		else:
			if len(listaVecinos) == 0:
				return None
			index_perm = [listaVecinos.pop(0), listaVecinos.pop(0)]
		
  		aux = vecino[index_perm[0]]
		vecino[index_perm[0]] = vecino[index_perm[1]]
		vecino[index_perm[1]] = aux
		if vecino not in vecinosGenerados or len(vecinosGenerados) >= num_vecinos():
			break
		else:
			vecino[index_perm[1]] = vecino[index_perm[0]]
			vecino[index_perm[0]] = aux
	if fichero:
		print "\tIndices de intercambio:", index_perm
		print "\tRecorrido:", vecino 
	vecinosGenerados.append(vecino)
	return vecino
 
def calcular_coste(solucion):

	#Cálculo del coste de la ciudad 0 a la primera de la solución
	coste = int((distancias[solucion[0]])[0])
	for x in range(len(solucion) - 1):
		#Se calcula entre cada par de ciudades cuál es la de mayor índice para acceder correctamente al diccionario de distancias
		if solucion[x] > solucion[x + 1]:
			coste += int((distancias[solucion[x]])[solucion[x + 1]])
		else:
			coste += int((distancias[solucion[x + 1]])[solucion[x]])
	#Cálculo del coste de la última ciudad de la solución a la ciudad 0
	coste += int((distancias[solucion[N - 2]])[0])
	return int(coste)

def main():
	random.seed()
	count = mediaAcum = 0
	#Inicialización de la variable de control del fichero aleatorio.txt
	fichero = None
	global vecinosGenerados
  	carga_fichero_distancias('distancias_10.txt')
	print distancias
	i = x = 0 #Contadores de soluciones y vecinos
	if len(sys.argv) > 1: #Si recibimos el nombre del fichero como parámetro
		#Llamamos a la función que lee los valores del fichero recibido (aleaatorios.txt)
		fichero = 1
		Sactual = genera_lista_vecinos(sys.argv[1])
	else:
		#Si no, generamos la solucion inicial mediante una permutación aleatoria
		Sactual = range(1, N)
		random.shuffle(Sactual)

	while True:
		print "Iteracion %d" % count
		print ""
		if count > 0:
			random.shuffle(Sactual)
		while True:
			vecinosGenerados.append(Sactual)
			print "*******************SOLUCION S_%d*******************" % i
			print "Recorrido:", Sactual
			print "Longitud: %d" % calcular_coste(Sactual)
			print "" 
			mejorVecino = list(Sactual)
			while True:
				if x == num_vecinos():
					break
				if fichero:
					print "\tVECINO V_%d............................." % x
				siguiente = genera_vecino(Sactual, fichero)
				if siguiente == None:
					break
				coste_siguiente = calcular_coste(siguiente)
				if fichero:
					print "\tLongitud: %d" % coste_siguiente
					print ""
				x += 1
				if coste_siguiente < calcular_coste(mejorVecino) or x == num_vecinos():
					del vecinosGenerados[:]
					x = 0
					i += 1
					if fichero:
						print ""
					break
		
			if coste_siguiente < calcular_coste(Sactual):
				Sactual = list(siguiente)
			if coste_siguiente >= calcular_coste(mejorVecino):
				mediaAcum += calcular_coste(mejorVecino)
				count += 1
				i = 0
				print mejorVecino
				soluciones.append(calcular_coste(Sactual))
				break
		
		if fichero == 1 or count > 9:
			break

	if not fichero:
		media = float(mediaAcum) / 10.0
		aux = 0.0
		solPeor = soluciones[0]
		solMejor = soluciones[1]
		for x in soluciones:
			aux += (float(x) - media) ** 2
			if solPeor < x:
				solPeor = x
			if solMejor > x:
				solMejor = x
			print x 
		desvTipica = math.sqrt(aux / (N - 1) - media)
		print "Media: %f" % media
		print "Desviación típica: %f" % desvTipica
		print "Maximo: %d\tMinimo: %d" % (solPeor, solMejor)

if __name__ == '__main__':
	main()
