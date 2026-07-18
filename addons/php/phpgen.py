import os
import hashlib
import subprocess
import urllib.request as req

from reformer.logger import *
from reformer.resources import ResourceManager

from reformer.app.home.new_project.Generator import Generator

from reformer.util.settings.Category import Category
from reformer.util.settings.set_value.BoolValue import BoolValue

class PHPGenerator(Generator):
    setup = Category("setup",
                           useComposer = BoolValue(False))

    __metadata__ = {
        "name": lambda: "PHP",
        "icon": lambda: ResourceManager.image['/image/generator/php.png']
    }

    def create(self, path: str, name: str) -> None:
        useComposer = self.setup.settings['useComposer'].value.value

        os.makedirs(path)

        if useComposer:
            getlogger() << 'Downloading Composer'

            try:
                req.urlretrieve("https://getcomposer.org/installer", setup := (path + "/composer-setup.php"))
            except:
                getlogger() << 'Failed to download'
                raise

            getlogger() << 'Requesting signature'
            try:
                with req.urlopen("https://composer.github.io/installer.sig") as resp:
                    checksum = resp.readline().decode(errors="ignore")
            except:
                getlogger() << 'Failed to request'
                raise

            with open(setup, 'rb') as f:
                checksumHas = hashlib.file_digest(f, 'sha384').hexdigest()

            if checksum == checksumHas:
                getlogger() << 'Installer verified'

                subprocess.Popen(["php", "composer-setup.php"], shell=True, cwd=path)
            else:
                getlogger() << 'Installer corrupt'

            os.unlink(setup)

        os.makedirs(include := (path + "/#include"))

        with open(include + "/api.php", "w", encoding="utf-8") as f:
            f.write(f"""
                    <?php
                    namespace API;

                    """.replace("                    ", "").lstrip())

        with open(path + "/index.php", "w", encoding="utf-8") as f:
            f.write(f"""
                    <?php
                    require_once './#include/api.php';
                    echo 'Hello, World!';

                    """.replace("                    ", "").lstrip())
