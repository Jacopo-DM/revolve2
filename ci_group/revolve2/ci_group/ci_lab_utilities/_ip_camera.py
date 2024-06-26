import logging
import queue
import threading
import time

import cv2
import numpy as np
from numpy.typing import NDArray

EXT_KEY = 27


class IPCamera:
    """A general class to steam and record from IP cameras via opencv.

    How to use:

    If you are experiencing XDG_SESSION_TYPE error messages because of wayland use the following code before you start the recording:


    >>> address = "rtsp://<user>:<password>@<ip>:<port (554)>/..."
    >>> camera = IPCamera(camera_location=address, recording_path="<example_path>")
    >>> camera.start(display=True, record=True)

    >>> import os
    >>> os.environ["XDG_SESSION_TYPE"] = "xcb"
    >>> os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    """

    _d_q: queue.Queue[cv2.typing.MatLike]  # Display queue
    _r_q: queue.Queue[cv2.typing.MatLike]  # Record queue
    """Threads for camera functionality."""
    _receive_thread: threading.Thread
    _display_thread: threading.Thread
    _record_thread: threading.Thread

    _camera_location: str  # Location (address) of the camera
    _is_running: bool  # Allows to break threads
    _image_dimensions: tuple[int, int]
    _fps: int
    """Maps to straightening the camera image."""
    _map1: cv2.typing.MatLike
    _map2: cv2.typing.MatLike

    def __init__(
        self,
        camera_location: str,
        recording_path: str | None = None,
        image_dimensions: tuple[int, int] = (1920, 1080),
        distortion_coefficients: NDArray[np.float64] | None = None,
        camera_matrix: NDArray[np.float64] | None = None,
        fps: int = 30,
    ) -> None:
        """Initialize the ip camera.

        :param camera_location: The location of the camera.
        :param recording_path: The path to store the recording.
        :param image_dimensions: The dimensions of the image produced by
            the camera and used for calibration.
        :param distortion_coefficients: The distortion coefficients for
            the camera.
        :param camera_matrix: The camera matrix for calibration.
        :param fps: The FPS of the camera.
        """
        if distortion_coefficients is None:
            distortion_coefficients = np.array([
                [-0.2976428547328032],
                [3.2508343621538445],
                [-17.38410840159056],
                [30.01965021834286],
            ])
        if camera_matrix is None:
            camera_matrix = np.array([
                [1490.4374643604199, 0.0, 990.6557248821284],
                [0.0, 1490.6535480621505, 544.6243597123726],
                [0.0, 0.0, 1.0],
            ])
        self._camera_location = camera_location
        self._recording_path = recording_path or f"{time.time()}_output.mp4"

        self._d_q = queue.Queue()
        self._r_q = queue.Queue()

        self._image_dimensions = image_dimensions
        self._fps = fps

        self._map1, self._map2 = cv2.fisheye.initUndistortRectifyMap(
            camera_matrix,
            distortion_coefficients,
            np.eye(3),
            camera_matrix,
            self._image_dimensions,
            cv2.CV_16SC2,
        )

    def _receive(self) -> None:
        """Receive data from the camera.


        :rtype: None

        """
        capture = cv2.VideoCapture(self._camera_location, cv2.CAP_FFMPEG)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._image_dimensions[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._image_dimensions[1])
        ret, frame = capture.read()

        frame = self._unfish(frame)
        self._d_q.put(frame)
        self._r_q.put(frame)
        while ret and self._is_running:
            ret, frame = capture.read()

            frame = self._unfish(frame)
            self._d_q.put(frame)
            self._r_q.put(frame)
        capture.release()

    def _display(self) -> None:
        """Display the data from the camera.


        :rtype: None

        """
        while self._is_running:
            if not self._d_q.empty():
                frame = self._d_q.get()
                cv2.imshow("Camera View", frame)
            key = cv2.waitKey(1)
            if key == EXT_KEY:  # Exit the viewer using ESC-button
                self._is_running = False
        cv2.destroyAllWindows()

    def _record(self) -> None:
        """Record the data from the camera.


        :rtype: None

        """
        out = cv2.VideoWriter(
            self._recording_path,
            cv2.VideoWriter.fourcc(*"mp4v"),
            self._fps,
            self._image_dimensions,
        )
        logging.info("Recording in progress...")
        while self._is_running:
            if not self._r_q.empty():
                out.write(self._r_q.get())
        logging.info("Recording finished.")
        logging.info("Saving video to: %s", self._recording_path)
        out.release()

    def _dump_record(self) -> None:
        """Dump record queue if not used.


        :rtype: None

        """
        while self._is_running:
            if not self._r_q.empty():
                self._r_q.get()

    def _dump_display(self) -> None:
        """Dump display queue if not used.


        :rtype: None

        """
        while self._is_running:
            if not self._d_q.empty():
                self._d_q.get()

    def _unfish(self, image: cv2.typing.MatLike) -> cv2.typing.MatLike:
        """Remove fisheye effect from the camera.

        :param image: The image
        :type image: cv2.typing.MatLike
        :returns: The undistorted image.
        :rtype: cv2.typing.MatLike

        """
        return cv2.remap(
            image,
            self._map1,
            self._map2,
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
        )

    def start(self, *, record: bool = False, display: bool = True) -> None:
        """Start the camera.

        :param *:
        :param record: Whether to record. (Default value = False)
        :type record: bool
        :param display: Whether to display the video stream. (Default
            value = True)
        :rtype: None
        :rtype: None
        :rtype: None
        :type display: bool
        :rtype: None

        """
        if not record and not display:
            msg = "The camera is neither recording or displaying, are you sure you are using it?"
            raise ValueError(msg)

        self._receive_thread = threading.Thread(target=self._receive)
        self._display_thread = threading.Thread(
            target=self._display if display else self._dump_display
        )
        self._record_thread = threading.Thread(
            target=self._record if record else self._dump_record
        )

        self._is_running = True

        self._receive_thread.start()
        self._record_thread.start()
        self._display_thread.start()
