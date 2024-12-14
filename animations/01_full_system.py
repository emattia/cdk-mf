from manim import (
    Scene,
    RoundedRectangle,
    Circle,
    Text,
    VGroup,
    Indicate,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    Arrow,
    Polygon,
    ArcBetweenPoints,
    CubicBezier,
    ORIGIN
)
import numpy as np
from parsers.flowspec import load_flow_from_file, parse_flow

# Define custom colors
LIGHT_PURPLE = '#D4D7EF'
MEDIUM_PURPLE = '#5460C0'

FONT_SIZE = 16

def create_bounding_box(content, padding=0.4, corner_radius=0.2, color=LIGHT_PURPLE):
    width = content.width + 2 * padding
    height = content.height + 2 * padding
    box = RoundedRectangle(
        corner_radius=corner_radius, width=width, height=height, color=color
    )
    box.move_to(content.get_center())
    return box

# def create_flow(name="FlowSpec"):
#     """
#     Creates a flow diagram with start and end circles connected by a smooth arrow.
#     """

#     # #  Usage:
#     # flow_file = '../flows/test_s3.py'
#     # TestS3Access = load_flow_from_file(flow_file)

#     # Create start circle and label
#     start_step = Circle(radius=0.3, color=MEDIUM_PURPLE)
#     start_label = Text("start", font_size=FONT_SIZE).move_to(start_step.get_center())
#     start_group = VGroup(start_step, start_label)

#     # Create end circle and label
#     end_step = Circle(radius=0.3, color=MEDIUM_PURPLE)
#     end_label = Text("end", font_size=FONT_SIZE).move_to(end_step.get_center())
#     end_group = VGroup(end_step, end_label)

#     # Arrange circles initially
#     circles_group = VGroup(start_group, end_group).arrange(RIGHT, buff=1.2)
    
#     # Create the connecting arrow using the same function
#     next_arrow, _ = draw_arrow_between(
#         start_group, 
#         end_group, 
#         control_scale=0.2  # Smaller scale for tighter curve
#     )
    
#     # Group the flow elements
#     flow_elements = VGroup(start_group, next_arrow, end_group)
    
#     # Add the flow name text
#     flow_text = Text(name, font_size=FONT_SIZE * 1.5)
#     flow_group = VGroup(flow_text, flow_elements).arrange(DOWN, buff=0.3)
    
#     # Create the bounding box
#     flow_box = create_bounding_box(flow_group, padding=0.5)
#     complete_flow_group = VGroup(flow_box, flow_group)

#     return start_group, end_group, next_arrow, complete_flow_group

def create_flow(name="FlowSpec", flow_file=None):
    """
    Creates a flow diagram based on a Metaflow DAG structure or default template.
    """
    if flow_file:
        # Load and parse the flow file
        flow_spec = load_flow_from_file(flow_file)
        dag_structure = parse_flow(flow_spec)
        
        # Create nodes dictionary
        nodes = {}
        for node_name, node_data in dag_structure['nodes'].items():
            # Create circle and label
            step = Circle(radius=0.3, color=MEDIUM_PURPLE)
            label = Text(node_name, font_size=FONT_SIZE).move_to(step.get_center())
            node_group = VGroup(step, label)
            nodes[node_name] = node_group
            
        # Arrange nodes horizontally with space between
        node_groups = VGroup(*nodes.values()).arrange(RIGHT, buff=1.2)
        
        # Create arrows between connected nodes
        arrows = []
        for edge in dag_structure['edges']:
            from_node = nodes[edge['from']]
            to_node = nodes[edge['to']]
            arrow, _ = draw_arrow_between(
                from_node,
                to_node,
                control_scale=0.2
            )
            arrows.append(arrow)
            
        # Group all elements
        flow_elements = VGroup(*nodes.values(), *arrows)
        
        # Add flow name and create bounding box
        flow_text = Text(name, font_size=FONT_SIZE * 1.5)
        flow_group = VGroup(flow_text, flow_elements).arrange(DOWN, buff=0.3)
        flow_box = create_bounding_box(flow_group, padding=0.5)
        complete_flow_group = VGroup(flow_box, flow_group)

        # Get the first and last nodes
        start_group = nodes['start']
        end_group = nodes['end']
        last_arrow = arrows[-1] if arrows else None
        
        return start_group, end_group, last_arrow, complete_flow_group

    else:
        # Default behavior - create simple start/end flow
        start_step = Circle(radius=0.3, color=MEDIUM_PURPLE)
        start_label = Text("start", font_size=FONT_SIZE).move_to(start_step.get_center())
        start_group = VGroup(start_step, start_label)

        end_step = Circle(radius=0.3, color=MEDIUM_PURPLE)
        end_label = Text("end", font_size=FONT_SIZE).move_to(end_step.get_center())
        end_group = VGroup(end_step, end_label)

        circles_group = VGroup(start_group, end_group).arrange(RIGHT, buff=1.2)
        
        next_arrow, _ = draw_arrow_between(
            start_group, 
            end_group, 
            control_scale=0.2
        )
        
        flow_elements = VGroup(start_group, next_arrow, end_group)
    
        # Add flow name and create bounding box
        flow_text = Text(name, font_size=FONT_SIZE * 1.5)
        flow_group = VGroup(flow_text, flow_elements).arrange(DOWN, buff=0.3)
        flow_box = create_bounding_box(flow_group, padding=0.5)
        complete_flow_group = VGroup(flow_box, flow_group)

        return start_group, end_group, next_arrow, complete_flow_group

        
