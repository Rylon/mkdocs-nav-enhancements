# from mkdocs.plugins import BasePlugin
import mkdocs


class MkDocsTitlePlugin(mkdocs.plugins.BasePlugin):
    # Options would go here.
    config_scheme = (
    )

    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        print("hi")
        import pdb
        pdb.set_trace()

        return markdown
