import os

ROOMS = {
    "Even": {
        "name": "Even Room",
        "color": "red",
        "image_path": "Room_Even.bmp",
        "coordinate_path": "Even.pkl",
        "room_list":{
            "AULA2":{
                "X": [1186.1766872932371, 1189.2109704789534, 845.325542764429, 842.2912595787125],
                "Y": [498.700269714061, 187.18052931384466, 186.16910158527253, 497.68884198548886]
            },
            "AULA4":{
                "X": [838.245548664424, 837.7398348001379, 412.4344749355567, 412.9401887998427],
                "Y": [496.67741425691673, 187.68624317813078, 185.1576738567004, 497.1831281212028]
            },
            "AULA6":{
                "X": [388.6659233141116, 98.38616521390998, 98.38616521390998, 389.6773510426837],
                "Y": [493.1374172069143, 493.64313107120034, 115.87487444950943, 116.38058831379556]
            }
        }
    },
    
    "Odd": {
        "name": "Odd Room",
        "color": "blue",
        "image_path": "Room_Odd.bmp",
        "coordinate_path": "Odd.pkl",
        "room_list":{
            "AULA01":{
                "X": [804.8684336215435, 922.6997640001969, 950.5140265359305, 1000.073985235965, 1029.9111032288429, 1148.2481474717822, 1148.2481474717822, 1096.6653333146035, 1052.1625132574297, 899.942640107324, 853.922678457292, 805.8798613501158],
                "Y": [162.40054996382742, 162.90626382811354, 202.85765910671273, 202.3519452424266, 164.42340542097168, 162.40054996382742, 566.4659275283938, 567.9830691212519, 634.7372992070126, 634.7372992070126, 565.9602136641076, 562.9259304783914]
                },
            "AULA03":{
                "X": [444.29444838557885, 572.2400560499534, 598.0314631285428, 650.1199911500075, 677.4285398214552, 790.7084454215337, 793.2370147429642, 740.1370589929272, 694.6228112071813, 553.0229292070828, 503.4629705070485, 451.88015634986976],
                "Y": [161.8948360995414, 162.90626382811354, 199.82337592099634, 198.8119481924242, 162.40054996382742, 162.40054996382742, 563.9373582069634, 563.9373582069634, 631.7030160212962, 637.265868528443, 564.9487859355356, 563.4316443426774]
                },
            "AULA05":{
                "X": [100.9147345353403, 231.8946253854313, 256.16889087116243, 306.74027729976893, 338.0945368855051, 433.6744572355714, 431.14588791414116, 389.6773510426837, 343.15167552836573, 200.54036579969517, 152.497548692519, 97.37473748533785],
                "Y": [160.88340837096928, 162.40054996382742, 198.8119481924242, 200.83480364956847, 160.88340837096928, 162.40054996382742, 562.4202166141052, 565.9602136641076, 634.2315853427265, 634.7372992070126, 563.9373582069634, 561.9145027498191]
                }
        }
    },
    
    "P": {
        "name": "Room P",
        "color": "purple",
        "image_path": "Room_P.bmp",
        "coordinate_path": "P.pkl",
        "room_list":{
            "AULA1P":{
                "X": [705.2428023571888, 704.2313746286165, 1067.3339291860116, 1065.8167875931535],
                "Y": [425.8774732568676, 632.2087298855822, 632.2087298855822, 422.8431900711512]
            },
            "AULA2P":{
                "X": [1067.8396430502978, 1066.8282153217256, 704.7370884929026, 704.2313746286165],
                "Y": [290.85187149248804, 84.5206148637734, 83.00347327091515, 291.8632992210602]
            },
            "AULA3P":{
                "X": [175.25467258539192, 176.77181417825017, 536.8400855499287, 538.357227142787],
                "Y": [630.185874428438, 423.34890393543725, 424.86604552829544, 631.7030160212962]
            },
            "AULA4P":{
                "X": [538.357227142787, 537.345799414215, 174.7489587211059, 175.76038644967804],
                "Y": [291.8632992210602, 84.01490099948728, 83.50918713520127, 291.35758535677417]
            }
        }
    },
    
    "R_G": {
        "name": "Room R ground floor",
        "color": "yellow",
        "image_path": "Room_R_G.bmp",
        "coordinate_path": "R_G.pkl",
        "room_list":{
            "AULAR1":{
                "X": [684.50853392146, 879.2083716715952, 899.942640107324, 700.691377578614],
                "Y": [440.54317532116346, 391.99464434970116, 521.9631074712199, 549.7773700069536]
            },
            "AULAR2":{
                "X": [413.95161652841483, 612.1914513285526, 623.8228702071322, 423.5601799498501],
                "Y": [454.1974496568872, 419.8089068854348, 549.2716561426676, 566.4659275283938]
            },
            "AULAR3":{
                "X": [989.9597079502437, 1188.7052566146674, 1189.2109704789534, 988.9482802216714],
                "Y": [402.6146354997086, 385.4203641139823, 516.9059688283594, 515.3888272355011]
            },
            "AULAR4":{
                "X": [85.74331860675835, 288.5345781854706, 271.8460206640305, 72.5947581353206],
                "Y": [408.68320187114136, 415.7631959711463, 545.731659092665, 521.4573936069339]
            }
        }
    },
    
    "R_1": {
        "name": "Room R first floor",
        "color": "green",
        "image_path": "Room_R_1.bmp",
        "coordinate_path": "R_G.pkl",
        "room_list":{
            "AULAR1":{
                "X": [647.085707964291, 854.428392321578, 876.1740884858789, 670.3485457214501],
                "Y": [241.7976266567398, 209.43193934243152, 366.20323727111185, 395.5346413997036]
            },
            "AULAR2":{
                "X": [377.03450443553214, 584.377188792819, 598.5371769928288, 391.19449263554196],
                "Y": [254.94618712817748, 236.23477414959302, 394.5232136711315, 412.7289127854299]
            },
            "AULAR3":{
                "X": [993.4997050002462, 1202.3595309503912, 1202.3595309503912, 995.5225604573905],
                "Y": [201.34051751385448, 199.82337592099634, 356.5946738496766, 357.1003877139627]
            },
            "AULAR4":{
                "X": [77.14618291389519, 284.4888672711821, 262.7431711068812, 56.41191447816652],
                "Y": [207.40908388528726, 233.20049096387663, 390.98321662112903, 362.6632402211094]
            }, 
            "AULAR1B":{
                "X": [671.3599734500224, 876.6798023501649, 900.44835397161, 692.599955750037],
                "Y": [401.09749390685033, 370.75466204968643, 523.4802490640782, 552.8116531926701]
            },
            "AULAR2B":{
                "X": [390.68877877125584, 598.5371769928288, 611.6857374642666, 403.3316253784075],
                "Y": [416.26890983543234, 399.0746384497061, 551.8002254640978, 570.0059245783962]
            },
            "AULAR3B":{
                "X": [995.0168465931042, 1204.8881002718215, 1203.8766725432495, 994.0054188645322],
                "Y": [362.6632402211094, 364.68609567825365, 515.3888272355011, 516.9059688283594]
            },
            "AULAR4B":{
                "X": [57.92905607102472, 263.24888497116734, 246.05461358544113, 36.68907377100999],
                "Y": [366.7089511353979, 394.5232136711315, 548.2602284140954, 521.4573936069339]
            }
        }
    }
}

