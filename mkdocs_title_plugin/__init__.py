import mkdocs
import re


class MkDocsTitlePlugin(mkdocs.plugins.BasePlugin):
    # Options would go here.
    config_scheme = (
    )

    def _process_nav_items_recursive(self, nav_items):
        new_nav_items = []

        for nav_item in nav_items:
            if nav_item.children:
                if len(nav_item.children) == 1:
                    new_nav_items.append( nav_item.children[0] )
                else:
                    nav_item.children = ( self._process_nav_items_recursive( nav_item.children ) )
                    new_nav_items.append(nav_item)
            else:
                new_nav_items.append(nav_item)

        return new_nav_items

    def _look_for_title_in_markdown(self, markdown_src):
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
                matches = re.match('^#(.+?)\!?\[', line)
                if matches:
                    return matches.groups()[0]
                # Otherwise, we can just strip the # from the start.
                else:
                    return line.lstrip('# ')

            # Finally, check for "setext" style headers, which are "underlined"
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
        new_title = self._look_for_title_in_markdown(markdown)
        if new_title:
            page.title = new_title

        return markdown

    def on_nav(self, nav, config, files, **kwargs):
        # TODO: Re-sort these alphabetically after sorting.
        nav.items = self._process_nav_items_recursive(nav)
        return nav
