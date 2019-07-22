# MkDocs Nav Enhancements

This is a small plugin for the excellent [MkDocs](https://www.mkdocs.org) project which makes some enhancements to the navigation.

## Features

### Enhanced titles

By default, MkDocs looks for a level 1 atx-style header found at the top of the document and uses that for the page title.

If you are dealing with documentation from third-party sources you may find that some of them start their titles at level 2 (possibly for aesthetic reasons), or use setext-style headers instead.

This plugin will try to help by looking through each Markdown document and using the following rules to detect a page title instead:

* Use the first atx-style header found in the document at any level between 1 to 6, which is any line beginning with between 1 to 6 '#' characters.

* Or use the first setext-style header, which is any line where the line immediately after contains only '=' or '-' characters, effectively 'underlining' the line.

It will also remove any additional markup that is found in the title, such as image or link tags, which would otherwise be rendered as string literals in the generated HTML.

### Reduced folders

In order to de-clutter the navigation, the plugin looks for any sections containing only one page, and tries to collapse that page up a level into its parent. This helps deal with navigation bars filled with single-page folders to keep things looking tidy.

## Usage

Install the plugin:

```bash
pip install mkdocs-nav-enhancements
```

Add the plugin to your `mkdocs.yml` [MkDocs configuration](https://www.mkdocs.org/user-guide/configuration/) file:

```yaml
plugins:
  - mkdocs-nav-enhancements
```

## Known issues

When changing the page title, or collapsing single-page folders, this can sometimes result in the effective page title being quite different. Currently this plugin does not re-sort the nav bar alphabetically when this happens.

A second issue is that these options are not independently controllable, at least not in the first version; it's all or nothing for now!

## Contributing

Source code is hosted at [GitHub](https://github.com/Rylon/mkdocs-nav-enhancements).

Please report issues and feature requests on [GitHub Issues](https://github.com/Rylon/mkdocs-nav-enhancements).

Pull Requests are also welcome!
