import requests
import json
import argparse
from colorama import Fore

def options() -> dict:

    '''
    Function to define arguments.

    Parameters
    ----------
    None

    Returns
    -------
    arg:dict Dict of arguments
    '''

    option = argparse.ArgumentParser()
    option.add_argument('-i', '--identity', dest='identity', help='identity to be searched for in crt.sh')
    option.add_argument('-w', '--no-wild-card-expression', dest='no-wild-card-expression', help="Don't use wildcard expression in search")

    arg = vars(option.parse_args())
    
    return arg

def crt_request(url:str) -> dict:

    '''
    Function to make request to crt.sh

    Parameters
    ----------
    url:str url to make the get request to.

    Returns
    -------
    crt_json:dict json file of response.
    '''

    try:
        crt_response = requests.get(url)
        crt_json = json.loads(crt_response.text, strict=False)
        return crt_json
    
    except Exception as e:
        print(Fore.RED + '\n', e, '\n' + Fore.RESET)


def parsing(json_file:dict) -> dict:

    '''
    Function to parse through the response from crt.sh and extracts relevant 

    Parameters
    ----------
    json_file:dict Dictionary/json file of response

    Returns
    -------
    results:dict Dictionary of two lists of sub_domains and potential_sub_domains
    '''

    sub_domains = []
    potential_sub_domains = []
    
    for index in range(len(json_file)):
        name = json_file[index]['name_value']
        name_split = name.split('\n')
    
        for sub_domain in name_split:
            if '*' in sub_domain:
                potential_sub_domains.append(sub_domain)

            if '.' in sub_domain and '*' not in sub_domain:
                sub_domains.append(sub_domain)

    results = {
        'sub_domains' : sub_domains, 
        'potential_sub_domains' : potential_sub_domains,
        }
    
    return results

def write_to_file(file_name:str, list_of_sub_domains:list) -> object:
    
    '''
    Function to write lists to text files.

    Parameters
    ----------
    file_name:str Name of file
    list_of_sub_domains:str List of subdomains to be written to file

    Returns
    -------
    None (writes to file)
    '''

    file = open(file_name, 'w')

    for sub_domain in list_of_sub_domains:
        file.write(sub_domain)
        file.write('\n')
    file.close()

if __name__ == '__main__':

    arg = options()

    if arg['no-wild-card-expression'] == True:
        url = f'https://crt.sh/?q={arg["identity"]}&output=json'
    else:
        url = f'https://crt.sh/?q=%25.{arg["identity"]}&output=json'
    
    print(Fore.GREEN + f'\nSearching {url} for sub-domains\n' + Fore.RESET )
    crt_json = crt_request(url)

    print(Fore.GREEN + 'Parsing through results\n' + Fore.RESET )
    sub_domains_dict = parsing(crt_json)
    
    print(Fore.YELLOW + 'Writing to file\n' + Fore.RESET)
    write_to_file('sub_domains.txt', sub_domains_dict['sub_domains'])
    write_to_file('potential_sub_domains.txt', sub_domains_dict['potential_sub_domains'])
