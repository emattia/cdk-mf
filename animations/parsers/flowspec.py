import os
import sys
import ast
import inspect
import importlib.util
from pathlib import Path
from metaflow import FlowSpec

def get_flow_spec_class(module):
    """
    Find and return the FlowSpec class in the given module.
    Returns the first class found that inherits from FlowSpec.
    """
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) and 
            issubclass(obj, FlowSpec) and 
            obj != FlowSpec):
            return obj
    return None

# Using the previously imported module
# flow_spec_class = get_flow_spec_class(flow_module)

def load_flow_from_file(flow_path):
    """
    Load a Metaflow FlowSpec class from a Python file.
    
    Args:
        flow_path (str): Path to the Python file containing the FlowSpec
        
    Returns:
        class: The FlowSpec class defined in the file
    """
    # Convert to Path object and resolve to absolute path
    flow_path = Path(flow_path).resolve()
    
    # Create spec from file path
    spec = importlib.util.spec_from_file_location(flow_path.stem, flow_path)
    flow_module = importlib.util.module_from_spec(spec)
    
    # Add to sys.modules and execute
    sys.modules[flow_path.stem] = flow_module
    spec.loader.exec_module(flow_module)
    
    # Find the FlowSpec class
    flow_spec_class = get_flow_spec_class(flow_module)
    
    if flow_spec_class is None:
        raise ValueError(f"No FlowSpec class found in {flow_path}")
        
    return flow_spec_class


class SimpleFlowGraph:
    def __init__(self, flow):
        self.name = flow.__name__
        self.nodes = {}
        self._create_nodes(flow)
        self.sorted_nodes = []
        self._traverse_graph()

    def _create_nodes(self, flow):
        """Extract steps from the flow class"""
        for name, method in inspect.getmembers(flow):
            if hasattr(method, 'is_step'):
                # Store basic info about each step
                self.nodes[name] = {
                    'name': name,
                    'type': 'task',
                    'out_funcs': set(),
                    'in_funcs': set()
                }
                
                # Get the next steps from the method
                next_steps = []
                if hasattr(method, 'next'):
                    next_steps = [method.next.__name__]
                
                # Store connections
                self.nodes[name]['out_funcs'].update(next_steps)
                for next_step in next_steps:
                    if next_step not in self.nodes:
                        self.nodes[next_step] = {
                            'name': next_step,
                            'type': 'task',
                            'out_funcs': set(),
                            'in_funcs': set()
                        }
                    self.nodes[next_step]['in_funcs'].add(name)

    def _traverse_graph(self):
        """Traverse the graph in topological order"""
        def traverse(node_name, seen):
            if node_name not in seen:
                self.sorted_nodes.append(node_name)
                seen.add(node_name)
                for next_node in self.nodes[node_name]['out_funcs']:
                    traverse(next_node, seen)

        # Start from 'start' node
        if 'start' in self.nodes:
            traverse('start', set())

    def get_dag_structure(self):
        """Return DAG structure in format suitable for visualization"""
        return {
            'nodes': {
                name: {
                    'type': 'start' if name == 'start' 
                           else 'end' if name == 'end' 
                           else 'task'
                } for name in self.nodes
            },
            'edges': [
                {'from': node_name, 'to': next_node}
                for node_name, node in self.nodes.items()
                for next_node in node['out_funcs']
            ]
        }

def parse_flow(flow_spec_class):
    """Parse a FlowSpec class into a DAG structure"""
    graph = SimpleFlowGraph(flow_spec_class)
    return graph.get_dag_structure()