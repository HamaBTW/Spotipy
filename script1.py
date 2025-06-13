import subprocess
import time
import threading
from queue import Queue

def read_output(output_stream, output_queue):
    for line in iter(output_stream.readline, b''):
        output_queue.put(line.decode('utf-8'))
    output_stream.close()

def main():
    print("Script 1 is running")

    # Start script 2 as a subprocess with capturing standard output
    script2_process = subprocess.Popen(['python', 'script2.py'], stdout=subprocess.PIPE, text=True, bufsize=1)

    output_queue = Queue()

    # Start a thread to read script2.py output in real-time
    output_thread = threading.Thread(target=read_output, args=(script2_process.stdout, output_queue))
    output_thread.start()

    for i in range(5):
        time.sleep(1)
        print(f"Script 1 working ({i+1}/5)")

    # Terminate script 2
    script2_process.terminate()

    while script2_process.poll() is None:
        time.sleep(1)

    output_thread.join()  # Wait for the output thread to finish

    # Print the captured output of script2.py
    while not output_queue.empty():
        print(output_queue.get(), end='')

    print("Script 2 has completed.")

if __name__ == "__main__":
    main()
