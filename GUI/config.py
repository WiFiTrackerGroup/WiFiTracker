ROOMS = {
    "Even": {
        "image_path": "Image\Room_Even.bmp",
        "room_list":{
            "AULA02":{
                "X": 1010.2526881720432,
                "Y": 327.5
            },
            "AULA04":{
                "X": 586.1666666666667,
                "Y": 330.9408602150538
            },
            "AULA06":{
                "X": 246.38172043010752,
                "Y": 306.85483870967744
            }
        }
    },
    "Odd": {
        "image_path": "Image\Room_Odd.bmp",
        "room_list":{
            "AULA01":{
                "X": 969.8225806451615,
                "Y": 396.3172043010753
            },
            "AULA03":{
                "X": 616.2741935483872,
                "Y": 395.45698924731187
            },
            "AULA05":{
                "X": 266.1666666666667,
                "Y": 392.01612903225805
            }
        }
    },
    "P": {
        "image_path": "Image\Room_P.bmp",
        "room_list":{
            "AULA1P":{
                "X": 877.7795698924733,
                "Y": 534.8118279569892
            },
            "AULA2P":{
                "X": 885.5215053763443,
                "Y": 186.42473118279577
            },
            "AULA3P":{
                "X": 336.70430107526886,
                "Y": 537.3924731182797
            },
            "AULA4P":{
                "X": 354.76881720430106,
                "Y": 182.1236559139785
            }
        }
    },
    "R Ground Floor": {
        "image_path": "Image\Room_R_G.bmp",
        "room_list":{
            "AULAR1":{
                "X": 793.478494623656,
                "Y": 486.6397849462366
            },
            "AULAR2":{
                "X": 513.0483870967743,
                "Y": 490.08064516129036
            },
            "AULAR3":{
                "X": 1092.8333333333335,
                "Y": 451.3709677419355
            },
            "AULAR4":{
                "X": 174.1236559139785,
                "Y": 470.2956989247312
            }
        }
    },
    "R First Floor": {
        "image_path": "Image\Room_R_1.bmp",
        "room_list":{
            "AULAR1":{
                "X": 757.3494623655915,
                "Y": 298.252688172043
            },
            "AULAR2":{
                "X": 491.54301075268825,
                "Y": 314.5967741935484
            },
            "AULAR3":{
                "X": 1094.5537634408604,
                "Y": 275.0268817204302
            },
            "AULAR4":{
                "X": 167.24193548387098,
                "Y": 293.95161290322585
            }, 
            "AULAR1B":{
                "X": 779.715053763441,
                "Y": 461.6935483870968
            },
            "AULAR2B":{
                "X": 494.1236559139785,
                "Y": 481.47849462365593
            },
            "AULAR3B":{
                "X": 1104.0161290322583,
                "Y": 432.44623655913983
            },
            "AULAR4B":{
                "X": 156.9193548387097,
                "Y": 465.1344086021506
            }
        }
    }
}

PSW_MONGODB = "hcgFRD3G!f"
USER_MONGODB = "wifitracker"
HOST_MONGODB = "127.0.0.1"
PORT_MONGODB = "27017"
DBNAME = "WifiTracker2024"
COUNTNAME = "counting"
TRACKNAME = "tracking"
FILE_ERRORS = "sub/log/mongoDB_log.txt"
URL_DB = f"mongodb://{USER_MONGODB}:{PSW_MONGODB}@{HOST_MONGODB}:{PORT_MONGODB}/{DBNAME}"