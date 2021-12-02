# class Functions describes the name and a description for available functions
class Functions:
    def __init__(self,id,name,description) -> None:
        self._id=id
        self._name=name
        self._description=description

    @property
    def id(self)->int:
        return self._id

    @property
    def name(self)->str:
        return self._name

    @property
    def description(self)->str:
        return self._description
