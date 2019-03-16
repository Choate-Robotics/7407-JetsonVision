from .video_frame import VideoStream as _VideoStream
from .video_frame import AngleDetection as _AngleDetection


class VideoStream(_VideoStream):
    def __init__(self, camera_num: int, width: int = 1080, height: int = 720, quality:int=80):
        super().__init__(camera_num, width, height,quality)

    def getCompressedFrame(self) -> memoryview:
        """
        :return: The processed, JPEG encoded frame with resolution of
                (self.width, self.height) and quality of self.quality
        """
        return memoryview(super().getCompressedFrame())

    @property
    def width(self) -> int:
        return super().getWidth()

    @property
    def height(self) -> int:
        return super().getHeight()

    @property
    def quality(self) -> int:
        return super().getQuality()

    @quality.setter
    def quality(self,quality:int):
        super().setQuaity(quality)

    @property
    def id(self) -> int:
        return super().getId()

    def setResolution(self, width: int) -> None:
        super().setResolution(width)

    def setQuality(self, quality: int):
        super().setQuality(quality)


class AngleDetection(_AngleDetection):
    def __init__(self, camera_num: int, width: int = 1080, height: int = 720,quality:int=80):
        super().__init__(camera_num, width, height,quality)

    def getCompressedFrame(self) -> memoryview:
        """
        :return: The processed, JPEG encoded frame with resolution of
                (self.width, self.height) and quality of self.quality
        """
        return super().getCompressedFrame()

    @property
    def width(self) -> int:
        return super().getWidth()

    @property
    def height(self) -> int:
        return super().getHeight()

    @property
    def quality(self) -> int:
        return super().getQuality()

    @property
    def id(self) -> int:
        return super().getId()

    @property
    def angle(self) -> float:
        return super().getAngle()

    def setResolution(self, width: int) -> None:
        super().setResolution(width)

    def setQuality(self, quality: int):
        super().setQuality(quality)


__all__ = ['AngleDetection', 'VideoStream']
