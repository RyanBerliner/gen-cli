import hashlib


def line_hash(id, content):
    length = 7
    if id == -1:
        return '0' * length

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
        ret += f'\n{curr[2]}|{curr[1].rstrip()}'
        curr = curr[3]

    return ret


def line_tree_to_content(root, with_hashes=False):
    # TODO: when delete nodes are in place this will filter them out
    ret = ''
    curr = root[3]

    while curr is not None:
        if with_hashes:
            ret += f'{curr[2]}|{curr[1]}'
        else:
            ret += curr[1]
        curr = curr[3]

    return ret
