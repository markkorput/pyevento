from evento import Event

event = Event[str]()


def observer(value: str) -> None:
    print(value)


event("This does nothing.")
event += observer
event("This is printed.")
