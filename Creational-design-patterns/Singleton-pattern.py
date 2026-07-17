class Remote:
    _the_only_remote=None
    def __new__(cls):
        if(cls._the_only_remote==None):
            print("Making the new remote")
            cls._the_only_remote=super().__new__(cls)
        else:
            print('remote already exists!!')
        return cls._the_only_remote
    def __init__(self):
        self.channel=1
    def set_channel(self,channel):
        self.channel=channel

# As there exists only one remote for a TV, 
# therefore everyone has access to only one remote.

remote1=Remote()
remote2=Remote()

remote1.set_channel(4);
print(remote2.channel)
print(remote1 is remote2)

