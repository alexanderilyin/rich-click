from typing import TYPE_CHECKING, Any, Mapping, Optional, Type, Union

import click
from rich.console import Console

from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter


class RichContext(click.Context):
    """Click Context class endowed with Rich superpowers."""

    formatter_class: Type[RichHelpFormatter] = RichHelpFormatter

    def __init__(
        self,
        *args: Any,
        rich_console: Optional[Console] = None,
        rich_help_config: Optional[Union[Mapping[str, Any], RichHelpConfiguration]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Create Rich Context instance.

        Args:
        ----
            *args: Args that get passed to click.Context.
            rich_console: Rich Console. Defaults to None.
            rich_help_config: Rich help configuration.  Defaults to None.
            **kwargs: Kwargs that get passed to click.Context.
        """
        super().__init__(*args, **kwargs)
        parent: Optional[RichContext] = kwargs.pop("parent", None)

        if rich_console is None and hasattr(parent, "console"):
            rich_console = parent.console  # type: ignore[has-type,union-attr]

        self.console = rich_console

        if rich_help_config is None and hasattr(parent, "help_config"):
            self.help_config = parent.help_config  # type: ignore[has-type,union-attr]
        elif isinstance(rich_help_config, Mapping):
            if hasattr(parent, "help_config"):
                if TYPE_CHECKING:
                    assert parent is not None
                kw = parent.help_config.__dict__.copy()
                kw.update(rich_help_config)
                self.help_config = RichHelpConfiguration(**kw)
            else:
                self.help_config = RichHelpConfiguration.load_from_globals(**rich_help_config)
        elif rich_help_config is None:
            self.help_config = RichHelpConfiguration.load_from_globals()
        else:
            self.help_config = rich_help_config

    def make_formatter(self) -> RichHelpFormatter:
        """Create the Rich Help Formatter."""
        return self.formatter_class(
            width=self.terminal_width, max_width=self.max_content_width, config=self.help_config
        )
