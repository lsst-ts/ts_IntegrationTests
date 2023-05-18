"""Sphinx configuration file for TSSW package"""

from documenteer.conf.pipelines import *  # type: ignore # noqa

project = "ts-IntegrationTests"
html_theme_options["logotext"] = project  # type: ignore # noqa
html_title = project
html_short_title = project
