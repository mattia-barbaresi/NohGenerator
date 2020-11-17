import matplotlib.pyplot as plt


# filename = 'garage4'
# data = jsonEditor.readKinectDict(filename)
# i = 0
# for key in data["datafile"]:
#     if i > 0:
def printplot(key):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for i in key["data"]:
        # x y z
        if "Left" in i["jointname"]:
            color = "red"
        elif "Right" in i["jointname"]:
            color = "green"
        else:
            color = "black"
        ax.plot([i['coordinates'][0]], [i['coordinates'][2]], [i['coordinates'][1]], marker='o', markersize=5,
                alpha=0.6, color=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.axis('equal')

    plt.show()
