import socket
import tkinter as tk
from tkinter import filedialog
import os

g_filepath = ""
g_folderpath = ""

g_send_num = 1
g_is_sending = g_send_num.to_bytes(1, "big")
g_get_num = 0
g_is_getting = g_get_num.to_bytes(1, "big")


def move_to_send_window():
    root.withdraw()
    send_window.deiconify()

def move_to_get_window():
    root.withdraw()
    get_window.deiconify()

def connect_to_server():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 32445

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((SERVER_IP, SERVER_PORT))
    except ConnectionRefusedError:
        label_file_name.set("An exception occured while connecting")
        return

    return soc;


def send_file_name(soc, file_name):
    """Sendind to the server the filename"""
    char_size_in_bytes = 1
    bytes_to_send = len(file_name) * char_size_in_bytes
    bytes_sent = soc.send(bytes_to_send.to_bytes(4, "big"))
    bytes_sent = soc.send(file_name.encode())

def sending_a_file():
    soc = connect_to_server();
    if soc == None:
        return

    global g_is_sending

    """Showing the server that we want to send a file"""
    soc.send(g_is_sending)
    
    global g_filepath
    file_name = os.path.basename(g_filepath)
    send_file_name(soc, file_name)

    """Sendind to the server the file content"""
    with open(g_filepath, "rb") as file:
        bytes_to_send = os.path.getsize(g_filepath)
        BYTES_SENT_EACH_TIME = 2048
        while(bytes_to_send > 0):
            BYTES_SENT_EACH_TIME = 2048
            bytes_sent = soc.send(file.read(BYTES_SENT_EACH_TIME))
            bytes_to_send -= bytes_sent

            if bytes_sent < BYTES_SENT_EACH_TIME  and  bytes_to_send > 0 :
                file.seek(file.tell() - (BYTES_SENT_EACH_TIME - bytes_sent))

    label_file_name.set("File sent successfuly!");



def downloading_a_file():
    soc = connect_to_server();
    if soc == None:
        return

    global g_is_getting

    """Showing the server that we want to download a file"""
    soc.send(g_is_getting)

    file_name = file_name_text_label.get(1.0, "end - 1c")
    send_file_name(soc, file_name)

    global g_folderpath
    file_path = g_folderpath + "\\" + file_name

    BYTES_GET_EACH_TIME = 2048
    with open(file_path, "wb") as file:
        """Downloading the file content"""
        recieved = soc.recv(BYTES_GET_EACH_TIME)
        while(len(recieved) > 0):
            file.write(recieved)
            recieved = soc.recv(BYTES_GET_EACH_TIME)

        
    label_get_folder_name.set("File downloaded successfuly!");


def file_search():
    global g_filepath;
    g_filepath = tk.filedialog.askopenfilename(initialdir = "/",
											  title = "Select a File",
											  filetypes = (("all files",
															"*.*"),
															("Text files",
															"*.txt*")))

    label_file_name.set("The file choosen is: \r\n" + g_filepath)

def folder_search():
    global g_folderpath;
    g_folderpath = tk.filedialog.askdirectory()

    label_get_folder_name.set("The folder choosen is: \r\n" + g_folderpath)


root = tk.Tk()
root.geometry("325x175")
root.winfo_height = 100
root.title("Main Page")
root.configure(background="#C8E9F2")

frame = tk.Frame(root, pady=10, background="#C8E9F2")
frame.pack();

move_to_send_window_button = tk.Button(frame,
                          text = "Send file",
						  command=move_to_send_window,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
move_to_send_window_button.pack()

download_file_button = tk.Button(frame,
                          text = "Download file",
						  command=move_to_get_window,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
download_file_button.pack()


send_window = tk.Toplevel()
send_window.title("Send File")
send_window.geometry("300x250")
send_window.configure(background="#C8E9F2")
send_window.withdraw()

label_file_name = tk.StringVar()
label_for_file_name = tk.Label(send_window, textvariable=label_file_name)
label_for_file_name.configure(background="#C8E9F2")
label_for_file_name.configure(font=("Arial", 14))
label_for_file_name.pack()


choose_file_frame = tk.Frame(send_window, pady=10, background="#C8E9F2")
choose_file_frame.pack();

choose_file_button = tk.Button(choose_file_frame,
                          text = "Choose file",
						  command=file_search,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
choose_file_button.pack()

send_file_button = tk.Button(choose_file_frame,
                          text = "Send file",
						  command=sending_a_file,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
send_file_button.pack()






get_window = tk.Toplevel()
get_window.title("Get File")
get_window.geometry("300x250")
get_window.configure(background="#C8E9F2")
get_window.withdraw()

label_get_folder_name = tk.StringVar()
label_get_folder_name.set("Enter the name of the file you want to get")
label_for_get_file_name = tk.Label(get_window, textvariable=label_get_folder_name)
label_for_get_file_name.configure(background="#C8E9F2")
label_for_get_file_name.configure(font=("Arial", 14))
label_for_get_file_name.pack()


get_file_frame = tk.Frame(get_window, pady=10, background="#C8E9F2")
get_file_frame.pack();

file_name_text_label = tk.Text(get_file_frame,
                          bd=3,
                          cursor="hand2",
                          font=("Arial", 14),
                          height=2,
                          padx=10,
                          pady=5,
                          width=15,
                          background="light goldenrod")
file_name_text_label.pack()

choose_folder_button = tk.Button(get_file_frame,
                          text = "Choose folder",
						  command=folder_search,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
choose_folder_button.pack()

download_file_button = tk.Button(get_file_frame,
                          text = "Get file",
						  command=downloading_a_file,
                          anchor="center",
                          bd=3,
                          cursor="hand2",
                          disabledforeground="gray",
                          font=("Arial", 14),
                          height=2,
                          justify="center",
                          padx=10,
                          pady=5,
                          width=15,
                          wraplength=100,
                          background="gold")
download_file_button.pack()

root.mainloop()