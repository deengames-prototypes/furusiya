#!/usr/bin/env python3
class Entity:
    def __init__(self):
        self.components = {}

    def set(self, component):
        key = type(component)
        self.components[key] = component

    def get(self, component_type):
        return self.components[component_type]