from pydantic import BaseModel
import string
from typing import Optional


class Template(BaseModel):
    name: str
    prompt: Optional[str]
    system: Optional[str]
    model: Optional[str]

    class Config:
        extra = "forbid"

    class MissingVariables(Exception):
        pass

    def execute(self, input, params=None):
        params = params or {}
        params["input"] = input
        if not self.prompt:
            system = self.interpolate(self.system, params)
            prompt = input
        else:
            prompt = self.interpolate(self.prompt, params)
            system = self.interpolate(self.system, params)
        return prompt, system

    @classmethod
    def interpolate(cls, text, params):
        if not text:
            return text
        # Confirm all variables in text are provided
        string_template = string.Template(text)
        vars = cls.extract_vars(string_template)
        missing = [p for p in vars if p not in params]
        if missing:
            raise cls.MissingVariables(
                "Missing variables: {}".format(", ".join(missing))
            )
        return string_template.substitute(**params)

    @staticmethod
    def extract_vars(string_template):
        return [
            match.group("named")
            for match in string_template.pattern.finditer(string_template.template)
        ]
