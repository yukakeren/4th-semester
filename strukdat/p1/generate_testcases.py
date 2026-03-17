from pathlib import Path

testcases = {
    1: {
        "in": """8
PLAN 10
PLAN 50
GO_OUT
MOOD 50
PLAN 5
GO_OUT
GO_OUT
GO_OUT
""",
        "out": """50
60
5
No one is going out
"""
    },
    2: {
        "in": """3
GO_OUT
PLAN 7
GO_OUT
""",
        "out": """No one is going out
7
"""
    },
    3: {
        "in": """4
MOOD 100
PLAN 20
GO_OUT
GO_OUT
""",
        "out": """120
No one is going out
"""
    },
    4: {
        "in": """6
PLAN 30
MOOD 10
GO_OUT
PLAN 5
GO_OUT
GO_OUT
""",
        "out": """40
5
No one is going out
"""
    },
    5: {
        "in": """6
PLAN 40
MOOD 10
MOOD 25
GO_OUT
PLAN 8
GO_OUT
""",
        "out": """65
8
"""
    },
    6: {
        "in": """8
PLAN 12
PLAN 90
PLAN 45
GO_OUT
GO_OUT
GO_OUT
PLAN 7
GO_OUT
""",
        "out": """90
45
12
7
"""
    },
    7: {
        "in": """7
PLAN 10
PLAN 20
MOOD 5
GO_OUT
GO_OUT
GO_OUT
PLAN 1
""",
        "out": """25
10
No one is going out
"""
    },
    8: {
        "in": """10
PLAN 3
PLAN 17
MOOD 4
PLAN 9
GO_OUT
GO_OUT
MOOD 100
GO_OUT
PLAN 2
GO_OUT
""",
        "out": """21
9
103
2
"""
    },
    9: {
        "in": """5
GO_OUT
GO_OUT
PLAN 11
GO_OUT
GO_OUT
""",
        "out": """No one is going out
No one is going out
11
No one is going out
"""
    },
    10: {
        "in": """6
PLAN 1000000
PLAN 999999
MOOD 123456
GO_OUT
GO_OUT
GO_OUT
""",
        "out": """1123456
999999
No one is going out
"""
    },
    11: {
        "in": """12
PLAN 15
PLAN 25
MOOD 30
GO_OUT
PLAN 5
MOOD 2
PLAN 100
GO_OUT
GO_OUT
GO_OUT
PLAN 1
GO_OUT
""",
        "out": """55
102
15
5
1
"""
    },
    12: {
        "in": """7
MOOD 9
GO_OUT
PLAN 4
GO_OUT
MOOD 20
GO_OUT
PLAN 6
""",
        "out": """No one is going out
13
No one is going out
"""
    },
}

base = Path(".")
for i, tc in testcases.items():
    (base / f"{i}.in").write_text(tc["in"], encoding="utf-8")
    (base / f"{i}.out").write_text(tc["out"], encoding="utf-8")

print(f"Generated {len(testcases)} input/output file pairs.")
