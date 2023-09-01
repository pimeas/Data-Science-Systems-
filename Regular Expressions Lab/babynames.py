#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    file = open(filename, 'r')
    data = file.read()

    string_list = []

    # Year '2006'
    year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', data)
    # error catching
    if not year_match:
        sys.stderr.write('Year not found. \n')
        sys.exit(1)
    year = year_match.group(1)
    string_list.append(year)

    # tuples
    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', data)

    ranked_names = {}
    for rank_tuple in tuples:
        (rank, boy, girl) = rank_tuple
        if boy not in ranked_names:
            ranked_names[boy] = rank
        if girl not in ranked_names:
            ranked_names[girl] = rank

    # Names sorted
    sorted_names = sorted(ranked_names.keys())
    for name in sorted_names:
        string_list.append(name + " " + ranked_names[name])

    return string_list


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for filename in args:
        string_list = extract_names(filename)

        # Making output
        data = '\n'.join(string_list)

        if summary:
            outfile = open(filename + '.summary', 'w')
            outfile.write(data + '\n')
            outfile.close()
        else:
            print(data)


if __name__ == '__main__':
    main()
