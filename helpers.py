clause_label_number = 0
clause_end_number = 0
clause_false_branch_label = 0
clause_post_conditional_number = 0
clause_while_start_number = 0
clause_while_end_number = 0
clause_for_start_number = 0
clause_for_end_number = 0
clause_for_post_expression_number = 0


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


def create_false_branch_label():
    global clause_false_branch_label
    result = f"false_branch_{clause_false_branch_label}"
    clause_false_branch_label += 1
    return result


def create_post_conditional_number():
    global clause_post_conditional_number
    result = f"post_conditional_{clause_post_conditional_number}"
    clause_post_conditional_number += 1
    return result


def create_clause_while_start_number():
    global clause_while_start_number
    result = f"while_start_{clause_while_start_number}"
    clause_while_start_number += 1
    return result


def create_clause_while_end_number():
    global clause_while_end_number
    result = f"while_end_{clause_while_end_number}"
    clause_while_end_number += 1
    return result


def create_clause_for_start_number():
    global clause_for_start_number
    result = f"for_start_{clause_for_start_number}"
    clause_for_start_number += 1
    return result


def create_clause_for_end_number():
    global clause_for_end_number
    result = f"for_end_{clause_for_end_number}"
    clause_for_end_number += 1
    return result


def create_clause_for_post_expression_number():
    global clause_for_post_expression_number
    result = f"for_post_expression_{clause_for_post_expression_number}"
    clause_for_post_expression_number += 1
    return result
