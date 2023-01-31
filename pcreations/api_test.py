# TODO: probably want to rename this file 



def get_token_from_file(filename:str="token.txt") -> str:
    with open(filename, "r") as fp:
        token = fp.read().strip()

    return token
