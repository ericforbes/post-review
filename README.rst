===========
post-review
===========

.. image:: https://travis-ci.org/ericforbes/post-review.svg?branch=develop
   :target: https://travis-ci.org/ericforbes/post-review
   :alt: Build Status


This package provied a unified command line interface for posting code reviews and merge requests

The post-review package works on Python versions:

* 2.7.x and greater
* 3.3.x and greater



------------
Installation
------------

The easiest way to install post-review is to use `pip`_::

    $ pip install post-review


If you already have post-review installed and want to upgrade to the latest version::

    $ pip install --upgrade post-review



---------------
Getting Started
---------------

post-review is able to determine your git service automatically. There is a one-time setup 
that is required to fetch your git service API keys -- but post-review will instruct you at this
step.

The quickest way to get started is to just run the ``post-review`` command::

    $ post-review --target <target_branch>


Assuming you are using GitLab Hosted, this is what you will see for your one time setup::

    $ post-review --target <target_branch>

    (One Time Setup) Please create a Personal Access Token
    https://gitlab.com/profile/personal_access_tokens
    Scope: API, Expires: Never

    Please enter your Personal Access Token: <paste_your_token_here>
