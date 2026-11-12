# ADORA NANO

![ADORA NANO](assets/nano.png)

**URDF model of the ADORA NANO mobile manipulator** — a three-wheel driven base, a
pan-tilt camera head, and two identical 5-DOF arms, each with a two-blade soft gripper.

Published by the **[DORA community](https://doracc.com)** (DORA 中文社区).

## Contents

```
ADORA NANO/
├── README.md
├── assets/nano.png                  model render
├── urdf/adora_nano.urdf             robot description
└── meshes/
    ├── visual/<link>.stl            25 visual meshes, metres, link frame
    └── collision/<link>*_c*.stl     convex collision meshes
```

The URDF references its meshes with relative paths (`../meshes/...`). Keep `urdf/` and
`meshes/` as siblings when using or copying the model.

## Model

| | |
|---|---|
| Robot name | `adora_nano` |
| Links | 27 |
| Joints | 26 — 14 revolute, 3 continuous, 9 fixed |
| Movable DOF | 17 — 5 per arm, 2 head, 3 wheels, 2 gripper |
| Mass | 9.1972 kg |
| Units | metres, radians, kilograms, kg·m² (mesh files are in metres) |
| Base frame | `base_link`; **+X** forward, **+Y** left, **+Z** up |
| Ground | `z = −0.0343 m` |
| Wheels | radius 51.0 mm, width 38.5 mm, axles radial 120° apart |
| Head | pan ±150°, tilt −40°…+120° |
| Arms | `left_*` and `right_*`: identical 5-revolute chains |
| TCP | fixed `{side}_tool_mount` frame on each wrist |
| Actuation limits | effort 1.86 N·m, velocity 5.45 rad/s; ±150° on joints without a modelled mechanical stop |

### Joints

| Joint | Type | Range |
|---|---|---|
| `wheel_1_joint` … `wheel_3_joint` | continuous | continuous |
| `head_pan_joint` | revolute | ±150° |
| `head_tilt_joint` | revolute | −40°…+120° |
| `{left,right}_j1_yaw` | revolute | ±150° |
| `{left,right}_j2_pitch` | revolute | ±150° |
| `{left,right}_j3_pitch` | revolute | ±150° |
| `{left,right}_j4_pitch` | revolute | ±150° |
| `{left,right}_j5_roll` | revolute | ±150° |
| `{left,right}_j6_gripper` | revolute | −0.30…+0.877 rad |
| `{left,right}_shoulder_fixed`, `head_mount_fixed`, `{left,right}_tool_mount_fixed`, `{left,right}_wrist_cam_fixed`, `{left,right}_finger_a_fixed` | fixed | — |

### Gripper (`j6`)

Each arm has one driven jaw and one fixed jaw:

- `{side}_j6_gripper` rotates the moving jaw (`{side}_finger_b`) about the vertical tool
  axis through its mounting point;
- `q = 0` open, `q = +0.877 rad` (50.25°) closed, negative opens further;
- `{side}_finger_a` is the fixed jaw, attached to the wrist housing;
- blade-to-blade clearance: 46.9 mm open, 5.9 mm closed.

## Usage

**MuJoCo** (URDF import, fixed-joint children welded, `nq = nv = 17`):

```python
import mujoco
model = mujoco.MjModel.from_xml_path("urdf/adora_nano.urdf")
data = mujoco.MjData(model)
mujoco.mj_step(model, data)
```

**PyBullet**:

```python
import pybullet as p
robot = p.loadURDF("urdf/adora_nano.urdf", useFixedBase=False)   # 26 joints
```

**Any URDF viewer** (e.g. `urdf-viz`, Blender importers, Isaac, Webots): open
`urdf/adora_nano.urdf` with `meshes/` kept beside it.

## Notes

- Mass and inertia are nominal values; update them if measured values are available.
- Collision geometry is a convex decomposition, suitable for contact simulation but not
  for centimetre-accurate collision checking.
- Visual meshes are high fidelity (~1.0 M triangles); decimate them for lightweight viewers.
- Joint limits are actuator limits where no mechanical stop is modelled.

## Source & community

This model is maintained by the **DORA community** — the Chinese community of the
[DORA](https://github.com/dora-rs/dora) robot-development framework.

- Community site: [doracc.com](https://doracc.com)
- GitHub organization: [github.com/DoraCN](https://github.com/DoraCN)
- Framework: [github.com/dora-rs/dora](https://github.com/dora-rs/dora)
