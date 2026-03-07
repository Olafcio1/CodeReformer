<center>

# 🌃 Event API
A Code Reformer library project.

</center>

## 💉 Registering listeners
To register a method:

```python
from reformer.util.event import EventManager

def onEvent(event: SampleEvent) -> None:
    print("onEvent invoked")

EventManager.register(onEvent)
```

To register a class:

```python
from reformer.util.event import EventManager, EventHandler
from typing import final

@final
class MyEventListener:
    @EventHandler
    def onEvent(event: SampleEvent) -> None:
        print("onEvent invoked")

EventManager.register(MyEventListener)
```

## 🧬 Creating events
```python
from reformer.util.event import Event

class SampleEvent(Event):
    pass
```

## 📮 Posting an event
```python
from reformer.util.event import EventManager

EventManager.fire(SampleEvent())
```
