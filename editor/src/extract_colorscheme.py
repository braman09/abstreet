#!/usr/bin/python2

import os

def run():
    mapping = {}

    for path, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.rs') and f != 'colors.rs' and f != 'objects.rs':
                for k, v in read_file(os.path.join(path, f)):
                    # TODO Check for double-definitions
                    mapping[k] = v

    for k in sorted(mapping.iterkeys()):
        print '{} = {}'.format(k, mapping[k])


def read_file(filename):
    print filename
    entries = []
    with open(filename, 'r') as f:
        src = ''.join(f.readlines())
        while src:
            if src.startswith('get('):
                src = src[len('get('):]

                # Look for the opening "
                while src[0] != '"':
                    src = src[1:]
                src = src[1:]

                # Read the key until the closing "
                key = ''
                while src[0] != '"':
                    key += src[0]
                    src = src[1:]
                src = src[1:]

                # Look for the ,
                while src[0] != ',':
                    src = src[1:]
                src = src[1:]

                # Look for the Color
                while not src.startswith('Color'):
                    src = src[1:]

                # Wait for the ()'s to be mismatched, meaning we found the ) of the get()
                counter = 0
                value = ''
                while True:
                    value += src[0]
                    if src[0] == '(':
                        counter += 1
                    elif src[0] == ')':
                        counter -= 1
                        if counter == -1:
                            value = value[:-1]
                            entries.append((key, value))
                            src = src[1:]
                            break
                    elif src[0] == ',' and counter == 0:
                        value = value[:-1]
                        entries.append((key, value))
                        src = src[1:]
                        break
                    src = src[1:]
            else:
                src = src[1:]
    return entries


if __name__ == '__main__':
    run()
