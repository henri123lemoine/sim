"""Defines a more Pythonic interface for specifying the joint names.

The best way to re-generate this snippet for a new robot is to use the
`sim/scripts/print_joints.py` script. This script will print out a hierarchical
tree of the various joint names in the robot.
"""

import textwrap
from abc import ABC
from typing import Dict, List, Tuple, Union


class Node(ABC):
    @classmethod
    def children(cls) -> List["Union[Node, str]"]:
        return [
            attr
            for attr in (getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__"))
            if isinstance(attr, (Node, str))
        ]

    @classmethod
    def joints(cls) -> List[str]:
        return [
            attr
            for attr in (getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__"))
            if isinstance(attr, str)
        ]

    @classmethod
    def joints_motors(cls) -> List[Tuple[str, str]]:
        joint_names: List[Tuple[str, str]] = []
        for attr in dir(cls):
            if not attr.startswith("__"):
                attr2 = getattr(cls, attr)
                if isinstance(attr2, str):
                    joint_names.append((attr, attr2))

        return joint_names

    @classmethod
    def all_joints(cls) -> List[str]:
        leaves = cls.joints()
        for child in cls.children():
            if isinstance(child, Node):
                leaves.extend(child.all_joints())
        return leaves

    def __str__(self) -> str:
        parts = [str(child) for child in self.children()]
        parts_str = textwrap.indent("\n" + "\n".join(parts), "  ")
        return f"[{self.__class__.__name__}]{parts_str}"


class LeftLeg(Node):
    hip_roll = "left hip roll"
    hip_yaw = "left hip yaw"
    hip_pitch = "left hip pitch"
    knee_pitch = "left knee pitch"
    ankle_pitch = "left ankle pitch"
    ankle_roll = "left ankle roll"


class RightLeg(Node):
    hip_roll = "right hip roll"
    hip_yaw = "right hip yaw"
    hip_pitch = "right hip pitch"
    knee_pitch = "right knee pitch"
    ankle_pitch = "right ankle pitch"
    ankle_roll = "right ankle roll"


class Legs(Node):
    left = LeftLeg()
    right = RightLeg()


class Stompy(Node):
    legs = Legs()

    @classmethod
    def default_positions(cls) -> Dict[str, float]:
        return {}

    @classmethod
    def default_standing(cls) -> Dict[str, float]:
        return {
            Stompy.legs.left.hip_pitch: -1.2,
            Stompy.legs.left.hip_yaw: 1.06,
            Stompy.legs.left.hip_roll: -0.03,
            Stompy.legs.left.knee_pitch: -1.27,
            Stompy.legs.left.ankle_pitch: 0.173,
            Stompy.legs.left.ankle_roll: 1.75,
            Stompy.legs.right.hip_pitch: 0.42,
            Stompy.legs.right.hip_yaw: -2.08,
            Stompy.legs.right.hip_roll: -1.65,
            Stompy.legs.right.knee_pitch: 3.3,
            Stompy.legs.right.ankle_pitch: 0.742,
            Stompy.legs.right.ankle_roll: 1.69,
        }

    @classmethod
    def default_limits(cls) -> Dict[str, Dict[str, float]]:
        return {
            Stompy.legs.left.hip_pitch: {
                "lower": -2.2,
                "upper": -0.2,
            },
            Stompy.legs.left.hip_yaw: {
                "lower": 0.6,
                "upper": 1.2,
            },
            Stompy.legs.left.hip_roll: {
                "lower": -1.03,
                "upper": 0.97,
            },
            Stompy.legs.left.knee_pitch: {
                "lower": -2.27,
                "upper": -0.27,
            },
            Stompy.legs.left.ankle_pitch: {
                "lower": -0.827,
                "upper": 1.173,
            },
            Stompy.legs.left.ankle_roll: {
                "lower": 0.75,
                "upper": 2.75,
            },
            Stompy.legs.right.hip_pitch: {
                "lower": -0.58,
                "upper": 1.42,
            },
            Stompy.legs.right.hip_yaw: {
                "lower": -2.2,
                "upper": -1.6,
            },
            Stompy.legs.right.hip_roll: {
                "lower": -2.65,
                "upper": -0.65,
            },
            Stompy.legs.right.knee_pitch: {
                "lower": 2.3,
                "upper": 4.3,
            },
            Stompy.legs.right.ankle_pitch: {
                "lower": -0.258,
                "upper": 1.742,
            },
            Stompy.legs.right.ankle_roll: {
                "lower": 0.69,
                "upper": 2.69,
            },
        }

    # p_gains
    @classmethod
    def stiffness(cls) -> Dict[str, float]:
        return {
            "hip pitch": 250,
            "hip yaw": 150,
            "hip roll": 150,
            "knee pitch": 150,
            "ankle pitch": 40,
            "ankle roll": 40,
        }

    # d_gains
    @classmethod
    def damping(cls) -> Dict[str, float]:
        return {
            "hip pitch": 10,
            "hip yaw": 7,
            "hip roll": 7,
            "knee pitch": 7,
            "ankle pitch": 1,
            "ankle roll": 0.3,
        }

    # pos_limits
    @classmethod
    def effort(cls) -> Dict[str, float]:
        return {
            "hip pitch": 150,
            "hip yaw": 90,
            "hip roll": 90,
            "knee pitch": 90,
            "ankle pitch": 24,
            "ankle roll": 24,
        }

    # vel_limits
    @classmethod
    def velocity(cls) -> Dict[str, float]:
        return {
            "hip pitch": 40,
            "hip yaw": 40,
            "hip roll": 40,
            "knee pitch": 40,
            "ankle pitch": 24,
            "ankle roll": 24,
        }

    @classmethod
    def friction(cls) -> Dict[str, float]:
        return {
            "hip pitch": 0.0,
            "hip yaw": 0.0,
            "hip roll": 0.0,
            "knee pitch": 0.0,
            "ankle pitch": 0.0,
            "ankle roll": 0.1,
        }


def print_joints() -> None:
    joints = Stompy.all_joints()
    assert len(joints) == len(set(joints)), "Duplicate joint names found!"
    print(Stompy())


if __name__ == "__main__":
    # python -m sim.stompy.joints
    print_joints()
