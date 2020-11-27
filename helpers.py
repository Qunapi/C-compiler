clauseLabelNumber = 0
clauseEndNumber = 0

def createClauseLabel():
    global clauseLabelNumber
    result = f"clause_{clauseLabelNumber}"
    clauseLabelNumber += 1
    return result

def createEndLabel():
    global clauseEndNumber
    result = f"end_{clauseEndNumber}"
    clauseEndNumber += 1
    return result