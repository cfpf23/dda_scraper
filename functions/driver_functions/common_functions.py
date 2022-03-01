from re import S
from ..utility_functions.utility_functions import get_elements_css_attr_re , get_element_css_attr_re
from ..utility_functions.decorators import run_once
from ..parsing_functions.parsing_functions import mapping
from .rendering_driver_functions import driver_actions
from typing import Callable, Dict, List, Union, Optional, Any
from engines.playwright.playwright_engine import PlaywrightDriver
from engines.scrapy.scrapy_engine import ScrapyEngine



def map_function(parsing_function: str, field_data: Union[str, List[str]], args: Dict[str, str]) -> Any:
    return mapping(parsing_function)(field_data, args) if args else mapping(parsing_function)(field_data)


def apply_parsing_function_element(field_data: str, parsing_functions: Dict[str, Dict[str, str]]) -> Any:
    for parsing_function, args in parsing_functions.items():
        field_data = map_function(parsing_function, field_data, args)
    return field_data


def apply_parsing_function_collection(field_data: List[str], input_processing: Dict[str, Dict[str, str]]) -> List[Any]:
    for parsing_function, args in input_processing.items():
        field_data = [map_function(parsing_function, data, args) for data in field_data]
    return field_data


def get_field_data(driver: Union[ScrapyEngine, PlaywrightDriver], step: Dict[str, Dict[str, str]]) -> Optional[str]:
    css, attr, re = get_element_css_attr_re(step)

    if attr:
        return driver.get_attribute(css, attr)
    elif re:
        return driver.get_element_re(css, re)

    return driver.get_element(css)


def get_field_data_container(driver: Union[ScrapyEngine, PlaywrightDriver], parent_selector, step: Dict[str, Dict[str, str]]) -> Optional[str]:
    css, attr, re = get_element_css_attr_re(step)

    if attr and re:
        return driver.get_attribute_container_re(parent_selector, css, attr, re)
    elif attr:
        return driver.get_attribute_container(parent_selector, css, attr)
    elif re:
        return driver.get_element_container_re(parent_selector, css, re)

    return driver.get_element_container(parent_selector, css)


def get_field_data_all(driver: Union[ScrapyEngine, PlaywrightDriver], step: Dict[str, Dict[str, str]]) -> List[Optional[str]]:
    css, attr, re = get_elements_css_attr_re(step)

    if attr:
        return driver.get_attributes(css, attr)
    elif re:
        return driver.get_element_re(css, re)

    return driver.get_elements(css)


def get_field_data_container_all(driver: Union[ScrapyEngine, PlaywrightDriver], parent_selector, step: Dict[str, Dict[str, str]]) -> List[Optional[str]]:
    css, attr, re = get_elements_css_attr_re(step)

    if attr:
        return driver.get_attributes_container(parent_selector, css, attr)
    elif re:
        return driver.get_element_container_re(parent_selector, css, re)

    return driver.get_elements_container(parent_selector, css)


def single_element_process_container(driver: Union[ScrapyEngine, PlaywrightDriver], parent_selector, step: Dict[str, Dict[str, str]]) -> Any:
    field_data = get_field_data_container(driver, parent_selector, step)
    parsing_functions = step.get("parsing_functions")
    field_data = apply_parsing_function_element(field_data, parsing_functions)

    return field_data


def single_element_process(driver: Union[ScrapyEngine, PlaywrightDriver], step: Dict[str, Dict[str, str]]) -> Any:
    field_data = get_field_data(driver, step)
    parsing_functions = step.get("parsing_functions")
    field_data = apply_parsing_function_element(field_data, parsing_functions)

    return field_data


def multiple_element_process(driver: Union[ScrapyEngine, PlaywrightDriver], step: Dict[str, Dict[str, str]]) -> Any:
    parsing_functions = step.get("parsing_functions")
    input_processing, output_processing = parsing_functions.get("input"), parsing_functions.get("output")

    field_data = get_field_data_all(driver, step)
    field_data = apply_parsing_function_collection(field_data, input_processing)
    field_data = apply_parsing_function_element(field_data, output_processing)

    return field_data


def multiple_element_process_container(driver: Union[ScrapyEngine, PlaywrightDriver], parent_selector, step: Dict[str, Dict[str, str]]) -> Any:
    parsing_functions = step.get("parsing_functions")
    input_processing, output_processing = parsing_functions.get("input"), parsing_functions.get("output")

    field_data = get_field_data_container_all(driver, parent_selector, step)
    field_data = apply_parsing_function_collection(field_data, input_processing)
    field_data = apply_parsing_function_element(field_data, output_processing)

    return field_data


def process_config_scenarios(fields_scenarios, driver: Union[ScrapyEngine, PlaywrightDriver]) -> Dict[str, Any]:
    item = {}
    for field, field_scenarios in fields_scenarios.items():
        item[field] = None
        field_data = None
        for field_scenario in field_scenarios:
            for step in field_scenario:
                field_data = map_step(step)(driver, step)
            if field_data is not None:
                item[field] = field_data
    return item

def process_config_scenarios_container(fields_scenarios, driver: Union[ScrapyEngine, PlaywrightDriver], child_selector) -> Dict[str, Any]:
    item = {}
    for field, field_scenarios in fields_scenarios.items():
        item[field] = None
        field_data = None
        for field_scenario in field_scenarios:
            field_data = None
            for step in field_scenario:
                field_data = map_step_container(step)(driver, child_selector, step)
            if field_data is not None:
                item[field] = field_data
    return item

def map_step(step: Dict[str, Dict[str, str]]) -> Optional[Callable]:
    possible_steps = {
        "get_element": single_element_process,
        "get_elements": multiple_element_process
    }
    for step_name, step_process in possible_steps.items():
        if step.get(step_name):
            return step_process
    return driver_actions

def map_step_container(step: Dict[str, Dict[str, str]]) -> Optional[Callable]:
    possible_steps = {
        "get_element": single_element_process_container,
        "get_elements": multiple_element_process_container
    }
    for step_name, step_process in possible_steps.items():
        if step.get(step_name):
            return step_process
    return driver_actions


@run_once
def on_enter_once(driver: Union[ScrapyEngine, PlaywrightDriver], on_enter_once_scenarios) -> None:
    if on_enter_once_scenarios:
        for scenario in on_enter_once_scenarios:
            for step in scenario:
                driver_actions(driver, step)

def on_enter_every_time(driver: Union[ScrapyEngine, PlaywrightDriver], on_enter_every_time_scenarios) -> None:
    if on_enter_every_time_scenarios:
        for scenario in on_enter_every_time_scenarios:
            for step in scenario:
                driver_actions(driver, step)

def pagination(driver: Union[ScrapyEngine, PlaywrightDriver], pagination_scenarios):
    if pagination_scenarios:
        for scenario in pagination_scenarios:
            for step in scenario:
                result = driver_actions(driver, step)
                if result:
                    return result
    return False

