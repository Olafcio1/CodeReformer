import os

from reformer.app.home.new_project.Generator import Generator

from reformer.util.settings.Category import Category
from reformer.util.settings.set_value.StringValue import StringValue

class JavaGenerator(Generator):
    publishing = Category("publishing",
                                groupID    = StringValue(lambda str: "/" not in str),
                                artifactID = StringValue())

    def __init__(self):
        super().__init__("java")

    def create(self, path: str) -> None:
        os.mkdir(path)
        os.makedirs(path + "/src/main/java/" + self.publishing.settings['groupID'].value.replace(".", "/"))
