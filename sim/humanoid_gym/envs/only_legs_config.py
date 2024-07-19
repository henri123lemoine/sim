"""Defines the environment configuration for the Getting up task"""

from humanoid.envs.base.legged_robot_config import (  # type: ignore
    LeggedRobotCfg,
    LeggedRobotCfgPPO,
)

from sim.env import stompy_urdf_path
from sim.stompy_legs.joints import Stompy

NUM_JOINTS = len(Stompy.all_joints())  # 12


class OnlyLegsCfg(LeggedRobotCfg):
    """
    Configuration class for the Legs humanoid robot.
    """

    class env(LeggedRobotCfg.env):
        # change the observation dim

        frame_stack = 15
        c_frame_stack = 3
        num_single_obs = 11 + NUM_JOINTS * 3
        num_observations = int(frame_stack * num_single_obs)
        single_num_privileged_obs = 25 + NUM_JOINTS * 4
        num_privileged_obs = int(c_frame_stack * single_num_privileged_obs)
        num_actions = NUM_JOINTS
        num_envs = 4096
        episode_length_s = 24  # episode length in seconds
        use_ref_actions = False

    class safety:
        # safety factors
        pos_limit = 0.9
        vel_limit = 0.9
        torque_limit = 0.9

    class asset(LeggedRobotCfg.asset):
        file = str(stompy_urdf_path(legs_only=True))

        name = "stompy"

        foot_name = "_foot_1_rmd_x4_24_mock_1_inner_rmd_x4_24_1"
        knee_name = "_rmd_x8_90_mock_3_inner_rmd_x8_90_1"

        termination_height = 0.23
        default_feet_height = 0.0
        # terminate_after_contacts_on = ["link_leg_assembly_left_1_leg_part_1_2", "link_leg_assembly_right_1_leg_part_1_2"]

        penalize_contacts_on = []
        self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter

        collapse_fixed_joints = True

        flip_visual_attachments = False
        replace_cylinder_with_capsule = False
        fix_base_link = False

    class terrain(LeggedRobotCfg.terrain):
        mesh_type = "plane"
        # mesh_type = 'trimesh'
        curriculum = False
        # rough terrain only:
        measure_heights = False
        static_friction = 0.6
        dynamic_friction = 0.6
        terrain_length = 8.0
        terrain_width = 8.0
        num_rows = 10  # number of terrain rows (levels)
        num_cols = 10  # number of terrain cols (types)
        max_init_terrain_level = 10  # starting curriculum state
        # plane; obstacles; uniform; slope_up; slope_down, stair_up, stair_down
        terrain_proportions = [0.2, 0.2, 0.4, 0.1, 0.1, 0, 0]
        restitution = 0.0

    class noise:
        add_noise = True
        noise_level = 0.6  # scales other values

        class noise_scales:
            dof_pos = 0.05
            dof_vel = 0.5
            ang_vel = 0.1
            lin_vel = 0.05
            quat = 0.03
            height_measurements = 0.1

    class init_state(LeggedRobotCfg.init_state):
        pos = [0.0, 0.0, 0.72]

        default_joint_angles = {k: 0.0 for k in Stompy.all_joints()}

        default_positions = Stompy.default_standing()
        breakpoint()
        for joint in default_positions:
            default_joint_angles[joint] = default_positions[joint]

    class control(LeggedRobotCfg.control):
        # PD Drive parameters:
        # stiffness = {
        #     "shoulder": 200,
        #     "elbow": 200,
        #     "wrist": 200,
        #     "hand": 200,
        #     "torso": 200,
        #     "hip": 250,
        #     "ankle": 200,
        #     "knee": 350,
        # }

        # damping = {
        #     "shoulder": 10,
        #     "elbow": 10,
        #     "wrist": 10,
        #     "hand": 10,
        #     "torso": 10,
        #     "hip": 10,
        #     "ankle": 10,
        #     "knee": 10,
        # }
        stiffness = {
            "shoulder": 50,
            "elbow": 50,
            "wrist": 50,
            "hand": 50,
            "torso": 50,
            "hip": 50,
            "ankle": 50,
            "knee": 50,
        }
        damping = {
            "shoulder": 1.5,
            "elbow": 1.5,
            "wrist": 10,
            "hand": 10,
            "torso": 10,
            "hip": 1.5,
            "ankle": 1.5,
            "knee": 1.5,
        }
        action_scale = 0.25

        decimation = 10  # 100hz

    class sim(LeggedRobotCfg.sim):
        dt = 0.001  # 1000 Hz
        substeps = 1  # 2
        up_axis = 1  # 0 is y, 1 is z

        class physx(LeggedRobotCfg.sim.physx):
            num_threads = 10
            solver_type = 1 # 0: pgs, 1: tgs
            num_position_iterations = 4
            num_velocity_iterations = 1
            contact_offset = 0.0 # [m]
            rest_offset = 0.0  # -0.02  # [m]
            bounce_threshold_velocity = 0.1  # [m/s]
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2**23  # 2**24 -> needed for 8000 envs and more
            default_buffer_size_multiplier = 5
            # 0: never, 1: last sub-step, 2: all sub-steps (default=2)
            contact_collection = 2

    class domain_rand:
        randomize_friction = True
        friction_range = [0.1, 2.0]

        randomize_base_mass = True
        # added_mass_range = [-1.0, 1.0]
        added_mass_range = [-0.3, 0.3]
        push_robots = False
        push_interval_s = 4
        max_push_vel_xy = 0.2
        max_push_ang_vel = 0.4
        dynamic_randomization = 0.05

    class commands(LeggedRobotCfg.commands):
        # Vers: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        num_commands = 4
        resampling_time = 8.0  # time before command are changed[s]
        heading_command = True  # if true: compute ang vel command from heading error

        class ranges:
            lin_vel_x = [-0.3, 0.6]  # min max [m/s]
            lin_vel_y = [-0.3, 0.3]  # min max [m/s]
            ang_vel_yaw = [-0.3, 0.3]  # min max [rad/s]
            heading = [-3.14, 3.14]

    class rewards:
        # quite important to keep it right
        base_height_target = 0.72

        #distance between the knees and feet is2ac
        min_dist = 0.2
        max_dist = 0.5

        # put some settings here for LLM parameter tuning
        target_joint_pos_scale = 0.17  # rad
        target_feet_height = 0.06  # m
        cycle_time = 0.64  # sec
        # if true negative total rewards are clipped at zero (avoids early termination problems)
        only_positive_rewards = True
        # tracking reward = exp(error*sigma)
        tracking_sigma = 5
        max_contact_force = 400  # forces above this value are penalized

        class scales:
            # reference motion tracking
            # joint_pos = 1.6
            # feet_clearance = 1.0
            # feet_contact_number = 1.2
            # # gait
            # feet_air_time = 1.0
            # foot_slip = -0.05
            # feet_distance = 0.2
            # knee_distance = 0.2
            # contact
            # feet_contact_forces = -0.01
            # # vel tracking
            # tracking_lin_vel = 1.2
            # tracking_ang_vel = 1.1
            # vel_mismatch_exp = 0.5  # lin_z; ang x,y
            # low_speed = 0.2
            # track_vel_hard = 0.5

            # above this was removed for standing policy
            # base pos
            default_joint_pos = 1.0
            orientation = 1
            base_height = 1.0

            # energy
            action_smoothness = -0.002
            torques = -1e-5
            dof_vel = -5e-4
            dof_acc = -1e-7
            base_acc = 0.2
            collision = -1.0

    class normalization:
        class obs_scales:
            lin_vel = 2.0
            ang_vel = 1.0
            dof_pos = 1.0
            dof_vel = 0.05
            quat = 1.0
            height_measurements = 5.0

        clip_observations = 18.0
        clip_actions = 18.0

    class viewer:
        ref_env = 0
        pos = [4, -4, 2]
        lookat = [0, -2, 0]


class OnlyLegsCfgPPO(LeggedRobotCfgPPO):
    seed = 5
    runner_class_name = "OnPolicyRunner"  # DWLOnPolicyRunner

    class policy:
        init_noise_std = 1.0
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [768, 256, 128]

    class algorithm(LeggedRobotCfgPPO.algorithm):
        entropy_coef = 0.001
        learning_rate = 1e-5
        num_learning_epochs = 2
        gamma = 0.994
        lam = 0.9
        num_mini_batches = 4

    class runner:
        policy_class_name = "ActorCritic"
        algorithm_class_name = "PPO"
        num_steps_per_env = 60  # per iteration
        max_iterations = 10001  # number of policy updates

        # logging
        save_interval = 100  # check for potential saves every this many iterations
        experiment_name = "Legs"
        run_name = ""
        # load and resume
        resume = False
        load_run = -1  # -1 = last run
        checkpoint = -1  # -1 = last saved model
        resume_path = None  # updated from load_run and chkpt