def create_horizontal_tip(point, width=0.2, height=0.2):
    """Creates a horizontal arrow tip at the given point"""
    tip = Polygon(
        point + LEFT * width + UP * height/2,
        point + LEFT * width + DOWN * height/2,
        point,
        fill_opacity=1,
        color=LIGHT_PURPLE
    )
    return tip

def draw_arrow_between(source, target, control_scale=0.5):
    """
    Draws a smooth arrow between source and target using a CubicBezier curve
    with a horizontal tip.
    """
    # Get start and end points
    start_point = source.get_right() + RIGHT * 0.1
    end_point = target[0].get_left() + LEFT * 0.1
    tip = create_horizontal_tip(end_point)

    end_point += LEFT * tip.get_width()  # Adjust end point to include tip

    # Calculate the horizontal distance between points
    x_dist = end_point[0] - start_point[0]
    
    # Create control points that extend horizontally from start and end points
    control1 = start_point + RIGHT * (x_dist * control_scale)
    control2 = end_point + LEFT * (x_dist * control_scale)
    
    # Create the path
    path = CubicBezier(
        start_point,
        control1,
        control2,
        end_point
    )
    
    # Create a VGroup with the path and tip
    arrow = VGroup(path, tip)
    
    return arrow, path

def midpoint_and_angle_from_path(path, proportion):
    """
    Returns the midpoint and angle of the path at the given proportion.
    """
    midpoint = path.point_from_proportion(proportion)
    p1 = path.point_from_proportion(proportion - 0.01)  # slightly before
    p2 = path.point_from_proportion(proportion + 0.01)  # slightly after
    direction = (p2 - p1)
    angle = np.angle(complex(direction[0], direction[1]))
    return midpoint, angle

class CreateMetaflowEventLambda(Scene):
    def construct(self):
        # AWS Lambda Function label
        lambda_label = Text("AWS Lambda Function", font_size=FONT_SIZE)
        lambda_box = create_bounding_box(lambda_label, padding=0.3, color=LIGHT_PURPLE)
        lambda_group = VGroup(lambda_box, lambda_label)

        # Create three flows
        _, _, _, set_ids_group = create_flow("SetIDs", flow_file="../flows/set_ids.py")
        _, _, _, data_enrichment_group = create_flow("DataEnrichment")
        _, _, _, llm_flow_group = create_flow("Summarization")

        flows_group = VGroup(set_ids_group, data_enrichment_group, llm_flow_group).arrange(DOWN, buff=0.7)
        outerbounds_title = Text("Outerbounds", font_size=FONT_SIZE * 1.5)
        outerbounds_all = VGroup(outerbounds_title, flows_group).arrange(DOWN, buff=0.5)
        outerbounds_box = create_bounding_box(outerbounds_all, padding=0.5, color=LIGHT_PURPLE)
        outerbounds_group = VGroup(outerbounds_box, outerbounds_all)

        # Arrange lambda and outerbounds first
        all_elements = VGroup(lambda_group, outerbounds_group).arrange(RIGHT, buff=2.0)

        # Draw the arrow between lambda_box and llm_flow_group
        lambda_event_arrow, lambda_event_arrow_path = draw_arrow_between(lambda_box, llm_flow_group)

        # Position the label above the midpoint of the arrow using the path
        lambda_event_label = Text("ArgoEvent.publish", font_size=FONT_SIZE)
        
        midpoint, angle = midpoint_and_angle_from_path(lambda_event_arrow_path, 0.5)

        lambda_event_label.move_to(midpoint + UP * 0.5).rotate(angle)
        lambda_event_group = VGroup(lambda_event_arrow, lambda_event_label)

        # Rebuild all elements with the arrow now included
        all_elements = VGroup(lambda_group, lambda_event_group, outerbounds_group)

        # Scale down to fit on the screen
        all_elements.scale(0.75)
        all_elements.move_to(self.camera.frame_center)

        self.add(all_elements)

        # Sequential highlight
        self.wait(0.5)
        self.play(Indicate(lambda_group))
        self.wait(0.1)
        self.play(Indicate(lambda_event_group))
        self.wait(0.1)

        # Highlighting LLM flow elements
        llm_flow_start = llm_flow_group[1][1][0][0]  # start circle
        llm_flow_arrow_inner = llm_flow_group[1][1][1]     # arrow in the LLM flow
        llm_flow_end = llm_flow_group[1][1][2][0]    # end circle

        self.play(Indicate(llm_flow_start))
        self.wait(0.1)
        self.play(Indicate(llm_flow_arrow_inner))
        self.wait(0.1)
        self.play(Indicate(llm_flow_end))
        self.wait(1)