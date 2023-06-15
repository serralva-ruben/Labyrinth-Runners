import subprocess

def launch_server():
    subprocess.Popen(["python3", "client/main_client.py"])

def launch_client():
    subprocess.Popen(["python3", "server/main_server.py"])

if __name__ == "__main__":
    launch_server()
    launch_client()
    