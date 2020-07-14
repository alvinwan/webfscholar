# webfscholar
Generate publications webpage from a google scholar. This occurs in two steps:

1. Generate bibtex from a google scholar
2. Generate webpage from a bibtex

By using bibtex as an intermediate representation, you can choose to make
modifications beyond what is supported in the current bibtex-builder. Unlike
most Google Scholar unofficial Python APIs, the Google Scholar utilities
provided in this package stay faithful to the information presented on the
user profile page. The website-builder also supports:

- Several website themes
- Multiple bibtexs, including online sources
