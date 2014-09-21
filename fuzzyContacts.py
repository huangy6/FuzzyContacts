#!/usr/bin/env python

import pandas as pd
from fuzzywuzzy import fuzz


def fuzzy_name_search(name, db):
    """Runs a chain of fuzzy searches
    for a given name in a DataFrame,
    assuming well-formatted name string

    -whole string search
    -misspelled name search
    -search by initials
    -name in email search
    """
    names = db['Full Name']
    emails = [l.split(',') for l in db['Emails']]
    try:
        matches = whole_string_search(name, names)
        return ('whole string match', matches)
    except ValueError:
        pass

    try:
        initial_search(name, names)
        return ('initials match', matches)
    except ValueError:
        pass

    i_nam, name_score = fuzzy_string_search(name, names)
    i_eml, email_score = name_in_emails(name, emails)
    if name_score > email_score:
        return ("Name score: %d" % name_score, [i_nam])
    else:
        return ("Email score: %d" % email_score, [i_eml])


def whole_string_search(st, li):
    """Looks for whole string in list, returns index
    """
    matches = []
    for (i, s) in enumerate(li):
        if s.lower() == st.lower:
            matches.append(i)

    if matches:
        return matches
    else:
        raise ValueError("%s is not in list" % st)


def fuzzy_string_search(st, li):
    """Looks for best match of string in list
    """
    best_match = 0
    best_rat = 0
    for (i, s) in enumerate(li):
        rat = fuzz.partial_ratio(s, st)
        if rat > best_rat:
            best_match = i
            best_rat = rat

    return best_match, best_rat


def initial_search(name, li):
    """Searches for name, allowing for initial abbreviations
    """
    matches = []

    first_last = name.split()
    first_l = first_last[0] + first_last[1][0]
    f_last = first_last[0][0] + first_last[1]

    for (i, s) in enumerate(li):
        if first_l.lower() == s.lower() or f_last == s.lower():
            matches.append(i)

    if matches:
        return matches
    else:
        raise ValueError("%s does not exist in this list" % name)


def name_in_emails(name, emails):
    """Searches through list of emails
    for any that contain name
    """
    best_match = 0
    best_score = 0

    for (i, email_l) in enumerate(emails):
        for email in email_l:
            if "@" not in email:
                continue
            user, domain = email.split("@")
            score = fuzz.ratio(name, user)
            if score > best_score:
                best_match = i
                best_score = score

    return best_match, best_score
