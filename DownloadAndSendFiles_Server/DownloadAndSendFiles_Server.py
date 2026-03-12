import socket
import os

HOST_IP = "127.0.0.1"
PORT = 32445

g_num = 1
SEND_REQUEST = g_num.to_bytes(1, "big")
g_server_files_folder_path = "C:\\LizProjects\\PhytonLearning\\SendAndDownloadFiles_Project\\ServerFiles"

def get_file_name_from_client(soc):
    file_name = ""

    "Get file name"
    INT_SIZE_IN_BYTES = 4
    file_name_length = soc.recv(INT_SIZE_IN_BYTES)
    file_name = soc.recv(int.from_bytes(file_name_length, "big"))

    return file_name

def get_a_file(soc):
    file_name = get_file_name_from_client(soc)

    global g_server_files_folder_path
    file_path = g_server_files_folder_path + "\\" + file_name.decode()

    BYTES_GET_EACH_TIME = 2048
    with open(file_path, "wb") as file:
        """Downloading the file content"""
        recieved = soc.recv(BYTES_GET_EACH_TIME)
        while(len(recieved) > 0):
            file.write(recieved)
            recieved = soc.recv(BYTES_GET_EACH_TIME)


def send_a_file(soc):
    file_name = get_file_name_from_client(soc)

    global g_server_files_folder_path
    file_path = g_server_files_folder_path + "\\" + file_name.decode()\

    with open(file_path, "rb") as file:
        bytes_to_send = os.path.getsize(file_path)
        BYTES_SENT_EACH_TIME = 2048
        while(bytes_to_send > 0):
            BYTES_SENT_EACH_TIME = 2048
            bytes_sent = soc.send(file.read(BYTES_SENT_EACH_TIME))
            bytes_to_send -= bytes_sent

            if bytes_sent < BYTES_SENT_EACH_TIME  and  bytes_to_send > 0 :
                file.seek(file.tell() - (BYTES_SENT_EACH_TIME - bytes_sent))


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.bind((HOST_IP, PORT))
    except:
        print("An exception occured")

    soc.listen()

    conn, address = soc.accept()

    max_num_of_bytes = 1

    send_or_download = conn.recv(max_num_of_bytes)

    if send_or_download == SEND_REQUEST:
        get_a_file(conn)
    else:
        send_a_file(conn)

if __name__ == "__main__":
    main()