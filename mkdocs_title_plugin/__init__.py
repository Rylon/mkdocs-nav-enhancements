import mkdocs
import re
import os


class MkDocsTitlePlugin(mkdocs.plugins.BasePlugin):
    # Options would go here.
    config_scheme = (
    )

    def _process_nav_items_recursive(self, nav_items):
        """
        Here we are walking the navigation tree of Sections and Pages recursively,
        looking for any folders containing only a single page.

        When that happens, we replace the Section with its only child, 'collapsing' the folder
        to help keep the nav uncluttered.

        If a page doesn't have a valid title at that point, we take the basename of its path
        and use that.
        """

        new_nav_items = []

        for nav_item in nav_items:
            if nav_item.children:
                # If there is only one child in this nav_item, and the nav_item isn't at the top level,
                # then we want to replace this nav_item with its only child to collapse folders with only one file in.
                # We only do this if the nav_item has a parent nav_item, otherwise it can result in top level nav sections
                # being hidden from the UI in some themes.
                if len(nav_item.children) == 1 and nav_item.parent:
                    child = nav_item.children[0]

                    # If the child doesn't have a title already, we set one
                    # using the base name of the filesystem path.
                    if not child.title:
                        child_url = child.url[:-1] if child.url[-1] == '/' else child.url
                        child.title = os.path.basename(child_url)

                    # new_nav_items.append( nav_item.children[0] )
                    new_nav_items.append(child)

                else:
                    # If there is more than one child, we want to recurse over them so that
                    # we can collapse folders of single pages at any depth in the tree.
                    nav_item.children = ( self._process_nav_items_recursive( nav_item.children ) )
                    new_nav_items.append(nav_item)

            else:
                # No child items, just add this directly.
                new_nav_items.append(nav_item)

        return new_nav_items

    def _look_for_title_in_markdown(self, markdown_src):
        """
        For a given block of Markdown, searches for the first title that matches the following:

        1. The first 'hash-style' header, which is a line beginning with between 1 to 6 '#'.
        2. The first 'setext-style' header, which is a line where the line immediately after contains
           only '=' or '-'.

        If either of those are found, it will attempt to extract the title text from any other markup
        that might be in the title, for example image or link markup, which would otherwise be rendered
        as a string literal in the generated HTML.

        Note that this can sometimes result in the title being quite different than the folder it
        was in, an outstanding improvement that could be made here would be to try to re-sort the
        nav alphabetically to account for that.
        """

        lines = markdown_src.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        for line_number, line in enumerate(lines):
            line = line.strip()

            # If the line is empty, skip
            if not line.strip():
                continue

            # Check if the line is a hash-style header
            if re.search('^#{1,6} .*$', line):
                # If it is, first we check if it has any markup after the title, such as image or text links
                # so we can exclude those from the title.
                matches = re.match('^#{1,6} ?(.+?) ?\!?\[', line)
                if matches:
                    return matches.groups()[0]
                # Otherwise, we can just strip the # from the start.
                else:
                    return re.sub('#{1,6} ', '', line)
                    # return line.lstrip('# ')

            # Next, check for "setext" style headers, which are "underlined"
            # with either "=" or "-". To do that, we need to check the line
            # after the current line, obviously only possible if we're not
            # on the last line.
            if not line_number == len(lines):

                # We get the set of unique characters in the line, and
                # check against the sets of ("=") or ("-") to verify that the
                # line contained *only* "=" or *only* "-" characters.
                # If it does, we can be reasonably sure this is the title.
                next_line_chars = set( lines[ line_number + 1 ].strip() )
                if next_line_chars == set("=") or next_line_chars == set("-"):
                    return line.strip()

        # If we somehow made it through the entire doc without matching anything, return None
        return None

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        """
        The page_markdown event is called after the page's markdown is loaded from
        file and can be used to alter the Markdown source text.
        The meta- data has been stripped off and is available as page.meta at this point.
        """

        new_title = self._look_for_title_in_markdown(markdown)
        if new_title and page.title != new_title:
            print("Changing title from %s to %s" % (page.title, new_title))
            page.title = new_title

        return markdown

    def on_nav(self, nav, config, files, **kwargs):
        """
        The nav event is called after the site navigation is created and can be used to alter the site navigation.

        Here we call our own method which will walk the page tree recursively looking for any folders containing
        only a single page, and attempt to collapse them to keep the nav uncluttered.
        """

        nav.items = self._process_nav_items_recursive(nav)
        return nav
