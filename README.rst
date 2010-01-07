==================
Django FlatContent
==================

Django FlatContent is intended as a flatpages-like app but for smaller chunks
of content that can be edited in the Django admin.

Features
========

* Simple FlatContent model
* Template tag for pulling FlatContent into templates
* Caching of FlatContent for performance

Installation
============

1. Add the ``flatcontent`` directory to your Python path.
2. Add ``flatcontent`` to your ``INSTALLED_APPS``.
3. Run the command ``manage.py syncdb`` to install the models.

Usage
=====

Once content is available in the `FlatContent` model, it can be accessed via
the templates using the provided template tags::

    {% load flatcontent_tags %}
    <div id="footer">
        {% flatcontent footer %}
    </div>

The above will perform a slug lookup on the text "footer" and return the
content associated with that slug.

You can also put the content into a template variable for passing to other
template tags or filters.  For example, getting the footer and processing the
text through the `textile` filter::

    {% load flatcontent_tags markup %}
    <div id="footer">
        {% flatcontent footer as content %}
        {{ content|textile }}
    </div>

