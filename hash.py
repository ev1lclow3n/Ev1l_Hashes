import hashlib
import requests


heart_cat = r"""
 /\_/\  
( o.o ) 
 > ^ <
"""


welcome_message = """
uWu Welcome to the Ev1lclow3n's Hash Cracking Tool!
I can help you with cracking md5 & sha1 hashes without any wordlists.
"""

print(welcome_message)
print(heart_cat)



def fetch_wordlist_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"Failed to fetch the wordlist from {url}. Status code:", response.status_code)
    except requests.RequestException as e:
        print(f"Error fetching the wordlist from {url}:", e)
    return []

def fetch_wordlists_from_urls(urls):
    wordlists = []
    for url in urls:
        wordlist = fetch_wordlist_from_url(url)
        if wordlist:
            wordlists.extend(wordlist)
    return wordlists

def identify_hash_type(hash_string):
    if len(hash_string) == 32:
        return "MD5"
    elif len(hash_string) == 40:
        return "SHA1"
    else:
        return None

def crack_hash(hash_to_crack, wordlist, hash_type):
    for word in wordlist:
        hashed_word = ""
        if hash_type == "MD5":
            hashed_word = hashlib.md5(word.encode()).hexdigest()
        elif hash_type == "SHA1":
            hashed_word = hashlib.sha1(word.encode()).hexdigest()
        
        if hashed_word.lower() == hash_to_crack.lower():
            return word, hash_type  
    return "Hash not found in the wordlist", None


print("\n" * 1)  
user_input = input("Give the file.txt containing hashes or a single hash to crack now: ")
print("\n" * 1)  

wordlist_urls = [
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou-75.txt",
    "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top304Thousand-probable-v2.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/default-passwords.txt",
    "https://pastebin.com/raw/KuTUJPLt"
]

words = fetch_wordlists_from_urls(wordlist_urls)
if words:
    if ".txt" in user_input:
        try:
            with open(user_input, 'r') as file:
                hashes = file.read().splitlines()
                
                cracked_hashes = [] 

                for hash_to_crack in hashes:
                    hash_type = identify_hash_type(hash_to_crack)
                    if hash_type:
                        result, found_hash_type = crack_hash(hash_to_crack, words, hash_type)
                        if result != "Hash not found in the wordlist":
                            cracked_hashes.append(f"{hash_to_crack} : {result} (Type: {found_hash_type})")
                            print(f"Hash: {hash_to_crack} - Cracked: {result} (Type: {found_hash_type})")
                        else:
                            print(f"Hash: {hash_to_crack} - {result}")
                    else:
                        print(f"Hash: {hash_to_crack} - Hash type not supported or unknown.")

                
                with open('cracked.txt', 'w') as output_file:
                    for cracked_hash in cracked_hashes:
                        output_file.write(cracked_hash + '\n')

            print("Cracked hashes saved in cracked.txt file.")
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
    else:
        hash_to_crack = user_input.strip()
        hash_type = identify_hash_type(hash_to_crack)
        if hash_type:
            result, found_hash_type = crack_hash(hash_to_crack, words, hash_type)
            if result != "Hash not found in the wordlist":
                with open('cracked.txt', 'w') as output_file:
                    output_file.write(f"{hash_to_crack} : {result} (Type: {found_hash_type})\n")
                print(f"Hash: {hash_to_crack} - Cracked: {result} (Type: {found_hash_type})")
            else:
                print(f"Hash: {hash_to_crack} - {result}")
        else:
            print("Hash type not supported or unknown.")
else:
    print("Wordlists couldn't be fetched or are empty.")

