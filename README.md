# webfscholar

Generate publications webpage from a google scholar. This occurs in two steps:

1. Generate bibtex from a google scholar
2. Generate webpage from a bibtex

The intermediate bibtex allows you to plug-and-play with other
auto-publication-webpage services. Furthermore, unlike most Google Scholar
unofficial APIs, this library:

- Uses information pulled directly from the Google Scholar profile page, as
  opposed to un-configurable search results. This means `webfscholar` will
  respect any custom titles or removed publications.
- Supplants Google Scholar information using ArXiv.

The website-builder also supports:

- A default, mobile-friendly theme with a search bar
- Multiple bibtexs, including online sources

## Installation

```
pip install webfscholar
```
