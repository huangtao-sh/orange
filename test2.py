def __getattr__(name):
    if name in ('abc'):
        print(name,'-pk')
        return "I am hunter."
    else:
        pass
