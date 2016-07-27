# -*- coding: utf-8 -*-

import operator

def check_conditions(s_value, conditions):
    res = True

    print len(conditions)

    for a in conditions:
        # print s_value, a["opr"], a["val"]
        # print operators[a["opr"]](int(s_value), a["val"])
        res &= operators[a["opr"]](int(s_value), a["val"])

    return res


operators = {"eg": operator.eq, "lt": operator.lt, "gt": operator.gt, "le": operator.le, "ge": operator.ge, "ne": operator.ne}

# sceneTriggers = {"Test": [{"scene": "Test", "conditions": [ {"opr": "lt", "val": 90}, {"opr": "gt", "val": 40}]},
#                            {"scene": "Test", "conditions": [ {"opr": "lt", "val": 90}, {"opr": "gt", "val": 40}]} ]}

sceneTriggers = {"Test": [
                    {"scene": "Test_Low", "conditions": [ {"opr": "lt", "val": 90} ] },
                    {"scene": "Test", "conditions": [ {"opr": "lt", "val": 90}, {"opr": "gt", "val": 40}]}
                ]}

# print sceneTriggers

target = "Test"

if target in sceneTriggers:
    currentTrigger = sceneTriggers[target]
    for a in currentTrigger:
        print a["conditions"]
        print check_conditions(s_value="50", conditions=a["conditions"])
    #print check_conditions("30", currentTrigger["conditions"])


#print check_conditions("50", test["conditions"])
