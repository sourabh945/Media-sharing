import os


def ls(path:str) -> list[dict]:
    content = []
    content_list = os.listdir(path)
    for i in content_list:
        if os.path.isdir(path+"/"+i) is True:
            content.append([i,"folder"])
        else:
            content.append([i,"file"])
    return content  



