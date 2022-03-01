from re import L, S
import yaml
from yaml.loader import Loader
from importlib import import_module
from typing import Dict, List, Optional, Union

class YamlConfigExeption(Exception):
    pass


class YamlInterpreter:
    def __init__(self, filepath: str, scraping_type: str):
        self.config = self._open_yaml_config(filepath)
        self.scraping_type_exist(scraping_type)
        self.scraping_type = scraping_type

    def _open_yaml_config(self, filepath: str):
        with open(filepath, "r") as stream:
            config = yaml.load(stream, Loader=self._get_loader())
        return config

    def _func_loader(self, loader: yaml.SafeLoader, node: str):
        """A loader for functions."""
        params = loader.construct_mapping(node)  # get node mappings
        m = import_module(params["module"])
        if isinstance(params["name"], str):
            return getattr(m, params["name"])  # get function from module

    def _get_loader(self) -> yaml.SafeLoader:
        """Return a yaml loader."""
        loader = yaml.SafeLoader
        loader.add_constructor("!Func", self._func_loader)
        return loader

    def scraping_type_exist(self, scraping_type: str) -> None:
        if not self.config.get(scraping_type):
            raise YamlConfigExeption(
                f"scraping type: {scraping_type} does not exist in the specified yaml file"
            )

    @property
    def input_path(self) -> str:
        return self.config["options"]["input_path"]

    @property
    def rotate_proxy(self) -> str:
        return self.config["options"]["scrape_options"]["rotate_proxy"]

    @property
    def proxy_address(self) -> str:
        return self.config["options"]["scrape_options"]["proxy"]["address"]

    @property
    def proxy_username(self) -> str:
        return self.config["options"]["scrape_options"]["proxy"]["username"]

    @property
    def proxy_password(self) -> str:
        return self.config["options"]["scrape_options"]["proxy"]["password"]

    @property
    def proxy_connetion_string(self) -> str:
        return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_address}"

    @property
    def engine(self) -> str:
        return self.config["options"]["scrape_options"]["engine"]

    @property
    def headers(self) -> str:
        return self.config["options"]["scrape_options"]["headers"]

    @property
    def engine_args(self) -> List[str]:
        return self.config["options"]["scrape_options"]["engine_args"]

    @property
    def download_delay(self) -> str:
        return self.config[self.scraping_type]["options"]["download_delay"]

    @property
    def pagination(self) -> Optional[Dict[str, Dict[str, List[List[Dict[str, Dict[str, str]]]]]]]:
        pagination = self.config[self.scraping_type].get("pagination")
        if pagination:
            return pagination.get("scenarios")

    @property
    def engine_settings(self):
        return self.config.get("options").get("scrape_options").get("engine_settings")

    @property
    def engine_settings_playwright_user_agent(self):
        engine_settings = self.config.engine_settings
        return engine_settings.get("user_agent")

    @property
    def engine_settings_playwright_vi(self):
        engine_settings = self.config.engine_settings
        return engine_settings.get("headers")

    @property
    def engine_settings_playwright_headers(self):
        engine_settings = self.config.engine_settings
        return engine_settings.get("headers")

    def get_all_fields(self) -> List[str]:
        return [*self.config[self.scraping_type]["fields"]]

    def get_all_fields_containers(self) -> List[str]:
        all_container_fields = []
        for container in self.config[self.scraping_type]["containers"]:
            all_container_fields += [*container["fields"]]
        return all_container_fields

    def get_all_field_scenarios(self, field:str) -> List[List[Dict[str, Dict[str, str]]]]:
        return self.config[self.scraping_type]["fields"][field]["scenarios"]

    def get_all_field_scenarios_container(self, index: int, field: str) -> List[List[Dict[str, Dict[str, str]]]]:
        return self.config[self.scraping_type]["containers"][index]["fields"][field]["scenarios"]

    def get_on_enter_scraping_type_scenarios(self) -> Optional[Dict[str, Dict[str, List[List[Dict[str, Dict[str, str]]]]]]]:
        scenarios = self.config[self.scraping_type].get("on_enter")
        if scenarios:
            return scenarios.get("scenarios")

    def get_all_container_scenarios(self):
        return self.config[self.scraping_type]["containers"]

    def get_on_enter_once_scenarios(self) -> Optional[Dict[str, Dict[str, List[List[Dict[str, Dict[str, str]]]]]]]:
        if self.config.get("on_enter"):
            return self.config.get("on_enter").get("scenarios")

    def get_fields_scenarios(self) -> Dict[str, List[List[Dict[str, Dict[str, str]]]]]:
        fields = self.get_all_fields()
        return {field: self.get_all_field_scenarios(field) for field in fields}
    
    def get_fields_scenarios_container(self, container_fields: Dict[str, Dict[str, List[List[Dict[str, Dict[str, str]]]]]]) -> Dict[str, List[List[Dict[str, Dict[str, str]]]]]:
        return {field: scenario.get("scenarios") for field, scenario in container_fields.items()}


def main():
    document = "C:/Users/Olaf/Desktop/spider_template/e_retailer_library/elgiganten_dk.yaml"
    # scraping_type is type of page to scrape taken from the yaml with fields
    yaml_conf = YamlInterpreter(filepath=document, scraping_type="listing")
    print(yaml_conf.engine_settings)
    # containers = yaml_conf.get_all_container_scenarios()
    # for container in containers:
    #     parent_selector = container.get("parent_selector")
    #     page_type = container.get("page_type")
    #     fields_to_scrape = container.get("fields")
    #     # print(fields_to_scrape)
    #     print(yaml_conf.get_fields_scenarios_container(fields_to_scrape))
    # print(yaml_conf.get_all_field_scenarios_container(0, "sku"))
    # print(containers)
    # yaml_conf = YamlInterpreter(filepath=document, scraping_type="product_card")
    # print(yaml_conf.get_fields_scenarios())


if __name__ == "__main__":
    main()
