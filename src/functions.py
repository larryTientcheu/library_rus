from werkzeug.security import generate_password_hash, check_password_hash

class Functions:
    def __init__(self) -> None:
        pass

    def hashPassword(self, password):
        hashed = generate_password_hash(password)
        return hashed

    
    def checkPassword(self, hashed, password):
        result = check_password_hash(hashed, password)
        return result

    def calculateFine(self, returnDate, issueDate):
        base = 500
        diff = returnDate - issueDate
        fine = base*diff
        return fine