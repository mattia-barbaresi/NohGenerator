# utilities

# convert dictionary levels in array
def dict_to_arr(d):
    arr = []
    for itm in d.items():
        for sq in itm[1]:
            if sq:
                arr.append(list(str(x) for x in sq))
    return arr


# convert generated into new list of sequences
def generated_to_arr(g):
    arr = []
    for itm in g.items():
        for sq in itm[1]:
            if len(sq) > 1:
                arr.append("".join(sq.split(" ")))
    return arr
