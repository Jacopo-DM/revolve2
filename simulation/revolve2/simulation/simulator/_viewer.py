from abc import ABC, abstractmethod


class Viewer(ABC):
    """An abstract viewer class, enabling the rendering of simulations."""

    @abstractmethod
    def close_viewer(self) -> None:
        """Close the viewer.


        :rtype: None

        """

    @abstractmethod
    def render(self) -> None | int:
        """Render the scene on the viewer.


        :returns: Nothing or feedback.

        :rtype: None|int

        """

    @abstractmethod
    def current_viewport_size(self) -> tuple[int, int]:
        """Get the current viewport size.


        :returns: The size as a tuple.

        :rtype: tuple[int,int]

        """

    @property
    @abstractmethod
    def view_port(self) -> None:
        """Get the viewport.


        :returns: The viewport object.

        :rtype: None

        """

    @property
    @abstractmethod
    def context(self) -> None:
        """Return the viewer context.


        :returns: The context object.

        :rtype: None

        """

    @property
    @abstractmethod
    def can_record(self) -> bool:
        """Check if this viewer can record.


        :returns: The truth.

        :rtype: bool

        """
