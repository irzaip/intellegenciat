import aiml
k = aiml.Kernel()
k.learn("../pyaiml/std-startup.xml")
k.respond("LOAD AIML IRZA")
while True: print k.respond(raw_input("> "))

