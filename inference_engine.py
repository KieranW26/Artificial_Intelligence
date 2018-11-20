from urllib.request import urlopen
from lxml import html
import requests
from pyknow import *


class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")

    @Rule(Fact(action='greet'),
          NOT(Fact(name=W())))
    def ask_name(self):
        self.declare(Fact(name=input("What's your name? ")))

    @Rule(Fact(action='greet'),
          NOT(Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where are you? ")))

    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name),
          Fact(location=MATCH.location))
    def greet(self, name, location):
        url = "https://traintimes.org.uk/" + name + "/" + location
        page = requests.get(url)
        tree = html.fromstring(page.content)
        for x in range(5):
            times = tree.xpath('//li[@id="result' + str(x) + '"]/strong[1]/text()')
            print(times)
            price = tree.xpath('//li[@id="result' + str(x) + '"]/small[2]/span[@class="tooltip" and 2]/text()')
            print(price)


engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!
