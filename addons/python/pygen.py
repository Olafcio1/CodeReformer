import os

from reformer.resources import ResourceManager

from reformer.app.home.new_project.Generator import Generator

from reformer.util.settings.Category import Category
from reformer.util.settings.set_value.BoolValue import BoolValue

class PythonGenerator(Generator):
    model = Category("model",
                           **{"use 'src' folder": BoolValue(True)})

    __metadata__ = {
        "name": lambda: "Python",
        "icon": lambda: ResourceManager.image['/image/generator/python.png']
    }

    def create(self, path: str) -> None:
        useSrcModel = self.model.settings["use 'src' folder"].value.value

        if useSrcModel:
            os.makedirs(path)
            os.makedirs(root := (path + "/src"))

            with open(root + "/main.py", "w", encoding="utf-8") as f:
                f.write(f"""
                        def main():
                            print("Hello, World!")

                        main()
                        """.replace("                        ", "").lstrip())

            with open(path + "/__main__.py", "w", encoding="utf-8") as f:
                f.write(f"""
                        from src import main as _
                        """.replace("                        ", "").lstrip())
        else:
            os.makedirs(path)

            with open(path + "/main.py", "w", encoding="utf-8") as f:
                f.write(f"""
                        def main():
                            print("Hello, World!")

                        main()
                        """.replace("                        ", "").lstrip())
