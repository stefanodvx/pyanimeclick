import json

class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return f"<class 'pyanimeclick.types.{self.__name__}'>"

class Object(metaclass=Meta):
    @staticmethod
    def default(obj: "Object"):
        return {
            key: value if not isinstance(value, list) else "[...]"
            for key, value in obj.__dict__.items()
        }

    def __str__(self) -> str:
        return json.dumps(
            self,
            indent=4,
            default=Object.default,
            ensure_ascii=False
        )