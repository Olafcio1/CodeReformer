import os

from reformer.resources import ResourceManager

from reformer.app.home.new_project.Generator import Generator

from reformer.util.settings.Category import Category
from reformer.util.settings.set_value.StringValue import StringValue

class JavaGenerator(Generator):
    publishing = Category("publishing",
                                groupID    = StringValue(lambda str: "/" not in str),
                                artifactID = StringValue())

    def __init__(self):
        super().__init__("Java", ResourceManager.image['/image/generator/java.png'])

    def create(self, path: str) -> None:
        groupID = self.publishing.settings['groupID'].value

        os.mkdir(path)
        os.makedirs(root := (path + "/src/main/java/" + groupID.replace(".", "/")))

        with open(root + "/Main.java", "w", encoding="utf-8") as f:
            f.write(f"""
                    package {groupID};

                    public class Main {{
                        public static void main(String[] args) {{
                            System.out.println("-=- welcome to code reformer. -=-");
                        }}
                    }}
                    """.replace("                    ", "").lstrip())
