import zipfile
import argparse
from colorama import Fore

def set_arguments():
    
    option = argparse.ArgumentParser()
    
    option.add_argument('-z','--zip',dest='zip',help='zipfile')
    
    option.add_argument('-w','--wordlist',dest='wordlist',help='wordlist')

    arg = vars(option.parse_args())
    
    return arg

  
def crack_password(password_list, obj):
    with open(password_list, 'rb') as file:
        for line in file:
            for word in line.split():
                try:
                    obj.extractall(pwd=word)
                    print(Fore.YELLOW + "Password found!!" + Fore.RESET)
                    print(Fore.RED + "Password is"+ Fore.RESET, word.decode())
                    return True
                except:
                    continue
    return False
  

if __name__ == "__main__":

    args = set_arguments()

    password_list = args['wordlist']

    zip_file = args['zip']
  
    # ZipFile object initialised
    obj = zipfile.ZipFile(zip_file)

    print(Fore.YELLOW +'\nAttempting to Crack:' + Fore.RESET, zip_file)
  
    password = crack_password(password_list, obj) 

    if password == False:
       print(Fore.RED + "Password not found in this file"+ Fore.RESET)