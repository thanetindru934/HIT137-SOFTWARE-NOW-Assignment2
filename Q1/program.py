# Q1
# File Encryption & Decryption

ALPHABET_SIZE = 26

#Markers (#, $, @, %) are used to preserve rule information
#so that decryption can correctly reverse the encryption


#Function to shift characters
def shift_character(c, shift):
    if c.islower():
        return chr((ord(c) - ord('a') + shift) % ALPHABET_SIZE + ord('a'))
    elif c.isupper():
        return chr((ord(c) - ord('A') + shift) % ALPHABET_SIZE + ord('A'))
    return c  # Non-alphabet characters unchanged


#Encryption Function
def encrypt_file():
    try:
        with open("raw_text.txt", "r") as infile, open("encrypted_text.txt", "w") as outfile:

            for ch in infile.read():

                #LOWERCASE LETTERS
                if ch.islower():
                    if 'a' <= ch <= 'm':
                        new_char = shift_character(ch, shift1 * shift2)
                        outfile.write(new_char + "#")   # Rule 1 marker
                    else:
                        new_char = shift_character(ch, -(shift1 + shift2))
                        outfile.write(new_char + "$")   # Rule 2 marker

                #UPPERCASE LETTERS
                elif ch.isupper():
                    if 'A' <= ch <= 'M':
                        new_char = shift_character(ch, -shift1)
                        outfile.write(new_char + "@")   # Rule 3 marker
                    else:
                        new_char = shift_character(ch, shift2 ** 2)
                        outfile.write(new_char + "%")   # Rule 4 marker

                #OTHER CHARACTERS
                else:
                    outfile.write(ch)

        print("Encryption done")

    except FileNotFoundError:
        print("raw_text.txt not found")


#Decryption Function (uses markers to reverse correctly)
def decrypt_file():
    try:
        with open("encrypted_text.txt", "r") as infile, open("decrypted_text.txt", "w") as outfile:
            text = infile.read()
            i = 0

            while i < len(text):
                ch = text[i]

                #Check if next character is a marker AND current is letter
                if i + 1 < len(text) and ch.isalpha():
                    marker = text[i + 1]

                    if marker == "#":  # Rule 1
                        new_char = shift_character(ch, -(shift1 * shift2))
                        outfile.write(new_char)
                        i += 2
                        continue

                    elif marker == "$":  # Rule 2
                        new_char = shift_character(ch, (shift1 + shift2))
                        outfile.write(new_char)
                        i += 2
                        continue

                    elif marker == "@":  # Rule 3
                        new_char = shift_character(ch, shift1)
                        outfile.write(new_char)
                        i += 2
                        continue

                    elif marker == "%":  # Rule 4
                        new_char = shift_character(ch, -(shift2 ** 2))
                        outfile.write(new_char)
                        i += 2
                        continue

                #If not a valid marker case -- treat as normal character
                outfile.write(ch)
                i += 1

        print("Decryption done")

    except FileNotFoundError:
        print("encrypted_text.txt not found")

#Verification Function
def verify_decryption():
    try:
        with open("raw_text.txt", "r") as f1, open("decrypted_text.txt", "r") as f2:

            #Exact comparison (IMPORTANT: no strip)
            if f1.read() == f2.read():
                print("Decryption SUCCESS")
            else:
                print("Decryption FAILED")

    except FileNotFoundError:
        print("File missing")


#Main Function
def main():
    global shift1, shift2

    #Take user input
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    #Program flow
    encrypt_file()
    decrypt_file()
    verify_decryption()


if __name__ == "__main__":
    main()