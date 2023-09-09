
import os
import shutil

def flatten(directory):
    for dirpath, _, filenames in os.walk(directory, topdown=False):
        if "interface" in dirnames:
            dirnames.remove("interface")  
        for filename in filenames:
            i = 0
            source = os.path.join(dirpath, filename)
            target = os.path.join(directory, filename)
            while os.path.exists(target):
                i += 1
                file_parts = os.path.splitext(os.path.basename(filename))
                target = os.path.join(
                    directory,
                    file_parts[0] + "_" + str(i) + file_parts[1],
                )
            shutil.move(source, target)
            print("Moved ", source, " to ", target)
        if dirpath != directory:
            os.rmdir(dirpath)
            print("Deleted ", dirpath)
            
            
            
flatten("../contracts/flat")