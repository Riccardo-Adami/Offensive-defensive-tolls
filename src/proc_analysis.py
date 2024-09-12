import os
import platform
import pefile as pe
import peutils as pes
import time

if platform.system == 'Linux':
    os.system("pip3 install psutil")
    import psutil
else: 
  os.system("pip install psutil")
  import psutil


proc_name = input("[X]name of the process...: \n")


def get_process_path(pid):
    try:
        process = psutil.Process(pid)
        return process.exe()  
    except psutil.NoSuchProcess:
        return f"[ERROR]Process with PID {pid} not found."
    except psutil.AccessDenied:
        return "[ERROR]AccessDenied to the proces."
    except Exception as e:
        return str(e)

def analysis():  
    for processes in psutil.process_iter():
        if processes.name() == proc_name:
            print("[INFO]: ", processes, "with pid: \n", processes.pid)
            process_pid = processes.pid
            kill = input("[*] Do u want to kill the process? (Y/N): \n")
            if kill.lower() == "Y":
                os.system("taskkill /in" + str(processes.pid))
            else:
                print("[X] Analysis of", proc_name, ".")
                print("[X] Analysis could take some time, please wait...")
                time.sleep(2)
                print("[X] Analysis in progress...")

                path1 = get_process_path(process_pid)

                path = pe.PE(path, True)
                sospicious = pes.is_suspicious(path)
                if sospicious == True:
                    print("[INFO] ",proc_name, "is sospicious...")
                    print("[INFO] It could be that: import tables are in unusual locations \n", "or section names are unrecognized \n", " or there is a presence of long ASCII strings....")
                else:
                    print("[INFO] File is not sospicious...\n")
                    continue
                time.sleep(3)
                print("[X] Analyzing signature... \n")
                time.sleep(1)
                valid = pes.is_valid(path)
                if valid != True:
                    print("[INFO] File's signature is not valid...\n")
                else:
                    print("[INFO] File's signature is valid...\n")

                print("[X] Analyzing sections...\n")
                
                for section in path.sections:
                    print("[INFO] File's section: \n")
                    time.sleep(1)
                    print (section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData "\n")

                print("[INFO] Analysis of the libraries... \n")
                time.sleep(1)

                path.parse_data_directories()
                for entry in path.DIRECTORY_ENTRY_IMPORT:
                    print("[INFO] LIbraries loaded... \n")
                    print (entry.dll, "\n")
                    for imp in entry.imports:
                        print ('\t', hex(imp.address), imp.name)

                print("[X] Analyzing the file format... \n")

                time.sleep(2)    

                strip =  pes.is_probably_packed(path)
                if strip == True:   
                    print("[INFO] File is probably packed or contains compressed data... \n")
                else:
                    print("[INFO] File isn't compressed or packed... \n")

    else: 
        print("[ERROR]No processes found...")
        exit()
