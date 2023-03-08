# 1 - Documentation's Correction            ----------------------------------------------------

def corrigir_palavra(word: str) -> str:
    """
    This function takes a string (potentially modified by a burst of letters) and
    returns the resulting string from removing the adjacent lowercase/uppercase pairs of the same letter,
    over and over, until there aren't any pairs of this nature left to remove.


    :param word: str
    :return: str
    """


    # The variable was_removed was made for looping the removal of adjancent lowercase/uppercase pairs of the same letter,
    # until no pair is removed for one passage (in which case, was_removed = False, closing the while loop).

    words_list = list(word)
    corrected_word = ""
    was_removed = True
    while was_removed == True:

        was_removed = False
        letter_order = 0

        # The letter_order is gonna be incremented by 1 until it references every pair of adjacent characters in the string

        while letter_order < len(words_list) - 1:

            # Verifies if two adjacent characters are of different capitalization (lower/upper or upper/lower)
            # Then if two adjacent characters are of the same letter (by making them lowercase, to disregard capitalization)

            if words_list[letter_order].islower() != words_list[letter_order + 1].islower()\
            and words_list[letter_order].lower() == words_list[letter_order + 1].lower():
                del words_list[letter_order:letter_order + 2]
                was_removed = True

            letter_order += 1

    for letter in words_list:
        corrected_word += letter
    return corrected_word




def eh_anagrama(word1: str, word2: str) -> bool:
    """
    This function takes two strings and returns True if and only if they are anagrams,
    that is, if the words are constituted by the same letters, ignoring capitalization differences
    and the order of the letters.


    :param word1: str
    :param word2: str
    :return: bool
    """


    # This part of the function saves the strings' characters in lists - one for each string - all converted to lowercase,
    # then it orders said lists, for anagrams' lists not to differ by capitalization nor order of the letters.

    word1_listed = list(word1.lower())
    word2_listed = list(word2.lower())

    word2_listed.sort()
    word1_listed.sort()

    # This way, when comparing word1_listed and word2_listed, the only thing analysed is the frequency of each character in each string.

    if word1_listed == word2_listed:
        return True
    else:
        return False




def corrigir_doc(phrase: str) -> str:
    """
        This function receives a string with BDB documentation errors and returns the filtered string
        with the corrected words and the second terms of anagrams that correspond to different words removed,
        leaving only their first occurrence. This function checks the validity of the argument, generating
        a ValueError with the message ‘correct doc: argument invalid’ if its argument is not valid. For this purpose,
        it's considered: that the words can only be separated by a single space; that the text is formed by
        one or more words; and that each word is made up of at least one letter.


        :param phrase: str
        :return: str
        """


    # It is verified if: there isn't more than one space in a row, if there isn't anything but spaces and letters,
    # and if there aren't spaces before or after the phrase. And if any of these isn't met, an error is raised

    if type(phrase) != str or len(phrase) == 0:
        raise ValueError("corrigir_doc: argumento invalido")
    if not(phrase[0].isalpha() and phrase[len(phrase) - 1].isalpha()):
        raise ValueError("corrigir_doc: argumento invalido")
    spacebar_counter = 0
    for character in phrase:
        if character == " ":
            if spacebar_counter == 0:
                spacebar_counter = 1
            elif spacebar_counter == 1:
                raise ValueError("corrigir_doc: argumento invalido")
        elif character.isalpha():
            spacebar_counter = 0
        else:
            raise ValueError("corrigir_doc: argumento invalido")

    words_list = phrase.split()

    # The words are corrected by "corrigir_palavra()" and then added to a list

    corrected_words_list = []
    for word in words_list:
        corrected_words_list.append(corrigir_palavra(word))

    # The following lines compute all the combinations of two different indexes from "corrected_words_list"

    index1 = 0
    index2 = index1 + 1
    if index2 == len(corrected_words_list):
        index2 = index1 + 1
    while index1 < len(corrected_words_list):
        if index2 == len(corrected_words_list):
            index1 += 1
            index2 = index1 + 1

    # The words related to the computed indexes are tested for being anagrams but different words, if so,
    # the second one is deleted from the list

        elif eh_anagrama(corrected_words_list[index1], corrected_words_list[index2]) and corrected_words_list[index1].lower() != corrected_words_list[index2].lower():
            del corrected_words_list[index2]

        else:
            index2 += 1

    # One by one, the words from the list are added to a string, each word is followed by a space, that,
    # in the last word's case, is then deleted

    corrected_words_phrase = ""
    for word in corrected_words_list:
        corrected_words_phrase += (word + " ")
    corrected_words_phrase = corrected_words_phrase[:len(corrected_words_phrase) - 1]

    return corrected_words_phrase




