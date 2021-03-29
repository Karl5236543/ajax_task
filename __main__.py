from PySide2 import QtWidgets, QtGui

import server  # DON`T REMOVE
import socket

def client():
    path_to_image = r'img.jpg'
    chunk=b''
    chunk_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect(('localhost', 8888))
        while True:
            conn.send('next'.encode())
            chunk = conn.recv(2048)
            print(len(chunk))
            if chunk:
                index, new_chunk = int.from_bytes(chunk[:1], byteorder='big'), chunk[1:]
                chunk_list.append((index, new_chunk))
            else:
                break

    data = b"".join([el[1] for el in sorted(chunk_list)])    
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
