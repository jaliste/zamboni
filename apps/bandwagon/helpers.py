import math

import jinja2
from jingo import register, env
from tower import ugettext as _

from amo.helpers import login_link
from cake.urlresolvers import remora_url


@register.inclusion_tag('bandwagon/collection_listing_items.html')
@jinja2.contextfunction
def collection_listing_items(context, collections):
    c = dict(context.items())
    c['collections'] = collections
    return c


@register.function
def user_collection_list(collections=[], heading=''):
    """list of collections, as used on the user profile page"""
    c = {'collections': collections, 'heading': heading}
    t = env.get_template('bandwagon/users/collection_list.html').render(**c)
    return jinja2.Markup(t)


@register.inclusion_tag('bandwagon/collection_favorite.html')
@jinja2.contextfunction
def collection_favorite(context, collection):
    c = dict(context.items())
    user = c['request'].amo_user
    is_subscribed = collection.is_subscribed(user)

    button_class = 'add-to-fav'

    if is_subscribed:
        button_class += ' fav'
        text = _('Remove from Favorites')
        action = remora_url('collections/unsubscribe')

    else:
        text = _('Add to Favorites')
        action = remora_url('collections/subscribe')

    c.update(locals())
    c.update({'c': collection})
    return c


@register.inclusion_tag('bandwagon/barometer.html')
@jinja2.contextfunction
def barometer(context, collection):
    """Shows a barometer for a collection."""
    c = dict(context.items())
    request = c['request']

    user_vote = None  # Non-zero if logged in and voted.

    if request.user.is_authenticated():
        # TODO: Use reverse when bandwagon is on Zamboni.
        up_action = collection.upvote_url()
        down_action = collection.downvote_url()
        up_title = _('Add a positive vote for this collection')
        down_title = _('Add a negative vote for this collection')
        cancel_title = _('Remove my vote for this collection')

        if 'collection_votes' in context:
            user_vote = context['collection_votes'].get(collection.id)
        else:
            votes = request.amo_user.votes.filter(collection=collection)
            if votes:
                user_vote = votes[0]

    else:
        up_action = down_action = login_link(c)
        login_title = _('Log in to vote for this collection')
        up_title = down_title = cancel_title = login_title

    up_class = 'upvotes'
    down_class = 'downvotes'
    cancel_class = 'cancel_vote'

    total_votes = collection.upvotes + collection.downvotes

    if total_votes:
        up_ratio = int(math.ceil(round(100 * collection.upvotes
                                       / total_votes, 2)))
        down_ratio = 100 - up_ratio

        up_width = max(up_ratio - 1, 0)
        down_width = max(down_ratio - 1, 0)

    if user_vote:
        if user_vote.vote > 0:
            up_class += ' voted'
        else:
            down_class += ' voted'
    else:
        cancel_class += ' hidden'

    c.update(locals())
    c.update({'c': collection})
    return c
