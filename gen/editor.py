import hashlib


def line_hash(id, content):
    length = 7
    if id == -1:
        return '0' * length

    return hashlib.md5(bytes(f'{id}|{content}', 'utf-8')).hexdigest()[:length]


def content_to_line_tree(content):
    # id, content, next
    prev = root = [-1, '', None]
    # the root node has an additional 4th index that stores the max id so we
    # can auto increment when new nodes are added later
    root.append(root[0])

    for line in content.splitlines(keepends=True):
        root[3] += 1
        curr = [root[3], line, None]
        prev[2] = curr
        prev = curr

    return root


def complete_line_tree(root):
    ret = f'{line_hash(*root[:2])}|{root[1]}'
    curr = root[2]

    while curr is not None:
        # remove the trailing newline so we dont get double newlines
        ret += f'\n{line_hash(*curr[:2])}|{curr[1].rstrip()}'
        curr = curr[2]

    return ret


def line_tree_to_content(root, with_hashes=False):
    # TODO: when delete nodes are in place this will filter them out
    ret = ''
    curr = root[2]

    while curr is not None:
        if with_hashes:
            ret += f'{line_hash(*curr[:2])}|{curr[1]}'
        else:
            ret += curr[1]
        curr = curr[2]

    return ret
