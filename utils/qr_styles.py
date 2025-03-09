from typing import TYPE_CHECKING, Any, Union
from qrcode.image.styles.moduledrawers.base import QRModuleDrawer
from qrcode.image.styledpil import StyledPilImage
from PIL import Image, ImageDraw
from qrcode.main import QRCode
import os
import abc


if TYPE_CHECKING:
    from qrcode.image.base import BaseImage
    from qrcode.main import ActiveWithNeighbors, QRCode

base_path = os.path.dirname(os.path.realpath(__file__))
ANTIALIASING_FACTOR = 4

class StyledPilQRModuleDrawer(QRModuleDrawer):
    """
    A base class for StyledPilImage module drawers.

    NOTE: the color that this draws in should be whatever is equivalent to
    black in the color space, and the specified QRColorMask will handle adding
    colors as necessary to the image
    """

    img: "StyledPilImage"
    
class StarModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules as circles
    """

    circle = None
    
    def __init__(self, keyTest='None'):
        self.keyTest = keyTest
        
    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        box_size = self.img.box_size
        fake_size = box_size * ANTIALIASING_FACTOR
        self.circle = Image.new(
            self.img.mode,
            (fake_size, fake_size),
            self.img.color_mask.back_color,
        )
        ImageDraw.Draw(self.circle).ellipse(
            (0, 0, fake_size, fake_size), fill=self.img.paint_color
        )
        self.circle = self.circle.resize((box_size, box_size), Image.Resampling.LANCZOS)
        

    def drawrect(self, box, is_active: bool):
        if is_active:
            box_size = self.img.box_size
            custom_image = Image.open(f"{base_path}/../img/star.png").resize((10, 10))
            custom_image.resize((box_size, box_size), Image.Resampling.LANCZOS)
            self.img._img.paste(custom_image, (box[0][0], box[0][1]),custom_image)

class BaseEyeDrawer(abc.ABC):
    needs_processing = True
    needs_neighbors = False
    factory: "StyledPilImage2"

    def initialize(self, img: "BaseImage") -> None:
        self.img = img

    def draw(self):
        (nw_eye_top, _), (_, nw_eye_bottom) = (
            self.factory.pixel_box(0, 0),
            self.factory.pixel_box(6, 6),
        )
        (nw_eyeball_top, _), (_, nw_eyeball_bottom) = (
            self.factory.pixel_box(2, 2),
            self.factory.pixel_box(4, 4),
        )
        self.draw_nw_eye((nw_eye_top, nw_eye_bottom))
        self.draw_nw_eyeball((nw_eyeball_top, nw_eyeball_bottom))

        (ne_eye_top, _), (_, ne_eye_bottom) = (
            self.factory.pixel_box(0, self.factory.width - 7),
            self.factory.pixel_box(6, self.factory.width - 1),
        )
        (ne_eyeball_top, _), (_, ne_eyeball_bottom) = (
            self.factory.pixel_box(2, self.factory.width - 5),
            self.factory.pixel_box(4, self.factory.width - 3),
        )
        self.draw_ne_eye((ne_eye_top, ne_eye_bottom))
        self.draw_ne_eyeball((ne_eyeball_top, ne_eyeball_bottom))

        (sw_eye_top, _), (_, sw_eye_bottom) = (
            self.factory.pixel_box(self.factory.width - 7, 0),
            self.factory.pixel_box(self.factory.width - 1, 6),
        )
        (sw_eyeball_top, _), (_, sw_eyeball_bottom) = (
            self.factory.pixel_box(self.factory.width - 5, 2),
            self.factory.pixel_box(self.factory.width - 3, 4),
        )
        self.draw_sw_eye((sw_eye_top, sw_eye_bottom))
        self.draw_sw_eyeball((sw_eyeball_top, sw_eyeball_bottom))

    @abc.abstractmethod
    def draw_nw_eye(self, position): ...

    @abc.abstractmethod
    def draw_nw_eyeball(self, position): ...

    @abc.abstractmethod
    def draw_ne_eye(self, position): ...

    @abc.abstractmethod
    def draw_ne_eyeball(self, position): ...

    @abc.abstractmethod
    def draw_sw_eye(self, position): ...

    @abc.abstractmethod
    def draw_sw_eyeball(self, position): ...


class TriRoundedRectangle(BaseEyeDrawer):
    def draw_nw_eye(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=None,
            width=self.factory.box_size,
            outline="black",
            radius=self.factory.box_size * 2,
            corners=[True, True, False, True],
        )

    def draw_nw_eyeball(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=True,
            outline="black",
            radius=self.factory.box_size,
            corners=[True, True, False, True],
        )

    def draw_ne_eye(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=None,
            width=self.factory.box_size,
            outline="black",
            radius=self.factory.box_size * 2,
            corners=[True, True, True, False],
        )

    def draw_ne_eyeball(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=True,
            outline="black",
            radius=self.factory.box_size,
            corners=[True, True, True, False],
        )

    def draw_sw_eye(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=None,
            width=self.factory.box_size,
            outline="black",
            radius=self.factory.box_size * 2,
            corners=[True, False, True, True],
        )

    def draw_sw_eyeball(self, position):
        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(
            position,
            fill=True,
            outline="black",
            radius=self.factory.box_size,
            corners=[True, False, True, True],
        )


class StyledPilImage2(StyledPilImage):
    def drawrect_context(self, row: int, col: int, qr: QRCode[Any]):
        box = self.pixel_box(row, col)
        if self.is_eye(row, col):
            drawer = self.eye_drawer
            if getattr(self.eye_drawer, "needs_processing", False):
                return
        else:
            drawer = self.module_drawer

        is_active: Union[bool, ActiveWithNeighbors] = (
            qr.active_with_neighbors(row, col)
            if drawer.needs_neighbors
            else bool(qr.modules[row][col])
        )

        drawer.drawrect(box, is_active)

    def process(self) -> None:
        if getattr(self.eye_drawer, "needs_processing", False):
            self.eye_drawer.factory = self
            self.eye_drawer.draw()
        super().process()
