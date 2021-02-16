import logging

logger = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.WARNING)
logger.addHandler(consoleHandler)

# The arxiv package (probably) is setting some global logger settings and
# configuring output to scholar.log. Unless you set a file logger here
# explicitly, you're gonna inherit whatever they do.
