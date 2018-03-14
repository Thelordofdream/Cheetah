def store(input, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input, fw)
    fw.close()


def grab(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)