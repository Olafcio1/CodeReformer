import pygame
import colour
import string
import os

from .new_project.NewProjectScreen import NewProjectScreen
from .vsc_clone.CloneScreen import CloneScreen
from ..settings.SettingsScreen import SettingsScreen
from ..project.ProjectScreen import ProjectScreen

from ...resources import ResourceManager

from ...lib.screen.Screen import Screen
from ...lib.screen.widget.Initializable import Initializable
from ...lib.screen.widget.ClippedWidget import ClippedWidget
from ...lib.screen.widget.Container import Container, Text

from ...lib.static.StaticRendering import StaticRendering
from ...lib.static.RGB import RGB

from typing import Callable

class HomeScreen(Screen):
    class Background(Initializable):
        def render(self, surface: pygame.Surface) -> None:
            super().render(surface)

            grad = pygame.Surface((1, 2))
            grad.set_at((0, 0), 0x252625)
            grad.set_at((0, 1), 0x111211)
            grad = pygame.transform.smoothscale(grad, surface.get_size())

            surface.blit(grad, (0, 0))

    class Logo(ClippedWidget):
        def renderClipped(self, surface: pygame.Surface) -> None:
            texture = pygame.transform.smoothscale(
                ResourceManager.image['/image/logo.png'],
                self.get_size()
            )

            surface.blit(texture, (0, 0))
            pygame.draw.rect(surface, 0x202120, self.get_clipped_rect(), 1)

    class Button(ClippedWidget):
        text: str
        onClick: Callable[[], None]

        def __init__(
                self,
                /,
                x: int, y: int,
                width: int, height: int,
                *,
                text: str,
                onClick: Callable[[], None]
        ):
            super().__init__(x, y, width, height)

            self.text = text
            self.onClick = onClick

        def renderClipped(self, surface: pygame.Surface) -> None:
            # opera-gx style colors: #2c2a2a, #2f2d2d
            # think of making an opera like theme for this.
            # however, would a red IDE look good?
            # an orange one does (imo) - i use `Bearded Theme Coffee` for `VS Code`

            rad = 15

            for y in range(self.height):
                r = 0

                if y <= rad:
                    r = rad - y
                elif y >= self.height - rad:
                    r = self.height - y  # The logic here is broken, but it looks good, so...

                for x in range(r, self.width - r*2):
                    surface.set_at((x, y), 0x2a2a2a)

            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.text)

            surface.blit(font.render(self.text, True, 0x69696fff if self.isHovered() else 0x59595fff), ((self.width - size[0])/2, (self.height - size[1])/2))

        def getText(self) -> str:
            return self.text

        def mousePressed(self, x: int, y: int, button: int) -> None:
            if self.isHovered(x, y):
                self.onClick()

    def init(self) -> None:
        self.addRenderable(HomeScreen.Background())
        self.addREWidget(HomeScreen.Logo(
            (int) (self.width/14),
            (int) (self.height/7),
            (int) (1024/4.4), (int) (383/4.4)
        ))

        self.addREWidget(btns := Container(
            (int) (self.width/14),
            (int) (self.height/7 + 403/4.4 - 1),
            (int) (1024/4.4),
            (int) (200)
        ).style
            .display("grid")
            .gap(8)
            .paddingTop(8)
         .back)

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="New Project", onClick=HomeScreen.Actions.newProject)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Open Project", onClick=HomeScreen.Actions.openProject)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Clone from VSC", onClick=HomeScreen.Actions.cloneFromVSC)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Settings", onClick=HomeScreen.Actions.openSettings)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        self.addREWidget(projects := Container(
            (int) (self.width/14 + 1024/4.4),
            (int) (self.height/7),
            (int) (self.width - (self.width/14 + 1024/4.4)),
            (int) (self.height - (self.height/7))
        ).style
            .display("grid")
            .gap(8)
            .paddingLeft(16)
         .back)

        projectsDir = os.path.expanduser("~/CodeReformerProjects")
        projectList = os.listdir(projectsDir)

        for proj in projectList:
            projEl = Container(
                (int) (self.width - (self.width/14 + 1024/4.4)) - 16 - 36,  # 16=paddingLeft, 36=paddingRight
                (int) (30 + 8 + 8)
            )

            projEl.style.display("flex")
            projEl.style.gap(8)
            projEl.style.background(0x3a3a3a)  # 0x4a4a4a on hover
            projEl.style.marginRight(36)
            projEl.style.padding((8, 8, 8, 8))

            projEl.text = Text(
                text  = proj,
                color = 0xafafafff,
                font  = ResourceManager.font["/font/LEXEND.TTF"],
                align = "left"
            )

            # TODO: Custom project icons
            # TODO: Extremely customizable icon behaviour
            #
            # Q1: What do you prefer?
            #     a) Performance  -> load all icons on start-up;                                             [good if you want the fastest experience. needs much ram]
            #     b) Battery      -> load icons lazily when neccessary, unload after a short period of time; [good if you don't want to spend an overly amount of ram]
            #     c) Balance      -> load most icons on start-up, unload most with time while in a project;  [a balance between the two. good for most people]
            #     robot)
            #            {Low Battery/High RAM="Battery"}
            #            {Medium CPU=          "Balance"}
            #
            #            <Should "Performance" be never picked?>
            #            <I think so.>
            #
            #            [Tip: "Picks the best option dynamically for you."]
            #
            # Q2: What do you prefer?  (only if creating those icons is expensive)
            #     a) Disk space   -> create icons dynamically; [good if you have a ton of things on your pc]
            #     b) Load time    -> store icons on disk;      [good if you're not a patient guy]
            #
            # Q3: What do you prefer?  (only visible when Q1 isn't "Performance")
            #     a) Completeness -> doesn't show menus that have not fully loaded yet; [good for video]
            #     b) Action       -> shows not fully-loaded menus;                      [good for practical use]
            #
            # Q2 is non-applicable to custom project icons.
            # Q2 would only make sense if the icons were:
            #
            # 1. on disk, but archived; or
            # 2. on the internet.
            #
            # This could be applied to all image resources in the app, too;
            #   however, that would require heavy modifications to
            #   the ResourceManager.

            iconText = ""

            for ch in proj:
                if ch in (string.digits + string.ascii_letters):
                    iconText += ch
                    break

            lastUp: str = ""

            for ch in proj:
                if ch.isupper():
                    lastUp = ch

            if lastUp == "":
                lastUp = proj[-1]

            iconText += lastUp

            projectDir = projectsDir + "/" + proj + "/.reformer/Project Color"

            try:
                with open(projectDir, "r", encoding="utf-8") as f:
                    accentColor = f.read()
            except Exception as e:
                accentColor = "0|0|0.31"

            accentHSL = [float(inp) for inp in accentColor.split("|")]

            icon = Container(30, 30)
            icon.text = Text(
                text  = iconText,
                color = RGB(colour.hsl2rgb((accentHSL[0], min(1, accentHSL[1] * 1.202, accentHSL[1] + (15/100)), min(1, accentHSL[2] + (13/100))))),
                font  = ResourceManager.font["/font/LEXEND.TTF"],
            )

            icon.style.background(RGB(colour.hsl2rgb(accentHSL)))

            projEl.insert(icon, 0)
            projEl.child(1).wrap() \
                           .style(display = "grid", marginTop = 5)

            projEl.mousePressed = lambda _, x, y: StaticRendering.setScreen(ProjectScreen(projectDir))

            projects.addREWidget(projEl)

    class Actions:
        @classmethod
        def newProject(cls) -> None:
            StaticRendering.setScreen(NewProjectScreen())

        @classmethod
        def openProject(cls) -> None:
            raise NotImplemented

        @classmethod
        def cloneFromVSC(cls) -> None:
            StaticRendering.setScreen(CloneScreen())

        @classmethod
        def openSettings(cls) -> None:
            StaticRendering.setScreen(SettingsScreen())

StaticRendering.setHomeScreen = lambda: StaticRendering.setScreen(HomeScreen())
