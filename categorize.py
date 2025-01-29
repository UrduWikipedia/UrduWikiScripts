#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot finds the counterpart of a non-English Wikipedia
page on specified language Wikipedias and fetches its categories.
If any of those categories have a counterpart in the origin Wikipedia,
the bot then adds the page to those categories.
"""
#
# (C) User:Huji, 2021
# (C) User:Yethrosh, 2025
#
# Distributed under the terms of the MIT license.
#

import pywikibot
from pywikibot import pagegenerators
from functools import lru_cache
from pywikibot.bot import SingleSiteBot, ExistingPageBot, AutomaticTWSummaryBot
import re

# Show help with the parameter -help.
docuReplacements = {"&params;": pagegenerators.parameterHelp}

LANGUAGE_CODES = ["en", "ar", "fa", "fr", "es", "de", "nl", "hi", "simple"]

class CategorizeBot(SingleSiteBot, ExistingPageBot, AutomaticTWSummaryBot):
    update_options = {
        "cosmetic": False,  # Whether to run cosmetic changes script
        "use_redirects": False,  # Do not follow redirects
    }

    def __init__(self, generator, **kwargs):
        """
        @param generator: the page generator that determines which pages
            to work on
        @type generator: generator
        """
        super(CategorizeBot, self).__init__(site=True, **kwargs)
        self.generator = generator
        self.skip_categories = [
            "خودکار زمرہ بندی سے گریزاں صفحات",
        ]
        self.allowednamespaces = [0, 4, 6, 12, 14, 16]
        self.cosmetic_changes = kwargs["cosmetic"]
        self.site_fa = pywikibot.Site("ur")
        self.sites = {lang: pywikibot.Site(lang) for lang in LANGUAGE_CODES}
        self.remove_parent = False
        self.added_categories_set = set()  # To track added categories

    def list_intersection(self, list1, list2):
        list3 = [value for value in list1 if value in list2]
        return list3

    @lru_cache(maxsize=None)
    def get_existing_cats(self, page):
        """Get a list() of categories the page is in."""
        cats = list(page.categories())
        cat_titles = list()
        for c in cats:
            cat_titles.append(c.title(with_ns=False))
        return cat_titles

    @lru_cache(maxsize=None)
    def check_eligibility(self, candidate):
        """Determine if the category is addable."""
        cat = pywikibot.Page(self.site_fa, "زمرہ:%s" % candidate)
        if not cat.exists():
            return False
        cat_cats = self.get_existing_cats(cat)
        ineligible_parents = [
            "پوشیدہ زمرہ جات",
            "متلاشی زمرہ جات",
            "زمرہ جات نامکمل",
            "منتقل شدہ زمرہ جات"
        ]
        if len(self.list_intersection(ineligible_parents, cat_cats)) > 0:
            return False
        return True

    @lru_cache(maxsize=None)
    def check_eligibility_lang(self, lang, candidate):
        """Determine if the category is addable in a specific language."""
        cat = pywikibot.Page(self.sites[lang], "Category:%s" % candidate)
        cat_cats = self.get_existing_cats(cat)
        ineligible_parents = [
            "Hidden categories",
            "Tracking categories",
            "Stub categories"
        ]
        if len(self.list_intersection(ineligible_parents, cat_cats)) > 0:
            return False
        return True

    @lru_cache(maxsize=None)
    def is_child_category_of(self, child, parent):
        child_cat = pywikibot.Page(self.site_fa, "زمرہ:%s" % child)
        child_cat_cats = self.get_existing_cats(child_cat)
        if parent in child_cat_cats:
            return True
        return False

    def treat_page(self):
        """Process the current page that the bot is working on."""
        page = self.current_page

        if page.namespace() not in self.allowednamespaces:
            pywikibot.output("Namespace not allowed!")
            return False

        langlinks = page.langlinks()
        remote_pages = {lang: None for lang in LANGUAGE_CODES}

        for ll in langlinks:
            if ll.site.code in LANGUAGE_CODES:
                remote_pages[ll.site.code] = pywikibot.Page(ll)

        current_categories = self.get_existing_cats(page)
        if len(set(self.skip_categories) & set(current_categories)) > 0:
            pywikibot.output("Page disallows this bot; skipped.")

        added_categories = list()
        removed_categories = list()

        for lang, remote_page in remote_pages.items():
            if remote_page is None:
                continue

            if remote_page.isRedirectPage():
                pywikibot.output(f"Target page in {lang} is a redirect; skipped.")
                continue

            remote_categories = list(remote_page.categories())

            for rc in remote_categories:
                if self.check_eligibility_lang(lang, rc.title(with_ns=False)) is False:
                    continue
                candidate = None
                for ll in rc.langlinks():
                    if ll.site.code == "ur":
                        candidate = ll.title
                if candidate is None:
                    continue
                if candidate not in current_categories and candidate not in self.added_categories_set:
                    if self.check_eligibility(candidate):
                        # If a child of this category is already used, don't add it
                        skip_less_specific = False
                        for cc in current_categories:
                            if self.is_child_category_of(cc, candidate):
                                skip_less_specific = True
                                pywikibot.output(
                                    "More specific category already used."
                                )

                        # Otherwise add this category
                        if skip_less_specific is False:
                            added_categories.append(candidate)
                            self.added_categories_set.add(candidate)

                        # If a parent of what you just added is used, remove it
                        if self.remove_parent is True:
                            candidate_fullname = "زمرہ:%s" % candidate
                            candidate_page = pywikibot.Page(
                                self.site_fa,
                                candidate_fullname
                            )
                            candidate_parents = self.get_existing_cats(
                                candidate_page
                            )
                            intersection = self.list_intersection(
                                candidate_parents,
                                current_categories)
                            if len(intersection) > 0:
                                pywikibot.output("Removing less specific parent.")
                                removed_categories.extend(intersection)

        if len(added_categories) > 0:
            text = page.text
            summary_categories = []

            for ac in added_categories:
                text += "\n[[زمرہ:%s]]" % ac
                summary_categories.append(f"[[زمرہ:{ac}]]")

            if len(removed_categories) > 0:
                for rc in removed_categories:
                    rc_pattern = r"\n\[\[زمرہ:" + rc + r"(\|[^\]]*)?\]\]"
                    text = re.sub(rc_pattern, "", text)

            # Construct the summary based on the number of categories
            num_categories = len(added_categories)
            if num_categories > 1:
                summary = f"خودکار: {num_categories} زمرہ جات کا اضافہ ({'، '.join(summary_categories)})"
            else:
                summary = f"خودکار: 1 زمرہ کا اضافہ ({'، '.join(summary_categories)})"
            
            self.put_current(text, summary=summary)


def main(*args):
    """
    Process command line arguments and invoke bot.

    @param args: command line arguments
    @type args: list of unicode
    """
    options = {}

    # Default value for "cosmetic" option
    options["cosmetic"] = False

    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # Process pagegenerators arguments
    gen_factory = pagegenerators.GeneratorFactory()
    local_args = gen_factory.handle_args(local_args)

    # Parse command line arguments
    for arg in local_args:
        arg, sep, value = arg.partition(":")
        option = arg[1:]
        if option in ("summary", "text"):
            if not value:
                pywikibot.input("Please enter a value for " + arg)
            options[option] = value
        # Take the remaining options as booleans.
        else:
            options[option] = True

    gen = gen_factory.getCombinedGenerator(preload=True)
    if gen:
        bot = CategorizeBot(gen, **options)
        bot.run()
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == "__main__":
    main()
