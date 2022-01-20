import time, sys, os, json

def hello(params):
    if not "name" in params:
        name = "Undefined"
    else:
        name = params['name']
    time.sleep(5)
    return "Hello, " + name

if __name__=="__main__":
    if len(sys.argv) == 2:
        task_id = sys.argv[1]
    else:
        exit(1)
    
    with open(os.path.join("scripts", "input", task_id + ".json"), "r") as fd:
        params = json.loads(fd.read())
    result = hello(params)
    os.remove(os.path.join("scripts", "input", task_id + ".json"))
    with open(os.path.join("scripts", "output", task_id + ".txt"), "w+") as fd:
        fd.write(result)