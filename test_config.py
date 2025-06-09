# two_solutions, single_solution, complex_solutions, no_solutions
active_config = "single_solution"

test_configs = {
    "two_solutions": {
        "step_0": [
            2,
            1,
        ],
        "step_1": [
            "x**3 + 2 * y**2",
            "2 * x + y"
        ],
        "step_2": [
            "3 * x**2 - 2*λ1",
            "4 * y - λ1",
            "-2 * x - y"
        ],
        "step_3": [
            "-16/3",
            "32/3",
            "128/3"
        ],
        "step_4": [
            "6 * x",
            "0",
            "0",
            "4",
        ],
        "step_5": [
            "-128"
        ]
    },
    "single_solution": {
         "step_0": [
            2,
            1,
        ],
        "step_1": [
            "3*x + 2",
            "x * y"
        ],
        "step_2": [
            "-y*λ1+3",
            "-x*λ1",
            "-x*y"
        ],
        "step_3": [
            "0",
            "3/λ1",
            "λ1"
        ],
        "step_4": [
            "6 * x",
            "0",
            "0",
            "4",
        ],
        "step_5": [
            "-128"
        ]
    },
    "complex_solutions": {
        "step_0": [
            1,
            1,
        ],
        "step_1": [
            "x**2 + y**2 + 1",
            "x + y"
        ],
        "step_2": [
            "2 * x - λ1",
            "2 * y - λ1",
            "-x - y"
        ],
        "step_3": [
            "i",
            "-i",
            "2"
        ],
        "step_4": [
            "2",
            "0",
            "0",
            "2",
        ],
        "step_5": [
            "4"
        ]
    },
    "no_solutions": {
        "step_0": [
            1,
            1,
        ],
        "step_1": [
            "x**2 + y**2 + 2",
            "x + y"
        ],
        "step_2": [
            "2 * x - λ1",
            "2 * y - λ1",
            "-x - y"
        ],
        "step_3": [
            "0",
            "0",
            "0"
        ],
        "step_4": [
            "2",
            "0",
            "0",
            "2",
        ],
        "step_5": [
            "0"
        ]
    }
}

# Export configuration based on active_config
test_config_step0 = test_configs[active_config]["step_0"]
test_config_step1 = test_configs[active_config]["step_1"]
test_config_step2 = test_configs[active_config]["step_2"]
test_config_step3 = test_configs[active_config]["step_3"]
test_config_step4 = test_configs[active_config]["step_4"]
test_config_step5 = test_configs[active_config]["step_5"]