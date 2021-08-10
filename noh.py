# coding=utf-8
# moves
# "z": "move_forward",
# "y": "move_backward",
# "x": "rotate_left",
# "w": "rotate_right",


katas = {
    "standing": ":",  # kamae
    "kneeling": ".",  # shita ni i
    "walking-forward":"z",  # deru
    "walking-backward":"y",  # sagaru
    "left step": "x",  # simple pivot (hidari nejiru) or step pivot (hidari kakeru)
    "right step": "w",  # simple pivot (migi nejiru) or step pivot right (migi kakeru)
    "large circle left":"xzxz",  # hidari ōmawari
    "large circle right":"wzwz",  # migi ōmawari
    "circlet left": "xxxx",  # hidari mawarikomi
    "circlet right": "wwww",  # migi mawarikomi
    "circlet point": "xxxxxxxxszbyrs",  # (mawari kaeshi): two complete Circlets and concludes with a Forward point
    "forward-point":"zb",  # shikake
    "open-retreat":"ycrs",  # hiraki
    "backing-point":"syebs",  # sashi
    "scooping-point":"swbexbs",  # kaikomi
    "double-sweep":"wfzhxzrybzwzw",  # sashi wake
    "closure-scoop": "wbexbsvs",  # katashi tome
    "zig-zag":"xmhzwbz", # kozayu
    "pivot-to-forward-point":"wezxbx",  # migi sasoi
    "weeping-l":"o",  # shiori hidari
    "weeping-r": "q",  # shiori migi
    "weeping-both":"p",  # shiori ryote
    "head left": "<",  # atama hidari e
    "head right": ">",  # atame migi e
    "head left right left": "<><",  # atama omote tsukai
    "offering":"t"
}

# shimai_dance = "zwzyx pivot-to-point open-retreat xzytqw forward-point open-retreat za"
shimai_dances_full = {
    "hasitomi-kuze":["Kneeling","Stand up","Left Stamp","Step forward, Right Stamp","Right Step pivot","Three Steps forward","Two steps backward","Mind Listening","Left Step pivot","Forward pointing","Open-retreat","Left Simple Pivot,","Three Steps forward","One Step backward","kneeling","Praying","Left Hand weeping","Stand up","Right Step pivot","Go to Square 3","Right Step pivot","Forward pointing","Open-retreat","Go to Square 2","Open fan","Right step pivot","Beckon fan","Left step pivot","Extended fan","Right Step pivot","Offering the fan","Left Step pivot","Take the flower with Left hand","Put it on the flat fan,","Two hand offering of the fan","Right Step pivot","kneeling","Pivot on knee","Look at the flower on the fan","Stand up","Large Zigzag","Left pivot","Scooping point","Open-retreat","Extended fan","Go to Square 3","Fan to the Left hand","Take the corner","Large Circle (3-9-1) ","Left step pivot","Feather fan","Left step pivot","Left hand offering the fan","Right Step pivot","Renesting the fan","Left simple pivot","Backing point","Go to Square 3 with extended fan","Take the corner with extended fan","Large Circle (3-5-8)","Small Zigzag","Closure scoop"],
    "hasitomi-kiri":["Kneeling with open fan","Stand up, Ageha","Medium Zigzag","Scooping point","Open retreat","Stand facing front","Left Simple pivot","Facing left","Right Simple pivot, facing front","Six steps towards Square 4.","Right step pivot, facing right","Two steps forward","Left Circlet, facing left","Forward pointing","Cloud fan","Right step pivot, Right Circle to Square 9.","Right Step pivot, Go to Square 3.","Take the corner, Large Circle","Forward point towards the back","Open retreat","Go to Square 9.","Right Simple pivot, Go to Square 8.","Fan to the left hand","Circlet facing right","Pillow fan","Renesting the fan","Closure scoop, Kneeling"],
    "kokaji-kuse":["Stand up","Four steps to Square 9","Forward pointing","Open-retreat","Seven steps to Square 4","Raise fan","Lashes it left and right","Four stamps","Open fan","Circle to Square 8","Scooping point","Ten steps to Square 4","Right circlet","Open retreat","Go to Square 3","Head motion L-R-L","kneeling","Point toward Bridge","Stand","Left Circle","Facing back","Scooping point","Right stamp","Open-retreat","Right Circle (5-2-8)","Close fan","Sweeping point","Scooping point","Open-retreat","Turn towards Square 5","Take three steps","Circlet","Go to Square 1","Left turn","Scooping point","Nine steps towards Square 5","Open retreat","Turn facing front","Four back steps","Closure scoop","kneeling"],
    "kokaji-kiri":["Kneeling","Stand up","Go to Square 4","kneeling","Use fan as a hammer","Hold fan with extended arms","Stand up","Right Full Circlet","Right Large circle(4-2-8)","Forward point","Right pivot","Go to Square 3","Sway the fan","Open retreat","L-R-L Head motion staring at the fan","Six Stamps and head motion L-R-L","Seven Stamps","Double sweep","Right Circle (4-2-1)","Body turn","Scooping point","Open retreat","Two hand offering of the close fan","Go to Square 5","kneeling","Put away the fan","Stand up","Nine steps back","kneeling","Bow to Square 5","Stand up","Right hand pointing","Go to Square 4","Right Circlet","Left Back jump","Stand up","Double kneeling","Go to Square 8","Right back jump","Stand up","One step to the Right","One step back","kneeling"],
    "":"zwzyxwezxbxsbyrsxzytqwszbyrssbyrsza",
}