# 2 - PIN's Discovery                       ----------------------------------------------------

def obter_posicao(direction: str, digit: int) -> int:
    """
    This function takes one string containing one character that represents the direction of one movement
    ("C", "B", "E" or "D") and an int representing the current position (any digit from 1 to 9); it must return
    the digit that corresponds to the new position.
        Note that "C", "B", "E" and "D" correlate to up, down, left and right, respectively.


    :param direction: str
    :param digit: int
    :return: int
    """


    # To keep track of the limits of the pad (so, per example, we don't "go right" from the digit "3")
    # we determine the line and col in which the digit is

    if digit <= 3:
        line = 1
        col = digit
    elif digit <= 6:
        line = 2
        col = digit - 3
    else:
        line = 3
        col = digit - 6

    # The new digit and its line/column are computed

    if direction == "C" and line > 1:
        line -= 1
        digit -= 3
    if direction == "B" and line < 3:
        line += 1
        digit += 3
    if direction == "D" and col < 3:
        col += 1
        digit += 1
    if direction == "E" and col > 1:
        col -= 1
        digit -= 1
    return digit




def obter_digito(directions, digit):
    """
    This function takes one string containing one or more movements, and one int corresponding to the initial position
    in the pad; then, it returns the resulting digit from executing every movement present in the directions string.


    :param direction: str
    :param digit: int
    :return: int
    """


    for letter in directions:
        digit = obter_posicao(letter, digit)
    return digit




def obter_pin(instructions: tuple) -> tuple:
    """
        This function takes one tuple containing between 4 and 10 movement sequences, returning the tuple of ints
        containing the codified pin, accordingly to the "instructions" tuple. This tuple's elements must be strings
        with 1 or more characters from ("C", "B", "E", "D"), raising a ValueError if not.


        :param instructions: tuple
        :return: tuple
    """


    # Verify if the "instrction"'s type is tuple, and if it has the right length; if not, raise an error

    if type(instructions) != tuple or not 4 <= len(instructions) <= 10:
        raise ValueError("obter_pin: argumento invalido")

    # Taking the digit 5 as the starting point, get the resulting digit from following the directions given in each step

    digit = 5
    pin = ()
    for directions in instructions:
        if type(directions) != str or len(directions) == 0:
            raise ValueError("obter_pin: argumento invalido")
        digit = obter_digito(directions, digit)

        # Before following the next instruction, create a new "pin" tuple with the added digit

        pin += (digit,)
        for letter in directions:
            if letter not in ("B", "E", "C", "D"):
                raise ValueError("obter_pin: argumento invalido")
    return pin




# 3 - Data Verification                     ----------------------------------------------------

