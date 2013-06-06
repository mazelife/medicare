from django.core.paginator import Page as BasePage
from django.core.paginator import Paginator as BasePaginator


class Page(BasePage):
    """
    A modified page class that makes it possible to handle very
    large numbers of pages with ellipses (see Google's paginaton for
    an example of this in action).
    """
    def __init__(self, *args, **kwargs):
        self.surrounding_pages = kwargs.pop("surrounding_pages")
        self.max_display_pages = self.surrounding_pages * 2
        super(Page, self).__init__(*args, **kwargs)
        if self.paginator.num_pages <= self.max_display_pages:
            self.page_range = self.paginator.page_range
            return
        if self.number <= self.max_display_pages:
            self.page_range = range(1, self.max_display_pages + 2)
            self.show_first = False
            self.show_last = True
        elif (self.paginator.num_pages - self.number + 1) < self.max_display_pages:
            start = self.paginator.num_pages - self.max_display_pages + 1
            stop = self.paginator.num_pages + 1
            self.page_range = range(start, stop)
            self.show_first = True
            self.show_last = False
        else:
            start = self.number - self.surrounding_pages + 1
            stop = self.number + self.surrounding_pages
            self.page_range = range(start, stop)
            self.show_first = True
            self.show_last = True


class Paginator(BasePaginator):
    """
    A modified paginator class that makes it possible to handle very
    large numbers of pages with ellipses (see Google's paginaton for
    an example of this in action).
    """
    surrounding_pages = 4  # Number of pages on either side of current page.

    def _get_page(self, *args, **kwargs):
        kwargs.update({
            "surrounding_pages": self.surrounding_pages
        })
        return Page(*args, **kwargs)

    def page(self, number):
        """
        Deprecated in Django 1.6. Use the ``_get_page`` hook instead.
        """
        base_page = super(Paginator, self).page(number)
        return self._get_page(base_page.object_list, base_page.number, self)
