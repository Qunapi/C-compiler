clause_label_number = 0
clause_end_number = 0

def create_clause_label():
    global clause_label_number
    result = f"clause_{clause_label_number}"
    clause_label_number += 1
    return result

def create_end_label():
    global clause_end_number
    result = f"end_{clause_end_number}"
    clause_end_number += 1
    return result