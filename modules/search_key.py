import subprocess

def search_key_path():
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE, text=True)
    
    output = result.stdout
    
    for line in output.splitlines():
        if '/media/' in line:
            key_found = line.split(" ")[-1]
            print("usb key is: ", key_found)
            return key_found
    
    print("No hay USB montado.")
    return False