# shimai_dances = {
#     "hasitomi-kuze":[".",":","z","w","zzz","yy","x","zsz","sbyrs","x","zzz","y",".","l","o",":","w","zsz","sbyrs","w","x","w","x","t","w",".",":","xmhzwbz","x","swbexbs","sbyrs","wzwz","x","x","t","w","x","syebs","xzxz","xmhzwbz","wbexbsvs","."],
#     "hasitomi-kiri":[".",":","xmhzwbz","swbexbs","sbyrs","x","w","zzzzzz","w","zz","xxxx","zsz","wzwz","w","zz","xzxz","zsz","sbyrs","w","wwww","wbexbsvs","."],
#     "kokaji-kuse":[".",":","zzzz","zsz","sbyrs","zzzzzzz","xzxz","swbexbs","zzzzzzzzzz","xzxz","sbyrs","<><",".",":","xzxz","swbexbs","sbyrs","wzwz","swbexbs","sbyrs","x","zzz","xxxx","zz","x","swbexbs","zzzzzzzzz","sbyrs","w","yyyy","wbexbsvs","."],
#     "kokaji-kiri":[".",":","zz",".",":","wwww","wzwz","zsz","w","zz","sbyrs","<><","wfzhxzrybzwzw","wzwz","swbexbs","sbyrs","t","zz",".",":","yyyyyyyyy",".",":","b","zz","wwww",".:.:","zz","w","y","."],
# }

shimai_dances = {
    "hasitomi-kuze":[".",":","z","w","zzz","yy","x","zsz","sbyrs","x","zzz","y","l","o","w","zsz","sbyrs","w","x","w","x","t","w","xmhzwbz","x","swbexbs","sbyrs","wzwz","x","x","t","w","x","syebs","xzxz","xmhzwbz","wbexbsvs","."],
    "hasitomi-kiri":[".",":","xmhzwbz","swbexbs","sbyrs","x","w","zzzzzz","w","zz","xxxx","zsz","wzwz","w","zz","xzxz","zsz","sbyrs","w","wwww","wbexbsvs","."],
    "kokaji-kuse":[".",":","zzzz","zsz","sbyrs","zzzzzzz","xzxz","swbexbs","zzzzzzzzzz","xzxz","sbyrs","<><","xzxz","swbexbs","sbyrs","wzwz","swbexbs","sbyrs","x","zzz","xxxx","zz","x","swbexbs","zzzzzzzzz","sbyrs","w","yyyy","wbexbsvs","."],
    "kokaji-kiri":[".",":","zz","wwww","wzwz","zsz","w","zz","sbyrs","<><","wfzhxzrybzwzw","wzwz","swbexbs","sbyrs","t","zz","yyyyyyyyy","b","zz","wwww","zz","w","y","."],
}


# RULES
# "scooping-point + zigzag": "indicates the end of a section or dance"
# "large circling": "This overall motion from front to backstage, from a strong stage position to a weaker one, has the effect of releasing the tension"
# "stamp": "While single and double stamps fall in the category of Structural patterns, sequences of stamps constitute a Mimetic pattern. Most dances start with a single or double stamp, and most Noh performances conclude with a double stamp"
# "opening fan":"Opening the fan (ōgi hiraki) marks the beginning of a new section in a dance"
# "closing fun":"The closing of the fan (ōgi subomeru) can be performed solemnly at the end of a dance, or inconspicuously anytime close to the end of a dance"
# "Moving fun to the Left Hand":"This pattern often marks the end of a section in a dance"
# "Large zigzag (ōzayu)":"Its overall motion from the back to the front of the stage gives it a raising-tension quality"
# "Medium zigzag (chūzayu)":"It often functions as a transition between two sections"
# "Scooping point (kaikomi) + the Small zigzag (kozayu)": "end of a section or dance"
# "Open-retreat (hiraki)":"the pointing pattern was used to identify an object to contemplate, and the Open-retreat was a stepping back motion to better contemplate the identified object"
# "Cloud fan(uchiyage)":"This pattern is a dynamic way to look into the distance, often at something high in the sky like clouds or the moon"
# "Pillow Fan (makura no ōgi)":"The pattern suggests laying the head against a pillow, giving the impression that the character is sleeping or dreaming. It may also be used to indicate embarrassment or the disappearance of the character, so it could also belongs in the mimetic group of patterns"
# "Feather Fan (hane ōgi)":"The poetic name of this pattern comes from the flapping of the fan and the swishing sound of the sleeves, reminiscent of a bird’s plumage fluttering in the wind"
# "Offering the Fan (ōgi mae dashi)":"this pattern suggests that an object is passing from one person to another. This pattern can also suggest the dancer is looking out at something"
# "jumps ":"Jumps usually feature in plays about lively gods, demons, or warriors. They can be used merely for the effect, or they may carry referential meaning"
