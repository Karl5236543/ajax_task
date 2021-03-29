from PySide2 import QtWidgets, QtGui

import server  # DON`T REMOVE
import socket

def client():
    path_to_image = r'img.jpg'
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('localhost', 8888))
    chunk=b''
    chunk_list = []
    try:
        while True:
            conn.send('next'.encode())
            chunk = conn.recv(2048)
            if chunk:
                index = int.from_bytes(chunk[:1], byteorder='big')
                new_chunk = chunk[1:]
                chunk_list.append((index, new_chunk))
            else:
                break
    except ConnectionAbortedError:
        conn.close()
    sorted_chunks = sorted(chunk_list, key=lambda el: el[0])
    data = b"".join([el[1] for el in sorted_chunks])    
    
    with open(path_to_image, 'wb') as f:
        f.write(data)
        f.flush()
    return path_to_image


def main():
    client()
    path = client()
    app = QtWidgets.QApplication([])
    label = QtWidgets.QLabel()
    label.setMinimumSize(100, 100)
    label.setPixmap(QtGui.QPixmap(path))
    label.show()
    app.exec_()


if __name__ == '__main__':
    main()
