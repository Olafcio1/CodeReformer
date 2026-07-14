import os
import string

from reformer.resources import ResourceManager

from reformer.app.home.new_project.Generator import Generator

from reformer.util.settings.Category import Category
from reformer.util.settings.set_value.StringValue import StringValue
from reformer.util.settings.set_value.BoolValue import BoolValue
from reformer.util.settings.set_value.PickValue import PickValue

class CSharpGenerator(Generator):
    general = Category("general",
                             namespace = StringValue(lambda str: str[0] in string.ascii_letters and not any([ch not in (string.ascii_letters + string.digits) for ch in str])))

    codeStyle = Category("code style",
                               nullable       = BoolValue(True),
                               implicitUsings = BoolValue(True))

    compiling = Category("compiling",
                               outputType = PickValue(0, [".exe", ".dll"]),
                               **{".NET version": PickValue(0, ["net10.0"])})

    __metadata__ = {
        "name": lambda: "C#",
        "icon": lambda: ResourceManager.image['/image/generator/csharp.png']
    }

    def create(self, path: str, name: str) -> None:
        namespace = self.general.settings['namespace'].value.value

        os.makedirs(path)

        with open(path + "/%s.csproj" % name, "w", encoding="utf-8") as f:
            f.write(f"""
                    <Project Sdk="Microsoft.NET.Sdk">

                      <PropertyGroup>
                        <OutputType>{self.compiling.settings['outputType'].value.value[1:].capitalize()}</OutputType>
                        <TargetFramework>{self.compiling.settings['.NET version'].value.value}</TargetFramework>
                        <ImplicitUsings>{'enable' if self.codeStyle.settings['implicitUsings'].value.value else 'disable'}</ImplicitUsings>
                        <Nullable>{'enable' if self.codeStyle.settings['nullable'].value.value else 'disable'}</Nullable>
                      </PropertyGroup>

                    </Project>
                    """.replace("                    ", "").lstrip())

        with open(path + "/%s.slnx" % name, "w", encoding="utf-8") as f:
            f.write(f"""
                    <Solution>
                      <Project Path="{name}.csproj" />
                    </Solution>
                    """.replace("                    ", "").lstrip())

        with open(path + "/Program.cs", "w", encoding="utf-8") as f:
            f.write(f"""
                    namespace {namespace} {{
                        public class Program {{
                            static void Main(string[] args) {{
                                Console.OutputEncoding = Encoding.UTF8;

                                Console.WriteLine("-=- welcome to code reformer. -=-");
                            }}
                        }}
                    }}
                    """.replace("                    ", "").lstrip())