def eh_entrada(bdb_entry: any) -> bool:
    """
        This function takes any argument and returns True only if that argument follows BDB entry's rules,
        which means: it has to be a tuple of length 3, being its elements (in order), a cypher, a checksum
        and a safety sequence. The cypher has to be a string with lowercase letters, potentially separated by hyphens;
        the checksum has to be a string composed of a "[" character, followed by five lowercase letters,
        followed by a "]" character; the safety sequence has to be a tuple, which elements must be natural numbers.


        :param bdb_entry: any
        :return: bool
    """


    # Verify if bdb_entry's type and length are the desired ones

    if type(bdb_entry) == tuple and len(bdb_entry) == 3:
        cypher = bdb_entry[0]
        checksum = bdb_entry[1]
        nums = bdb_entry[2]
    else:
        return False

    # Verify if cypher is a string that isn't empty, and which first and last characters are letters (being that,
    # per example, "-abc-" isn't a valid "cypher")

    if type(cypher) != str or len(cypher) == 0  or not cypher[0].isalpha() or not cypher[len(cypher)-1].isalpha():
        return False

    # Verify if all characters are either "-" or any lowercase letter

    for element in cypher:
        if element != "-" and not (element.isalpha() and element == element.lower()):
            return False

    # Verify if there aren't any adjacent hyphens

    for index in range(0, len(cypher) - 1):
        if cypher[index] == cypher[index + 1] == "-":
            return False

    if type(checksum) != str:
        return False

    # Verify if: the first character is "[", the last one is "]", between them there are 5 lowercase letters

    if not (checksum[0]== "[" and checksum[len(checksum) - 1] == "]" and len(checksum) == 7):
        return False

    for element in checksum[1: len(checksum)-1]:
        if not (element.isalpha() and element == element.lower()):
            return False

    if type(nums) != tuple or len(nums) < 2:
        return False

    # Verify if numbers in the tuple "nums" are natural

    for element in nums:
        if type(element) != int or element <= 0:
            return False
    return True




def validar_cifra(cypher: str, checksum: str) -> bool:
    """
        This function receives two strings, corresponding to a cypher and a checksum; it returns True only if
        the checksum is valid for the given cypher.


        :param cypher: str
        :param checksum: str
        :return: bool
    """


    # Create a dictionary that keeps the frequency of each letter in the cypher

    d = {}
    for letter in cypher:
        if letter != "-":
            if "{}".format(letter) in d.keys():
                d["{}".format(letter)] += 1
            else:
                d["{}".format(letter)] = 0

    # Create list for the frequencies in order, and one to save (later) the letters sorted by frequency (from max to min)
    # and, in the case of letters with the same frequency, alphabetically, between them

    ordered_frequencies = sorted(d.values(), reverse=True)
    ordered_letters = []

    # Add the letter with max frequency, delete it from the "ordered_frequencies" list, and repeat,
    # in order to end up with a list of letters sorted by frequency - ordered_letters

    for letter in d.keys():
        ordered_letters += [key for key, value in d.items() if value == max(ordered_frequencies)]
        ordered_frequencies.remove(max(ordered_frequencies))

    # Remove the duplicates - obtained by adding letters with the same frequency
    # once there are letters that verify the condition value == max(ordered_frequencies) multiple times

    ordered_letters = list(dict.fromkeys(ordered_letters))

    # The compare_list's objective is to allow us to verify if there were changes to the list's order
    # If not, the while loop won't change anything else, so it is stopped

    compare_list = []

    # For letters that have the same frequency (in the cypher): order them alphabetically

    while compare_list != ordered_letters:
        compare_list = ordered_letters.copy()
        cond_2ndlap = False
        for index in range(0, len(ordered_letters)-1):
            letter1 = ordered_letters[index]
            letter2 = ordered_letters[index + 1]
            if d[letter1] == d[letter2]:
                temp_list = [letter1, letter2]
                temp_list2 = temp_list.copy()
                temp_list.sort()
                ordered_letters[index] = temp_list[0]
                ordered_letters[index + 1] = temp_list[1]


    # Verify if (disregarding the brackets) the letters in the checksum are equal to the ones in the ordered_letters
    # If so, the cypher is validated by the checksum

    if list(checksum[1: 6]) == ordered_letters[:5]:
        return True
    else:
        return False




def filtrar_bdb(entries_group: list) -> list:
    """
        This function receives a list containing one or more BDB entries and returns a list containing
        those in which the checksum isn't coherent with the respective cypher, in the same order as the original.
        This function should verify its arguments, raising a ValueError if they aren't valid.


        :param entries_group: list
        :return: list
    """


    list_verified = []

    # If entries_group is not a list, or is an empty list, or if one of the BDB entries isn't validated by "eh_entrada"
    # an error must be raised

    if isinstance(entries_group, list) and len(entries_group) != 0:
        for bdb in entries_group:
            if eh_entrada(bdb):

                #bdb[0] and bdb[1] refer to a cypher and a checksum, respectively
                if not validar_cifra(bdb[0], bdb[1]):
                    list_verified.append(bdb)
            else:
                raise ValueError("filtrar_bdb: argumento invalido")
    else:
        raise ValueError("filtrar_bdb: argumento invalido")
    return list_verified




