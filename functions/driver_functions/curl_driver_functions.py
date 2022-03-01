def driver_actions(driver, action):
    for function, arguments in action.items():
        return_val = function_list(driver, function)(**arguments)
        if return_val:
            return return_val


def function_list(driver, key):
    mapping = {
        "go_to": driver.go_to,
    }
    return mapping.get(key)