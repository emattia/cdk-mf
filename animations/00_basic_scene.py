from manim import (
    Scene,
    RoundedRectangle,
    Circle,
    Text,
    VGroup,
    Arrow,
    Indicate,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)

# Define custom colors
METAFLOW_BLUE = "#6d9eeb"
LIGHT_PURPLE = '#D4D7EF'
MEDIUM_PURPLE = '#5460C0'
DARK_PURPLE = '#323A73'
LIGHT_YELLOW = '#FBEFD4'
MEDIUM_YELLOW = '#F0C054'
DARK_YELLOW = '#907332'

FONT_SIZE = 16

class CreateMetaflowEventLambda(Scene):
    def construct(self):
        # AWS Lambda Function box
        lambda_box = RoundedRectangle(corner_radius=0.2, width=3, height=1.5, color=LIGHT_PURPLE)
        lambda_text = Text("AWS Lambda Function", font_size=FONT_SIZE).move_to(lambda_box.get_center())
        lambda_group = VGroup(lambda_box, lambda_text)

        # Arrow indicating event publishing
        lambda_event_arrow = Arrow(start=lambda_group.get_right(), end=lambda_group.get_right() + RIGHT * 2, buff=0.1)
        lambda_event_label = Text("ArgoEvent.publish", font_size=FONT_SIZE).next_to(lambda_event_arrow, UP)
        lambda_event_group = VGroup(lambda_event_arrow, lambda_event_label)    

        # Metaflow Workflow box
        outerbounds_box = RoundedRectangle(corner_radius=0.2, width=4, height=2.5)
        outerbounds_text = Text("Outerbounds", font_size=FONT_SIZE * 1.5).move_to(outerbounds_box.get_top() + DOWN * 0.3)
        # outerbounds_group = VGroup(outerbounds_box, outerbounds_text)
        # outerbounds_group.next_to(event_arrow, RIGHT, buff=0.1)
        start_step = Circle(radius=0.3, color=MEDIUM_PURPLE).shift(DOWN * 0.5 + LEFT * 0.7)
        start_label = Text("start", font_size=FONT_SIZE).move_to(start_step.get_center())
        start_group = VGroup(start_step, start_label)

        end_step = Circle(radius=0.3, color=MEDIUM_PURPLE).shift(DOWN * 0.5 + RIGHT * 0.7)
        end_label = Text("end", font_size=FONT_SIZE).move_to(end_step.get_center())
        end_group = VGroup(end_step, end_label)

        step_arrow = Arrow(start=start_step.get_right(), end=end_step.get_left(), buff=0.1)

        # Grouping steps and placing them inside the Metaflow box
        steps_group = VGroup(start_group, step_arrow, end_group)
        steps_group.move_to(outerbounds_box.get_center() + DOWN * 0.5)
        outerbounds_group = VGroup(outerbounds_box, outerbounds_text, steps_group)

        # Group all elements together
        all_elements = VGroup(lambda_group, lambda_event_group, outerbounds_group)
        all_elements.arrange(RIGHT, buff=0.5)
        all_elements.move_to(self.camera.frame_center)

        # Adding all elements to the scene at once
        self.add(all_elements)

        # Sequentially highlighting each component
        self.wait(0.5)
        self.play(Indicate(lambda_group))
        self.wait(0.1)
        self.play(Indicate(lambda_event_arrow))
        self.wait(0.1)
        self.play(Indicate(start_group))
        self.wait(0.1)
        self.play(Indicate(end_group))
        self.wait(1)