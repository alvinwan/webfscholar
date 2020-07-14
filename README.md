![Mockup](https://user-images.githubusercontent.com/2068077/87393876-ac37e580-c563-11ea-8104-e9f8b43ffcef.jpg)

# webfscholar

Generate publications webpage from a google scholar in just two steps:

1. Convert Google Scholar to BibTeX
2. Convert BibTeX to webpage.

The default theme (pictured above) is mobile-friendly and searchable. You can view sample output at [r.aaalv.in](https://r.aaalv.in).

![webfscholar](https://user-images.githubusercontent.com/2068077/87399323-16548880-c56c-11ea-96d6-ad84da727a2f.gif)

## Installation

```
pip install webfscholar
```

# Why webfscholar

The intermediate bibtex allows you to plug-and-play with other
auto-publication-webpage services. Furthermore, unlike most Google Scholar
unofficial APIs, this library:

- Uses information pulled directly from the Google Scholar profile page, as
  opposed to un-configurable search results. This means `webfscholar` will
  respect any custom titles or removed publications.
- Supplants Google Scholar information using ArXiv.

The website-builder also supports:

- A default, mobile-friendly theme with a search bar

