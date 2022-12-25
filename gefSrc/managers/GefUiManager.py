from .GefManager import GefManager

class GefUiManager(GefManager):
    """Class managing UI settings."""
    def __init__(self) -> None:
        self.redirect_fd : Optional[TextIOWrapper] = None
        self.context_hidden = False
        self.stream_buffer : Optional[StringIO] = None
        self.highlight_table: Dict[str, str] = {}
        self.watches: Dict[int, Tuple[int, str]] = {}
        self.context_messages: List[Tuple[str, str]] = []
        return
