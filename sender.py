import sys
import socket
import os
import random

from util import *

#Usage: python sender.py [Receiver IP] [Receiver Port] [Window Size] [Sender Port]
#maindeki yorumlu kısmı yorumdan çıkararak üstteki şekilde kullanabilirsiniz

def sender(receiver_ip, sender_port, receiver_port, window_size):

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Dosya paketlerini oluşturmak için
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #ACK paketlerini almak için
    recv_sock.bind((receiver_ip, receiver_port))

    file_name="D:/Users/efe.sekmen/Desktop/aglar/deneme.txt" #yollanılacak dosya hardcoded
    data_length= os.path.getsize(file_name)
    pkt_header=PacketHeader()

    with open(file_name) as f:
        lines = f.readlines()
        f.close()
        msg=''.join(lines)

    while(data_length%window_size!=0):
        print("cant equally part the message, type another window size : ")
        window_size=sys.argv[1]

    packet_num=int(data_length/window_size)
    msg.encode('utf-8')
    window=list()

    def my_range(start, end, step):
        while start <= end:
            yield start
            start += step

    #Dosyayı stringe çevirerek paketlere bölüyorum
    for j in my_range(0,data_length,window_size):
        window.append(msg[j:j+window_size])

    ack=0
    for i in range(packet_num+2):

        dummy = random.randint(0, packet_num)

        if i==0:   #Rastgele bir seq_num ile start mesajı yollanıyor
            pkt_header.type=0
            pkt_header.seq_num=dummy
            send_sock.sendto(bytes(pkt_header),(receiver_ip,receiver_port))
            is_ack=ack_received(recv_sock)
            while(is_ack== False):
                send_sock.sendto(bytes(pkt_header), (receiver_ip, sender_port))
                is_ack=ack_received(recv_sock)
        elif i==(packet_num+1): #Rastgele bir seq_num ile end mesajı yollanıyor
            pkt_header.type=1
            pkt_header.seq_num=dummy
            send_sock.sendto(bytes(pkt_header), (receiver_ip, sender_port))
            is_ack = ack_received(recv_sock)
            while(is_ack== False):
                send_sock.sendto(bytes(pkt_header), (receiver_ip, sender_port))
                is_ack=ack_received(recv_sock)

        else: #Dosyayı içeren paketler yollanıyor
            pkt_header.type=2
            pkt_header.seq_num=int(i-1)
            pkt_header.length=len(window[i-1])
            pkt_header.checksum=compute_checksum(window[i-1])
            send_sock.sendto(bytes(pkt_header/(window[i-1])),(receiver_ip,sender_port))


    for i in range(packet_num):
        is_ack=ack_received(recv_sock)
        if is_ack==True:
            ack=ack+1
    if ack!=(window_size-1):
        sender(receiver_ip,sender_port, receiver_port,window_size)

def ack_received(recv_sock):
    pkt, address = recv_sock.recvfrom(2048)
    pkt_header = PacketHeader(pkt[:16])
    if pkt_header.type == 3:
        return True
    else:
        return False

def main():

    #receiver_ip = sys.argv[1]
    #receiver_port = int(sys.argv[2]) #ACK dosyalarını alması için ayrı bir port tanımlıyorum, recv_sock ile bind edilmiş
    #window_size = int(sys.argv[3])
    #sender_port= int(sys.argv[4]) #Dosya paketlerini yollaması için

    receiver_ip = "127.0.0.1"
    receiver_port = 9000
    window_size = 4
    sender_port = 8000

    sender(receiver_ip, sender_port, receiver_port, window_size)


if __name__ == "__main__":
    main()