ROOM_LIST ={
    "Even": {
        "name": "Even Rooms",
        "color": "red",
        "room_list":[
            "AULA2",
            "AULA4",
            "AULA6",
            "AULA08",
            "AULA10",
            "AULA12",
            "AULA14",
            "AULA16"
        ]
    },
    
    "Odd": {
        "name": "Odd Rooms",
        "color": "blue",
        "room_list":[
            "AULA01",
            "AULA03",
            "AULA05",
            "AULA11",
            "AULA13",
            "AULA15",
            "AULA17",
            "AULA19",
            "AULA21",
            "AULA23",
            "AULA25",
            "AULA27",
            "AULA29"
        ]
    },
    
    "P": {
        "name": "Rooms P",
        "color": "purple",
        "room_list":[
            "AULA1P",
            "AULA2P",
            "AULA3P",
            "AULA4P"
        ]
    },
    
    "R": {
        "name": "Rooms R",
        "color": "green",
        "room_list":[
            "AULAR1",
            "AULAR2",
            "AULAR3",
            "AULAR4", 
            "AULAR1B",
            "AULAR2B",
            "AULAR3B",
            "AULAR4B"
        ]
    },

    "I": {
        "name": "Rooms I",
        "color": "yellow",
        "room_list":[
            "AULA1I",
            "AULA2I",
            "AULA3I",
            "AULA4I",
            "AULA5I",
            "AULA6I",
            "AULA7I",
            "AULA8I",
            "AULA9I"
        ]
    }

}

PSW_MONGODB = "ciao"
USER_MONGODB = "root"
HOST_MONGODB = "127.0.0.1"
PORT_MONGODB = "27017"
DBNAME = "WifiTracker2024"
COUNTNAME = "counting"
TRACKNAME = "tracking"
RAWNAME = "raw_data"
SCHEDULE = 900
path = os.path.dirname(os.path.abspath(__file__))
FILE_ERRORS = os.path.join(path,"sub", "log", "mongoDB_log.txt")
URL_DB = f"mongodb://{USER_MONGODB}:{PSW_MONGODB}@{HOST_MONGODB}:{PORT_MONGODB}"
