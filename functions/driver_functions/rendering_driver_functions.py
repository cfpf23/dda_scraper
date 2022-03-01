from re import S
from typing import Callable, Dict, Optional, Union, Any
from engines.playwright.playwright_engine import PlaywrightDriver
from engines.scrapy.scrapy_engine import ScrapyEngine


def driver_actions(
    driver: Union[ScrapyEngine, PlaywrightDriver], action: Dict[str, Dict[str, Union[str, int]]]
) -> bool:
    for function, arguments in action.items():
        return_val = function_list(driver, function)(**arguments)
        if return_val:
            return return_val


def function_list(driver: Union[ScrapyEngine, PlaywrightDriver], key: str) -> Callable:
    if isinstance(driver, ScrapyEngine):
        mapping = {
            "go_to": driver.go_to,
        }
    else:
        mapping = {
            "click": driver.click,
            "click_postion": driver.click_position,
            "pagination_click": driver.pagination_click,
            "move": driver.move,
            "wait": driver.wait,
            "scroll": driver.scroll,
            "go_to": driver.go_to,
            "solve_amazon_captcha": driver.solve_amazon_captcha,
            "infinite_scroll": driver.infinite_scroll,
            "focus_on": driver.focus_on,
            "hover_on": driver.hover_on,
        }
    return mapping.get(key)

