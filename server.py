import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = ["Which CPU powered the Altair 8800? \n a.Atmel-ATMEGA328p \n b.Intel-8080 \n c.Intel-4004 \n d.AMD-AM9080", 
            "A camel's hump is for: \n a.Storing water \n b.Deterring predators \n c.Storing fat \n d.Providing balance",
            "Which of these dogs are used pull sleds? \n a.Huskies \n b.Golden Retrievers \n c.Chihuahuas \n d.Terriers",
            "The ENIAC used ____ instead of transistors: \n a.Mechanical Relays \n b.manual switches \n c.Variable resistors \n d.Vacuum Tubes"]
     


answers = ["b", "c", "a", "d"]

print("Server has started...")

def get(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Ready to start?".encode('utf-8'))
    conn.send("Evey Question is multiple choice.\n".encode('utf-8'))
    conn.send("Enter A,B,C or D to answer.\n\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Correct! Score: {score}\n\n".encode('utf-8'))
                else:
                    conn.send(f"Incorrect! Score: {score}\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
