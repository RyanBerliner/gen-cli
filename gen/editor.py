import hashlib


def line_hash(id, content):
    length = 7
    if id == -1:
        return '0' * length
    if isinstance(content, int):
        return '1' * length

    return hashlib.md5(bytes(f'{id}|{content}', 'utf-8')).hexdigest()[:length]


def content_to_line_tree(content):
    # id, content, hash, next
    prev = root = [-1, '', line_hash(-1, ''), None]
    # the root node has an additional 4th index that stores the max id so we
    # can auto increment when new nodes are added later
    root.append(root[0])

    for line in content.splitlines(keepends=True):
        root[4] += 1
        curr = [root[4], line, line_hash(root[4], line), None]
        prev[3] = curr
        prev = curr

    return root


def debug_line_tree(root):
    ret = f'{root[2]}|{root[1]}'
    curr = root[3]

    while curr is not None:
        # remove the trailing newline so we dont get double newlines
        content = str(curr[1]) \
                if isinstance(curr[1], int) else curr[1].rstrip()
        ret += f'\n{curr[2]}|{content}'
        curr = curr[3]

    return ret


def line_tree_to_content(root, with_hashes=False):
    ret = ''
    curr = root[3]

    skip_next = 0

    while curr is not None:
        content = curr[1]

        if skip_next > 0:
            skip_next -= 1
            curr = curr[3]
            continue

        if not isinstance(content, int):
            if with_hashes:
                ret += f'{curr[2]}|{content}'
            else:
                ret += content

        else:
            skip_next = content

        curr = curr[3]

    return ret


def insert_new_content_after_line(new_content, line, root):
    curr = root

    while curr is not None and curr[2] != line:
        curr = curr[3]

    assert curr is not None, \
        f'Unable to find the reference line hash {line}'

    # we should make sure the last line ends in a newline
    if not isinstance(new_content, int) and curr[1].rstrip('\n') == curr[1]:
        curr[1] += '\n'

    og_next = curr[3]
    prev = curr

    if isinstance(new_content, int):
        root[4] += 1
        curr = [root[4], new_content, line_hash(root[4], new_content), None]
        prev[3] = curr
        prev = curr
    else:
        for content in new_content.splitlines(keepends=True):
            root[4] += 1
            curr = [root[4], content, line_hash(root[4], content), None]
            prev[3] = curr
            prev = curr

    # we should make sure the last line ends in a newline
    if not isinstance(new_content, int) and prev[1].rstrip('\n') == prev[1]:
        prev[1] += '\n'

    prev[3] = og_next


def delete_content(start_line, end_line, root):
    # start and end are inclusive
    # we record deletions just as integers, which denote the next N lines are
    # to be deleted

    # the start will actually be the item before the start so we can insert the
    # number of lines to delete before it
    start = root

    while start[3] is not None and start[3][2] != start_line:
        start = start[3]

    assert start is not None, \
        f'Unable to find the reference start line hash {start_line}'

    end = start
    count = 0

    while end is not None and end[2] != end_line:
        end = end[3]
        count += 1

    assert end is not None, \
        f'Unable to find the reference end line hash {end_line}'

    return insert_new_content_after_line(count, start[2], root)


def update_content(start_line, end_line, new_content, root):
    # start and end are inclusive
    # this is literally just a delete, then an insert
    start = root

    while start[3] is not None and start[3][2] != start_line:
        start = start[3]

    assert start is not None, \
        f'Unable to find the reference start line hash {start_line}'

    delete_content(start_line, end_line, root)
    insert_new_content_after_line(new_content, start[2], root)
