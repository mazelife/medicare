import inspect
from operator import itemgetter
from medicare.core.decorators import provides_context


class ContextProvider(object):

    def get_additional_context_data(self):
        methods = inspect.getmembers(self, inspect.ismethod)
        context_providers = filter(lambda m: getattr(m[1], "provides_context", False), methods)
        context = {}
        for name, _ in context_providers:
            context.update(getattr(self, name)())
        return context


class NavMixin(ContextProvider):

    _allowed_sections = frozenset(("hospitals", "regions", "procedures", "home"))

    @provides_context
    def get_navigation_context(self):
        section = getattr(self, "section", "home")
        assert section in self._allowed_sections, "Invalid section: \"{0}\", must be one of: {1}".format(
            section,
            ", ".join(self._allowed_sections)
        )
        return {'section': section}
