from werkzeug.security import generate_password_hash, check_password_hash
from flask_paginate import Pagination, get_page_args

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

    def paginateResults(self, obj,per_page):
        page, _, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
        total = len(obj)
        # per_page = per_page ## line 24 returns per_page and is default set to 10. Below I'm changing the number
        offset = ((page - 1) * per_page)
        paginatedObjs = obj[offset:offset+per_page]
        paginationLength = (offset,len(paginatedObjs)+offset)
        pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstap4')

        return(paginatedObjs, page, per_page, pagination, paginationLength)