# 4 - Data Decryption                       ----------------------------------------------------

def obter_num_seguranca(nums: tuple) -> int:
    """
        This function receives a tuple containing natural numbers and returns the security number (the minimum positive
        difference between all the combinations of two numbers from the tuple).


        :param nums: tuple
        :return: int
    """


    # Sort all the numbers, to compute the differences a - b, with a > b, always. So we don't worry with negative results
    nums = list(nums)
    nums.sort(reverse = True)
    index1 = 0
    index2 = index1 + 1
    cond = True

    # Compute all combinations of two numbers from the tuple "nums", with the variation of index1 and index2
    # Calculate all differences, and maintain the lowest one
    # The bool "cond" is set to True, for the first passage, allowing us to define the first value for "difference"

    while index1 < len(nums) - 1:

        # If index2 corresponds to the last number in the tuple
        if index2 == len(nums) - 1:

            temp_difference = nums[index1] - nums[index2]       # Temporary difference that will be compared to the lowest

            if cond == True:
                difference = temp_difference

            cond = False                                        # The condition is set to False, so it doesn't
            difference = min(difference, temp_difference)       # interfere with the next passages
            index1 += 1
            index2 = index1 + 1

        else:
            temp_difference = nums[index1] - nums[index2]       # Temporary difference that will be compared to the lowest

            if cond == True:
                difference = temp_difference

            cond = False                                        # The condition is set to False, so it doesn't
            difference = min(difference, temp_difference)       # interfere with the next passages
            index2 += 1
    return difference




def decifrar_texto(cypher: str, num_seguranca: int) -> str:
    """
        This function receives a string containing a cypher and a security number, and switches each letter,
        going forward in the alphabet a number of times equal to each entry's security number, plus one for even positions,
        and minus one for odd positions in the text.


        :param cypher: str
        :param num_seguranca: int
        :return: str
    """


    # The following list serves the purpose of later in the code being able to go forward and backwards in the alphabet,
    # by using the letter's index in the list

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    final_text = ""
    index = 0

    for character in cypher:
        if character == "-":
            final_text += " "
            index += 1

        # If the position is odd

        elif index % 2 == 0:
            newposition = (alphabet.index(character) + num_seguranca + 1) % 26  # By taking the remainder (in "% 26")
            final_text += alphabet[newposition]                                 # we take out the full laps around
            index += 1                                                          # the alphabet list

        # If the position is even

        elif index % 2 == 1:
            newposition = (alphabet.index(character) + num_seguranca - 1) % 26
            final_text += alphabet[newposition]
            index += 1

    return final_text




def decifrar_bdb(lista_bdb: list) -> list:
    """
        This function receives a list containing one or more BDB entries and returns a list of equal length,
        containing the deciphered entries' text, in the same order.
        This function also verifies if the argument is valid, returning a ValueError if it isn't.


        :param lista_bdb: list
        :return: list
    """


    deciphered_list = []
    # If the argument is invalid, raise a ValueError
    if len(lista_bdb) == 0 or type(lista_bdb) != list:
        raise ValueError("decifrar_bdb: argumento invalido")
    for bdb in lista_bdb:
        if not eh_entrada(bdb):
            raise ValueError("decifrar_bdb: argumento invalido")

    # If the argument is valid, correct the entry, and append to a list
        else:
            cypher = bdb[0]
            checksum = bdb[1]
            nums = bdb[2]
            security_number = obter_num_seguranca(nums)
            text = decifrar_texto(cypher, security_number)
            deciphered_list.append(text)
    return deciphered_list




# 5 - Password Debbuging                    ----------------------------------------------------

