# from mkdocs.plugins import BasePlugin
import mkdocs


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

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        print("hi")
        # import pdb ; pdb.set_trace()
        # TODO: Edit page.title based on the Markdown here.

        return markdown

    def on_nav(self, nav, config, files, **kwargs):
        nav.items = self._process_nav_items_recursive(nav)
        return nav
