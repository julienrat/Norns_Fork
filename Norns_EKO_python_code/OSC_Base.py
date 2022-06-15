from uosc.client import Bundle, Client, create_message

osc = Client('10.42.0.1', 10111)

b = Bundle()

b.add(create_message("/params/cutoff", 125))
osc.send(b)
