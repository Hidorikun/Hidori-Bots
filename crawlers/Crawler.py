import urllib.robotparser


class Crawler:

    def __init__(self, robots_url, polite=True):
        self.robots = urllib.robotparser.RobotFileParser()
        self.robots.set_url(robots_url)
        self.polite = polite

