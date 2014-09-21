#!/usr/bin/env python

import pandas as pd
import fuzzyContacts


def get_event_roster(signups, event):
    """Returns the list of names of
    people who signed up for a given event
    """
    return [s for s in signups[event][3:] if type(s) == str]


def get_roster_emails(roster, emails_db, scores=False):
    """Returns emails for names in the roster
    """
    if scores:
        scores_l = []
    roster_emails = {}
    emails_db.sort('Full Name')
    for name in roster:
        retrieval_method, l_i = fuzzyContacts.fuzzy_name_search(name, emails_db)
        roster_emails[name] = [emails_db['Emails'][i] for i in l_i]
        if scores:
            scores_l.append(retrieval_method)
    if scores:
        return roster_emails, scores_l
    return roster_emails


