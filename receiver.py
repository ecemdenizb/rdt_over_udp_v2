import sys
import socket
from util import *

#Usage: python receiver.py [Receiver IP] [Receiver Port] [Window Size] [Sender Port]
#maindeki yorumlu kısmı yorumdan çıkararak üstteki şekilde kullanabilirsiniz

def receiver(receiver_ip, receiver_port, window_size, sender_port):

    while True:
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        recv_sock.bind((receiver_ip, receiver_port))
        #start mesajı bekliyor
        pkt, address = recv_sock.recvfrom(2048)
        pkt_header = PacketHeader(pkt[:16])

        if(pkt_header.type==0): #start mesajı gelirse paketleri alıyor
            pkt_header.type=3
            send_sock.sendto(bytes(pkt_header),(receiver_ip, sender_port)) #start mesajı için ACK yollanıyor
            paketler=list()
            mesajlar=list()

            for i in range(window_size+1):
                pkt, address = recv_sock.recvfrom(2048)
                in_pkt_header = PacketHeader(pkt[:16])
                msg=pkt[16:16 + in_pkt_header.length]

                if in_pkt_header.type==2: # DATA tipindeki paketler birleştirilmek için mesajlar listesinde toplanıyor
                    mesajlar.append(msg.decode('utf-8'))
                    computed_checksum= compute_checksum(str(msg,'utf-8'))

                if in_pkt_header.checksum == computed_checksum:
                    paketler.append(in_pkt_header) # Eğer checksumlar aynıysa bu paketler ack yollanmak üzere bir listede tutuluyor

                if in_pkt_header.type==1:
                    print("indirildi")

            for k in range(len(paketler)):
                paketler[k].type=3
                send_sock.sendto(bytes(paketler[k]),(receiver_ip,receiver_port))

            mesaj=''.join(mesajlar) # Yeni dosyaya yazmak için ayrı ayrı alınan paketler birleştiriliyor

        f=open("abc.txt",'w+')
        f.write(str(mesaj))
        f.close()


def main():

   # receiver_ip = sys.argv[1]
   # receiver_port = int(sys.argv[2])
   # window_size = int(sys.argv[3])
   # sender_port= int(sys.argv[4])
    receiver_ip="127.0.0.1"
    receiver_port=8000
    window_size=4
    sender_port=9000

    receiver(receiver_ip, receiver_port, window_size, sender_port)


if __name__ == "__main__":
    main()
