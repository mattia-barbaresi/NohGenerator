import plots.trigo


def angleHeadPitch(x1, y1, z1, #head
                   x2, y2, z2, #shoulder centre
                   x3, y3, z3): #spine
    angle =-(180 - plots.trigo.angleBetween3Points2D(y1, z1, y2, z2, y3, z3))
    if angle > 29:
        angle = 29
    elif angle< -38:
        angle = -38
    return angle