def eh_utilizador(user_dictionary: any) -> bool:
    """
        This function receives any argument and returns True only if it's a dictionary that contains
        the user's BDB information: name, password and individual rule. Names and passwords have a minimum
        length of 1, and can contain any character.


        :param user_dictionary: any
        :return: bool
    """


    # Validate type and length of the argument

    if not isinstance(user_dictionary, dict) or len(user_dictionary) != 3:
        return False

    # Verify the existence of the requested keys in the dictionary

    keyslist_dictionary = []
    keyslist_rule = []
    for key in user_dictionary:
        keyslist_dictionary.append(key)
    for key in user_dictionary["rule"]:
        keyslist_rule.append(key)
    keyslist_rule.sort()
    keyslist_dictionary.sort()

    if keyslist_dictionary != ["name", "pass", "rule"] or \
            keyslist_rule != ["char", "vals"]:
        return False


    # Validate type and length of "rule"'s value

    elif not isinstance(user_dictionary["rule"], dict) or len(user_dictionary["rule"]) != 2:
        return False

    # Validate type and length of "vals"'s value

    elif not isinstance(user_dictionary["rule"]["vals"], tuple) or len(user_dictionary["rule"]["vals"]) != 2:
        return False

    # Validate type and length of "vals"'s elements

    elif not isinstance(user_dictionary["rule"]["vals"][0], int) or not isinstance(user_dictionary["rule"]["vals"][1], int):
        return False
    elif not (user_dictionary["rule"]["vals"][0] >= 0 and user_dictionary["rule"]["vals"][1] >= user_dictionary["rule"]["vals"][0]):
        return False

    # Validate type and length of "char"'s value

    elif not (isinstance(user_dictionary["rule"]["char"], str) and len(user_dictionary["rule"]["char"]) == 1)\
            or user_dictionary["rule"]["char"].isupper() or not user_dictionary["rule"]["char"].isalpha():
        return False

    # Validate type and length of "name"'s value

    elif not (isinstance(user_dictionary["name"], str) and len(user_dictionary["name"]) != 0):
        return False

    # Validate type and length of "pass"'s value

    elif not (isinstance(user_dictionary["pass"], str) and len(user_dictionary["pass"]) != 0):
        return False
    return True




def eh_senha_valida(password: str, rule: dict) -> bool:
    """
        This function receives a string regarding a password, and a dictionary regarding the individual
        rule of the password's creation. It must return True if the password meets all the rules defined:
        both general rules and individual ones.
        General rules are:  containing at least 3 lowercase letters;
                            there must be at least two adjacent letters that are equal to each other.
        Individual rule:    the rules sets a character and two natural numbers, x and y; being that
                            the frequency of that character in the password must be in the interval [x, y]


        :param password: str
        :param rule: dict
        :return: bool
    """


    lowest = rule["vals"][0]
    highest = rule["vals"][1]
    char = rule["char"]
    vowels = ["a", "e", "i", "o", "u"]
    num_vowels = 0
    condition = False
    char_count = 0
    character_temp = ""

    # Validate "vals"'s elements' type and length

    if type(lowest) != int or type(highest) != int or not (lowest >= 0 and highest >= 0):
        return False

    # Verify if char is a lowercase letter

    if char.isupper() or type(char) != str:
        return False

    # Verify all rules listed

    for character in password:
        if character in vowels:
            num_vowels += 1
        if character == character_temp:
            condition = True
        if character == char:
            char_count += 1
        character_temp = character
        temporary = False

    # If any rule isn't met, return False

    if not (num_vowels >= 3 and lowest <= char_count <= highest and condition == True):
        return False

    return True




def filtrar_senhas(entries_list: list) -> list:
    """
        This function receives a list containing one or more dictionaries regarding BDB entries, as described before.
        It must return an alphabetically ordered list containing the names of the users whose passwords are wrong.
        The function also checks if the argument is valid, raising a ValueError otherwise.


        :param entries_list: list
        :return: list
    """


    faulty_entries_list = []

    # Validate the argument's type and length

    if type(entries_list) != list or len(entries_list) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")

    for entry in entries_list:

        if not eh_utilizador(entry):                                # If any dictionary is not valid
            raise ValueError("filtrar_senhas: argumento invalido")

        elif not eh_senha_valida(entry["pass"], entry["rule"]):     # If a password isn't correct
            faulty_entries_list.append(entry["name"])               # the name of the respective user is
    faulty_entries_list.sort()                                      # appended to a list.
    return(faulty_entries_list)
