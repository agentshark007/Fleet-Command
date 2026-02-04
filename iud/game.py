import math
import random
import sys

from core.camera import Camera
from core.enums import ExtendDirection
from core.explosion import Explosion
from core.projectile import *
from core.team import TeamType, random_teams
from core.unit import *
from core.utility import distance, pseudo_random_offset
from libraries import log
from libraries.pgiud import *

_unused_math_random = (math, random)


def initialize(self):
    check_flags(self)
    initialize_settings(self)
    initialize_state_variables(self)
    initialize_game_logic(self)
    initialize_layout(self)


def check_flags(self):
    log.info(f"flags: {sys.argv}")


def initialize_settings(self):
    self.water_state_speed = 5
    self.camera_zoom_speed = 0.5
    self.min_camera_scale = 0.3
    self.max_camera_scale = 3.0
    self.camera_move_speed = 50.0
    self.camera_move_friction = 0.9
    self.selection_marker_scale = 0.03
    self.selection_distance = 100
    self.autonomous_target_image_scale = 0.05
    self.water_image_scale = 0.3
    self.target_stop_distance = 100
    self.autonomous_forward_backward_angle_threshold = 45
    self.selection_marker_offset = 20
    self.projectile_limit = 1000


def initialize_state_variables(self):
    self.gui_scale = 1.0
    self.water_state = 0
    self.water_layer_offsets = [0.0, 0.0, 0.0, 0.0]
    self.camera = Camera(0.0, 0.0, 1.0)
    self.selected_units_ids = []


def initialize_game_logic(self):
    self.unit_types = [Battleship, Warship]
    team_count = 4
    self.teams = random_teams(team_count)
    self.units = {}
    for i in range(20):
        possible_units = [
            Battleship(
                team_index=random.randint(0, len(self.teams) - 1),
                position_x=random.uniform(-3000, 3000),
                position_y=random.uniform(-3000, 3000),
                direction=random.uniform(0, 360),
            ),
            Warship(
                team_index=random.randint(0, len(self.teams) - 1),
                position_x=random.uniform(-3000, 3000),
                position_y=random.uniform(-3000, 3000),
                direction=random.uniform(0, 360),
            ),
        ]
        unit = random.choice(possible_units)
        unit.unit_id = i
        self.units[i] = unit
    self.projectiles = {}
    self.next_projectile_id = 0
    self.explosions = {}
    self.next_explosion_id = 0
    try:
        unit_type_names = [t.__name__ for t in self.unit_types]
    except Exception:
        unit_type_names = [str(t) for t in self.unit_types]
    log.info(
        f"game_initialized teams={len(self.teams)} units={len(self.units)} unit_types={unit_type_names}"
    )


def initialize_layout(self):
    self.side_panel_color = Color(0, 0, 144, 150)
    self.middle_panel_color = Color(0, 0, 70, 150)
    self.panel_outline_color = Color(0, 0, 100, 50)
    self.title_text_color = Color(100, 100, 20)
    self.title_text_shadow_color = Color(20, 20, 50, 150)
    self.title_text_shadow_offset = 1
    self.panel_outline_thickness = 2
    self.side_panel_roundness = 15
    self.other_unit_filter = Color(150, 150, 150, 255)
    self.hover_unit_filter = Color(200, 200, 200, 255)
    self.selected_unit_filter = Color(255, 255, 255, 255)


def update(self):
    handle_camera_movement(self)
    handle_unit_selection(self)
    handle_unit_control(self)
    handle_unit_shooting(self)
    update_projectiles(self)
    detect_collisions(self)
    update_explosions(self)
    update_water(self)


def handle_unit_selection(self):
    mouse_world_pos = self.camera.deduce_v(self.mouse_pos)
    closest_unit_index = -1
    closest_unit_index_selectable = -1
    closest_distance = float("inf")
    closest_distance_selectable = float("inf")
    for unit_id, unit in self.units.items():
        dist = distance(unit.position, mouse_world_pos)
        if dist < closest_distance:
            closest_distance = dist
            closest_unit_index = unit_id
        if dist < closest_distance_selectable and dist < self.selection_distance:
            closest_distance_selectable = dist
            closest_unit_index_selectable = unit_id
    if self.mousedownprimary and (not self.mouse_primary_last_frame):
        if closest_unit_index_selectable != -1:
            team = self.teams[self.units[closest_unit_index_selectable].team_index]
            if team.type == TeamType.PLAYER:
                if self.keydown(Key.LSHIFT) or self.keydown(Key.RSHIFT):
                    if closest_unit_index_selectable not in self.selected_units_ids:
                        self.selected_units_ids.append(closest_unit_index_selectable)
                        log.info(
                            f"selection_added unit_id={closest_unit_index_selectable} selected_units={
                                self.selected_units_ids}"
                        )
                    else:
                        self.selected_units_ids.remove(closest_unit_index_selectable)
                        log.info(
                            f"selection_removed unit_id={closest_unit_index_selectable} selected_units={
                                self.selected_units_ids}"
                        )
                else:
                    self.selected_units_ids = [closest_unit_index_selectable]
                    log.info(f"selection_set selected_units={
                            self.selected_units_ids}")
            else:
                log.warn(
                    f"selection_non_player unit_id={closest_unit_index_selectable}"
                )
                self.selected_units_ids = []
        else:
            self.selected_units_ids = []
            log.info("selection_cleared")


def handle_unit_control(self):

    def manual_override():
        return any(
            [
                self.keydown(Key.W),
                self.keydown(Key.S),
                self.keydown(Key.A),
                self.keydown(Key.D),
            ]
        )

    for unit_id, unit in self.units.items():
        team = self.teams[unit.team_index]
        if team.type == TeamType.PLAYER:
            if unit_id in self.selected_units_ids:
                if self.mousedownsecondary:
                    mouse_world_x, mouse_world_y = self.camera.deduce(
                        self.mousex, self.mousey
                    )
                    unit.autonomous = True
                    unit.autonomous_target_x = mouse_world_x
                    unit.autonomous_target_y = mouse_world_y
                    log.info(f"autonomous_target_set unit_id={
                            getattr(
                                unit,
                                'unit_id',
                                unit_id)} target=({
                            unit.autonomous_target_x: .1f}, {
                            unit.autonomous_target_y: .1f})")
                if manual_override():
                    if getattr(unit, "autonomous", False):
                        log.info(f"manual_override unit_id={
                                getattr(
                                    unit,
                                    'unit_id',
                                    unit_id)} autonomous_disabled=True")
                    unit.autonomous = False
                acc = 0
                rot_acc = 0
                if self.keydown(Key.W):
                    acc += unit.speed
                if self.keydown(Key.S):
                    acc -= unit.speed
                if self.keydown(Key.A):
                    rot_acc -= unit.rotation_speed
                if self.keydown(Key.D):
                    rot_acc += unit.rotation_speed
                if acc != 0 or rot_acc != 0:
                    unit.autonomous = False
                    unit.acceleration = acc
                    unit.rotation_acceleration = rot_acc
        elif team.type == TeamType.AI:
            handle_ai_for_unit(self, unit_id, unit)
        else:
            log.warn(f"unknown_team_type unit_id={unit_id} team_index={
                    unit.team_index}")
        if getattr(unit, "autonomous", False):
            target_x, target_y = (unit.autonomous_target_x, unit.autonomous_target_y)
            dx = target_x - unit.position_x
            dy = target_y - unit.position_y
            distance_to_target = math.hypot(dx, dy)
            if distance_to_target < self.target_stop_distance:
                unit.autonomous = False
                continue
            angle_to_target = math.degrees(math.atan2(dx, dy))
            angle_diff = (angle_to_target - unit.direction + 360) % 360
            if angle_diff > 180:
                angle_diff -= 360
            if abs(angle_diff) < self.autonomous_forward_backward_angle_threshold:
                rotation_change = max(
                    -unit.rotation_speed, min(unit.rotation_speed, angle_diff)
                )
                acceleration = unit.speed
            else:
                rotation_change = max(
                    -unit.rotation_speed, min(unit.rotation_speed, angle_diff)
                )
                acceleration = -unit.speed
            acceleration = max(-unit.speed, min(unit.speed, acceleration))
            rotation_change = max(
                -unit.rotation_speed, min(unit.rotation_speed, rotation_change)
            )
            unit.acceleration = acceleration
            unit.rotation_acceleration = rotation_change
    for unit_id, unit in self.units.items():
        angle_rad = math.radians(unit.direction)
        unit.velocity_x += math.sin(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_y += math.cos(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_rotation += unit.rotation_acceleration * self.deltatime
        friction_factor = pow(unit.friction, self.deltatime * 60)
        unit.velocity_x *= friction_factor
        unit.velocity_y *= friction_factor
        rotation_friction_factor = pow(unit.rotation_friction, self.deltatime * 60)
        unit.velocity_rotation *= rotation_friction_factor
        unit.direction += unit.velocity_rotation * self.deltatime
        unit.position_x += unit.velocity_x * self.deltatime
        unit.position_y += unit.velocity_y * self.deltatime
        unit.acceleration = 0
        unit.rotation_acceleration = 0


def handle_unit_shooting(self):
    for unit_id, unit in self.units.items():
        team = self.teams[unit.team_index]
        if unit.cooldown_timer <= 0:
            if team.type == TeamType.PLAYER:
                if unit_id in self.selected_units_ids:
                    if self.keydown(Key.SPACE):
                        mouse_world_pos = self.camera.deduce(self.mousex, self.mousey)
                        direction = calculate_direction(
                            unit.position_x, unit.position_y, *mouse_world_pos
                        )
                        projectile = Missile(
                            x=unit.position_x,
                            y=unit.position_y,
                            direction=direction,
                            shooter_id=unit.team_index,
                        )
                        pid = self.next_projectile_id
                        self.projectiles[pid] = projectile
                        log.info(
                            f"projectile_created id={pid} type=Missile shooter_team={
                                unit.team_index} pos=({
                                unit.position_x: .1f}, {
                                unit.position_y: .1f}) dir={
                                direction: .1f}"
                        )
                        self.next_projectile_id += 1
                        unit.cooldown_timer = projectile.cooldown
            elif team.type == TeamType.AI:
                possible_target_units = []
                for sub_unit_id, sub_unit in self.units.items():
                    if sub_unit.team_index != unit.team_index:
                        possible_target_units.append((sub_unit_id, sub_unit))
                if len(possible_target_units) == 0:
                    continue
                target_unit = random.choice(possible_target_units)
                direction = calculate_direction(
                    unit.position_x,
                    unit.position_y,
                    target_unit[1].position_x,
                    target_unit[1].position_y,
                )
                projectile = Missile(
                    x=unit.position_x,
                    y=unit.position_y,
                    direction=direction,
                    shooter_id=unit.team_index,
                )
                pid = self.next_projectile_id
                self.projectiles[pid] = projectile
                log.info(f"projectile_created id={pid} type=Missile shooter_team={
                        unit.team_index} pos=({
                        unit.position_x: .1f}, {
                        unit.position_y: .1f}) dir={
                        direction: .1f}")
                self.next_projectile_id += 1
                unit.cooldown_timer = projectile.cooldown
            else:
                log.warn(f"unknown_team_type unit_id={unit_id} team_index={
                        unit.team_index}")
        else:
            unit.cooldown_timer -= self.deltatime


def handle_ai_for_unit(self, unit_id, unit):
    if not hasattr(unit, "ai_state"):
        unit.ai_state = "WANDER"
        unit.ai_state_timer = 0.0
        unit.ai_wander_target_x = unit.position_x
        unit.ai_wander_target_y = unit.position_y

    def nearest_enemy():
        best = (None, float("inf"))
        for sid, s in self.units.items():
            if s.team_index == unit.team_index:
                continue
            d = distance(unit.position_x, unit.position_y, s.position_x, s.position_y)
            if d < best[1]:
                best = (s, d)
        return best

    unit.ai_state_timer -= self.deltatime
    enemy, enemy_dist = nearest_enemy()
    low_health_threshold = unit.max_health * 0.35
    if unit.health <= low_health_threshold and enemy is not None:
        unit.ai_state = "EVADE"
        unit.ai_state_timer = max(unit.ai_state_timer, 1.0)
    elif enemy is not None and enemy_dist < 800:
        unit.ai_state = "CHASE"
    else:
        unit.ai_state = "WANDER"
    if unit.ai_state == "WANDER":
        if unit.ai_state_timer <= 0:
            radius = 600
            unit.ai_wander_target_x = unit.position_x + random.uniform(-radius, radius)
            unit.ai_wander_target_y = unit.position_y + random.uniform(-radius, radius)
            unit.ai_state_timer = random.uniform(2.0, 5.0)
        unit.autonomous = True
        unit.autonomous_target_x = unit.ai_wander_target_x
        unit.autonomous_target_y = unit.ai_wander_target_y
    elif unit.ai_state == "CHASE":
        if enemy is None:
            unit.ai_state = "WANDER"
        else:
            lead_seconds = min(1.0, enemy_dist / 600.0)
            predict_x = (
                enemy.position_x + getattr(enemy, "velocity_x", 0) * lead_seconds
            )
            predict_y = (
                enemy.position_y + getattr(enemy, "velocity_y", 0) * lead_seconds
            )
            unit.autonomous = True
            unit.autonomous_target_x = predict_x
            unit.autonomous_target_y = predict_y
            if enemy_dist < 200 and random.random() < 0.3:
                dx = unit.position_x - enemy.position_x
                dy = unit.position_y - enemy.position_y
                nd = math.hypot(dx, dy) or 1.0
                unit.autonomous_target_x = unit.position_x + dx / nd * 300
                unit.autonomous_target_y = unit.position_y + dy / nd * 300
    elif unit.ai_state == "EVADE":
        if enemy is None:
            unit.ai_state = "WANDER"
        else:
            dx = unit.position_x - enemy.position_x
            dy = unit.position_y - enemy.position_y
            nd = math.hypot(dx, dy) or 1.0
            flee_dist = 800
            unit.autonomous = True
            unit.autonomous_target_x = unit.position_x + dx / nd * flee_dist
            unit.autonomous_target_y = unit.position_y + dy / nd * flee_dist
            unit.ai_state_timer = max(unit.ai_state_timer, 1.0)
    if getattr(unit, "autonomous", False) and random.random() < 0.02:
        unit.autonomous_target_x += random.uniform(-20, 20)
        unit.autonomous_target_y += random.uniform(-20, 20)


def update_projectiles(self):
    if len(self.projectiles) > self.projectile_limit:
        excess = len(self.projectiles) - self.projectile_limit
        log.warn(f"too_many_projectiles limit={
                self.projectile_limit} actual={
                len(
                    self.projectiles)}")
        for _ in range(excess):
            if self.projectiles:
                del self.projectiles[list(self.projectiles.keys())[0]]
    for projectile in self.projectiles.values():
        projectile.update_fuel(self.deltatime)
    to_delete = []
    for projectile_id, projectile in self.projectiles.items():
        if projectile.fuel <= 0:
            to_delete.append(projectile_id)
    for delete in to_delete:
        del self.projectiles[delete]
    for projectile in self.projectiles.values():
        projectile.update(self.deltatime)


def detect_collisions(self):
    units_to_remove = set()
    projectiles_to_remove = set()
    for unit_id, unit in self.units.items():
        for projectile_id, projectile in self.projectiles.items():
            if unit.team_index == projectile.shooter_id:
                continue
            dist = distance(
                projectile.x, projectile.y, unit.position_x, unit.position_y
            )
            if dist < unit.collision_radius:
                unit.health -= projectile.damage
                projectiles_to_remove.add(projectile_id)
                log.info(
                    f"hit projectile_id={projectile_id} target_unit={unit_id} damage={
                        projectile.damage} unit_health_after={
                        unit.health}"
                )
                if unit.health <= 0:
                    units_to_remove.add(unit_id)
                    log.info(f"unit_destroyed unit_id={unit_id} team={
                            unit.team_index} pos=({
                            unit.position_x: .1f}, {
                            unit.position_y: .1f})")
                    create_explosion(self, unit.position_x, unit.position_y)
                break
    for unit_id_a, unit_a in self.units.items():
        for unit_id_b, unit_b in self.units.items():
            if unit_id_a >= unit_id_b:
                continue
            dist = distance(
                unit_a.position_x,
                unit_a.position_y,
                unit_b.position_x,
                unit_b.position_y,
            )
            min_dist = unit_a.collision_radius + unit_b.collision_radius
            if min_dist > dist > 0:
                units_to_remove.add(unit_id_a)
                units_to_remove.add(unit_id_b)
                log.info(
                    f"unit_collision unit_a={unit_id_a} unit_b={unit_id_b} contact_pos=({
                        (
                            unit_a.position_x +
                            unit_b.position_x) /
                        2: .1f}, {
                        (
                            unit_a.position_y +
                            unit_b.position_y) /
                        2: .1f})"
                )
                create_explosion(
                    self,
                    (unit_a.position_x + unit_b.position_x) / 2,
                    (unit_a.position_y + unit_b.position_y) / 2,
                )
    for uid in units_to_remove:
        if uid in self.units:
            del self.units[uid]
        else:
            log.warn(f"removal_warning missing_unit_id={uid}")
    for pid in projectiles_to_remove:
        if pid in self.projectiles:
            del self.projectiles[pid]
        else:
            log.warn(f"removal_warning missing_projectile_id={pid}")
    self.selected_units_ids = [
        uid for uid in self.selected_units_ids if uid in self.units
    ]


def create_explosion(self, x, y):
    eid = self.next_explosion_id
    self.explosions[eid] = Explosion(x, y)
    log.info(f"explosion_created id={eid} pos=({x: .1f}, {y: .1f})")
    self.next_explosion_id += 1


def update_explosions(self):
    explosions_to_remove = set()
    for explosion_id, explosion in self.explosions.items():
        explosion.current_frame += 1
        if explosion.current_frame >= explosion.frames:
            explosions_to_remove.add(explosion_id)
    for eid in explosions_to_remove:
        log.info(f"explosion_finished id={eid}")
        del self.explosions[eid]


def handle_camera_movement(self):
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)
    if not command_down:
        if self.keydown(Key.EQUALS) and (not self.plus_last_frame):
            old_scale = self.camera.scale
            attempted = old_scale + self.camera_zoom_speed
            self.camera.scale = min(
                [self.max_camera_scale, self.camera.scale + self.camera_zoom_speed]
            )
            if self.camera.scale != old_scale:
                log.info(f"camera_zoom old_scale={
                        old_scale: .2f} new_scale={
                        self.camera.scale: .2f}")
                if self.camera.scale != attempted:
                    log.warn(f"camera_zoom_clamped attempted={
                            attempted: .2f} clamped_to={
                            self.camera.scale: .2f}")
        elif self.keydown(Key.MINUS) and (not self.minus_last_frame):
            old_scale = self.camera.scale
            attempted = old_scale - self.camera_zoom_speed
            self.camera.scale = max(
                [self.min_camera_scale, self.camera.scale - self.camera_zoom_speed]
            )
            if self.camera.scale != old_scale:
                log.info(f"camera_zoom old_scale={
                        old_scale: .2f} new_scale={
                        self.camera.scale: .2f}")
                if self.camera.scale != attempted:
                    log.warn(f"camera_zoom_clamped attempted={
                            attempted: .2f} clamped_to={
                            self.camera.scale: .2f}")
    mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
    closest_unit_index = -1
    closest_unit_index_selectable = -1
    closest_distance = float("inf")
    closest_distance_selectable = float("inf")
    for unit_id, unit in self.units.items():
        dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
        if dist < closest_distance:
            closest_distance = dist
            closest_unit_index = unit_id
        if dist < closest_distance_selectable and dist < self.selection_distance:
            closest_distance_selectable = dist
            closest_unit_index_selectable = unit_id
    if closest_unit_index_selectable == -1:
        if self.mousedownprimary:
            self.camera.velocity_x = 0
            self.camera.velocity_y = 0
            self.camera.x += (self.mousex_last_frame - self.mousex) / self.camera.scale
            self.camera.y += (self.mousey_last_frame - self.mousey) / self.camera.scale
    factor_x = self.camera_move_speed / self.camera.scale * self.deltatime
    factor_y = self.camera_move_speed / self.camera.scale * self.deltatime
    if self.keydown(Key.LEFT):
        self.camera.velocity_x -= factor_x
    if self.keydown(Key.RIGHT):
        self.camera.velocity_x += factor_x
    if self.keydown(Key.UP):
        self.camera.velocity_y += factor_y
    if self.keydown(Key.DOWN):
        self.camera.velocity_y -= factor_y
    friction_factor = pow(self.camera_move_friction, self.deltatime * 60)
    self.camera.velocity_x *= friction_factor
    self.camera.velocity_y *= friction_factor
    self.camera.x += self.camera.velocity_x
    self.camera.y += self.camera.velocity_y


def update_water(self):
    self.water_state += self.water_state_speed * self.deltatime


def draw(self):
    if "--no-water" not in sys.argv:
        draw_water(self)
    draw_units(self)
    draw_explosions(self)
    draw_projectiles(self)
    if "--no-ui" not in sys.argv:
        draw_ui_panels(self)
    if "--fps" in sys.argv:
        draw_fps(self)


def draw_units(self):
    mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
    closest_unit_index = -1
    closest_unit_index_selectable = -1
    closest_distance = float("inf")
    closest_distance_selectable = float("inf")
    for unit_id, unit in self.units.items():
        dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
        if dist < closest_distance:
            closest_distance = dist
            closest_unit_index = unit_id
        if dist < closest_distance_selectable and dist < self.selection_distance:
            closest_distance_selectable = dist
            closest_unit_index_selectable = unit_id
    for unit_id, unit in self.units.items():
        screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
        if unit_id in self.selected_units_ids:
            self.draw_image(
                unit.image,
                pos=V(screen_x, screen_y),
                origin=Origin.CENTER,
                scalex=0.5 * self.camera.scale,
                scaley=0.5 * self.camera.scale,
                image_filter=self.selected_unit_filter,
                rotation=unit.direction,
            )
            if unit.autonomous:
                target_screen_x, target_screen_y = self.camera.project(
                    unit.autonomous_target_x, unit.autonomous_target_y
                )
                self.draw_image(
                    self.autonomous_target_image,
                    pos=V(target_screen_x, target_screen_y),
                    origin=Origin.CENTER,
                    scalex=self.autonomous_target_image_scale * self.camera.scale,
                    scaley=self.autonomous_target_image_scale * self.camera.scale,
                    rotation=0,
                )
        elif unit_id == closest_unit_index_selectable:
            self.draw_image(
                unit.image,
                pos=V(screen_x, screen_y),
                origin=Origin.CENTER,
                scalex=0.5 * self.camera.scale,
                scaley=0.5 * self.camera.scale,
                image_filter=self.hover_unit_filter,
                rotation=unit.direction,
            )
            if (
                self.teams[self.units[closest_unit_index_selectable].team_index].type
                == TeamType.PLAYER
            ):
                if unit.autonomous:
                    target_screen_x, target_screen_y = self.camera.project(
                        unit.autonomous_target_x, unit.autonomous_target_y
                    )
                    self.draw_image(
                        self.autonomous_target_image,
                        pos=V(target_screen_x, target_screen_y),
                        origin=Origin.CENTER,
                        scalex=self.autonomous_target_image_scale * self.camera.scale,
                        scaley=self.autonomous_target_image_scale * self.camera.scale,
                        rotation=0,
                    )
        else:
            self.draw_image(
                unit.image,
                pos=V(screen_x, screen_y),
                origin=Origin.CENTER,
                scalex=0.5 * self.camera.scale,
                scaley=0.5 * self.camera.scale,
                image_filter=self.other_unit_filter,
                rotation=unit.direction,
            )
    for unit_id, unit in self.units.items():
        screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
        self.draw_image(
            self.selection_marker_image,
            pos=V(
                screen_x, screen_y + self.selection_marker_offset * self.camera.scale
            ),
            origin=Origin.BOTTOM,
            scalex=self.selection_marker_scale * self.camera.scale,
            scaley=self.selection_marker_scale * self.camera.scale,
            image_filter=self.teams[unit.team_index].color,
            rotation=0,
        )


def draw_projectiles(self):
    for projectile in self.projectiles.values():
        screen_x, screen_y = self.camera.project(projectile.x, projectile.y)
        if self.projectile_images:
            img = self.projectile_images[
                random.randint(0, len(self.projectile_images) - 1)
            ]
            self.draw_image(
                img,
                pos=V(screen_x, screen_y),
                origin=Origin.CENTER,
                scalex=1 * self.camera.scale,
                scaley=1 * self.camera.scale,
                image_filter=Color(255, 255, 255, 255),
                rotation=90 - projectile.direction,
            )


def draw_explosions(self):
    for explosion_id, explosion in self.explosions.items():
        screen_x, screen_y = self.camera.project(explosion.x, explosion.y)
        img = explosion.image()
        self.draw_image(
            img,
            pos=V(screen_x, screen_y),
            origin=Origin.CENTER,
            scalex=explosion.scale * self.camera.scale,
            scaley=explosion.scale * self.camera.scale,
            image_filter=Color(255, 255, 255, 255),
            rotation=0,
        )


def draw_water(self):
    rotation_speed_0 = 0.03
    rotation_radius_0 = 7.0
    offset_x_0 = math.sin(self.water_state * rotation_speed_0) * rotation_radius_0
    offset_y_0 = math.cos(self.water_state * rotation_speed_0) * rotation_radius_0
    draw_water_layer(
        self,
        Color(30, 60, 170, 255),
        Color(20, 20, 20, 0),
        Color(51, 51, 51, 0),
        offset_x_0,
        offset_y_0,
        False,
    )
    wave_speed_1 = 1.5
    offset_x_1 = self.water_state * wave_speed_1
    offset_y_1 = -self.water_state * wave_speed_1 * 0.8
    draw_water_layer(
        self,
        Color(70, 170, 230, 120),
        Color(15, 15, 15, 0),
        Color(26, 26, 26, 0),
        offset_x_1,
        offset_y_1,
        True,
    )


def draw_water_layer(
    self,
    color: Color,
    color_fluctuation_strength: Color,
    color_fluctuation_speed: Color,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
    per_tile_offset: bool = False,
):
    final_color = Color(
        color.r
        + math.sin(color_fluctuation_speed.r * self.water_state)
        * color_fluctuation_strength.r,
        color.g
        + math.cos(color_fluctuation_speed.g * self.water_state)
        * color_fluctuation_strength.g,
        color.b
        + math.sin(color_fluctuation_speed.b * self.water_state)
        * color_fluctuation_strength.b,
        color.a
        + math.cos(color_fluctuation_speed.a * self.water_state)
        * color_fluctuation_strength.a,
    )
    draw_tiled_water(self, final_color, offset_x, offset_y, per_tile_offset)


def draw_tiled_water(
    self,
    filter_color: Color,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
    per_tile_offset: bool = False,
):
    offset = 5
    world_tile_w = (self.water_image.get_width() - offset) * self.water_image_scale
    world_tile_h = (self.water_image.get_height() - offset) * self.water_image_scale
    screen_w = self.screen_right - self.screen_left
    screen_h = self.screen_top - self.screen_bottom
    eff_cam_x = self.camera.x + offset_x
    eff_cam_y = self.camera.y + offset_y
    world_left = self.screen_left / self.camera.scale + eff_cam_x
    world_bottom = self.screen_bottom / self.camera.scale + eff_cam_y
    world_right = self.screen_right / self.camera.scale + eff_cam_x
    world_top = self.screen_top / self.camera.scale + eff_cam_y
    start_world_x = world_left - world_left % world_tile_w - world_tile_w
    start_world_y = world_bottom - world_bottom % world_tile_h - world_tile_h
    tile_w_screen = world_tile_w * self.camera.scale
    tile_h_screen = world_tile_h * self.camera.scale
    cols = int(math.ceil(screen_w / tile_w_screen)) + 3
    rows = int(math.ceil(screen_h / tile_h_screen)) + 3
    scalex = self.water_image_scale * self.camera.scale
    scaley = scalex
    for col in range(cols):
        for row in range(rows):
            wx = start_world_x + col * world_tile_w
            wy = start_world_y + row * world_tile_h
            tile_offset_x = 0
            tile_offset_y = 0
            if per_tile_offset:
                tile_offset_x = (pseudo_random_offset(wx, wy, seed=1) - 0.5) * 2
                tile_offset_y = (pseudo_random_offset(wx, wy, seed=2) - 0.5) * 2
            sx, sy = self.camera.project(
                wx - offset_x - tile_offset_x, wy - offset_y - tile_offset_y
            )
            self.draw_image(
                self.water_image,
                pos=V(sx, sy),
                origin=Origin.BOTTOMLEFT,
                scalex=scalex,
                scaley=scaley,
                image_filter=filter_color,
                rotation=0,
            )


def draw_ui_panels(self):
    self.fill_rounded_rect(
        V(self.screen_left, self.screen_bottom),
        V(
            self.extend(self.screen_left, 150, ExtendDirection.RIGHT),
            self.extend(self.screen_bottom, 100, ExtendDirection.UP),
        ),
        color=self.side_panel_color,
        outline_thickness=self.panel_outline_thickness * self.gui_scale,
        outline_color=self.panel_outline_color,
        topleft_roundness=0,
        topright_roundness=self.side_panel_roundness * self.gui_scale,
        bottomleft_roundness=0,
        bottomright_roundness=0,
    )
    self.fill_rounded_rect(
        V(
            self.extend(self.screen_right, 150, ExtendDirection.LEFT),
            self.screen_bottom,
        ),
        V(self.screen_right, self.extend(self.screen_bottom, 100, ExtendDirection.UP)),
        color=self.side_panel_color,
        outline_thickness=self.panel_outline_thickness * self.gui_scale,
        outline_color=self.panel_outline_color,
        topleft_roundness=self.side_panel_roundness * self.gui_scale,
        topright_roundness=0,
        bottomleft_roundness=0,
        bottomright_roundness=0,
    )
    self.fill_rect(
        V(
            self.extend(self.screen_left, 150, ExtendDirection.RIGHT),
            self.screen_bottom,
        ),
        V(
            self.extend(self.screen_right, 150, ExtendDirection.LEFT),
            self.extend(self.screen_bottom, 80, ExtendDirection.UP),
        ),
        color=self.middle_panel_color,
        outline_thickness=self.panel_outline_thickness * self.gui_scale,
        outline_color=self.panel_outline_color,
    )
    self.fill_rect(
        V(self.screen_left, self.screen_top),
        V(self.screen_right, self.extend(self.screen_top, 30, ExtendDirection.DOWN)),
        color=self.middle_panel_color,
        outline_thickness=self.panel_outline_thickness * self.gui_scale,
        outline_color=self.panel_outline_color,
    )
    shadow_offset = self.title_text_shadow_offset * self.gui_scale
    title_x = self.screen_center_x
    title_y = self.extend(self.screen_top, 15, ExtendDirection.DOWN)
    font = self.title_font.new_size(20 * self.gui_scale)
    origin = Origin.CENTER
    shadow_color = self.title_text_shadow_color
    self.draw_text(
        "Fleet Command",
        pos=V(title_x, title_y - shadow_offset),
        font=font,
        color=shadow_color,
        origin=origin,
    )
    self.draw_text(
        "Fleet Command",
        pos=V(title_x, title_y + shadow_offset),
        font=font,
        color=shadow_color,
        origin=origin,
    )
    self.draw_text(
        "Fleet Command",
        pos=V(title_x - shadow_offset, title_y),
        font=font,
        color=shadow_color,
        origin=origin,
    )
    self.draw_text(
        "Fleet Command",
        pos=V(title_x + shadow_offset, title_y),
        font=font,
        color=shadow_color,
        origin=origin,
    )
    self.draw_text(
        "Fleet Command",
        pos=V(title_x, title_y),
        font=font,
        color=self.title_text_color,
        origin=origin,
    )
    team_info_x = self.extend(self.screen_right, 5, ExtendDirection.LEFT)
    team_info_y = self.extend(self.screen_bottom, 100 + 20, ExtendDirection.UP)
    for i, team in enumerate(self.teams):
        self.draw_text(
            f"{team.name}: {team.type.name} - {len([u for u in self.units.values() if u.team_index == i])}",
            pos=V(team_info_x, team_info_y + i * (15 * self.gui_scale)),
            font=self.context_font.new_size(12 * self.gui_scale),
            color=team.color,
            origin=Origin.BOTTOMRIGHT,
        )
    if len(self.selected_units_ids) > 0:
        info_x = self.extend(self.screen_left, 10, ExtendDirection.RIGHT)
        info_y = self.extend(self.screen_bottom, 95, ExtendDirection.UP)
        line_height = 15 * self.gui_scale
        selected_count = len(self.selected_units_ids)

        def safe_average(values):
            return round(sum(values) / len(values)) if values else 0

        avg_direction = safe_average(
            [self.units[i].direction for i in self.selected_units_ids]
        )
        avg_health = safe_average(
            [self.units[i].health for i in self.selected_units_ids]
        )
        avg_max_health = safe_average(
            [self.units[i].max_health for i in self.selected_units_ids]
        )
        if selected_count == 1:
            lines = [
                f"Unit Info: {selected_count}",
                f"Direction: {avg_direction}°",
                f"Health: {avg_health}",
                f"Max Health: {avg_max_health}",
            ]
        else:
            lines = [
                f"Selected Units: {selected_count}",
                f"Average Direction: {avg_direction}°",
                f"Average Health: {avg_health}",
                f"Average Max Health: {avg_max_health}",
            ]
        for i, line in enumerate(lines):
            self.draw_text(
                line,
                pos=V(info_x, info_y - i * line_height),
                font=self.context_font.new_size(12 * self.gui_scale),
                color=Color(200, 200, 200),
                origin=Origin.TOPLEFT,
            )
    else:
        mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
        closest_unit_index = -1
        closest_unit_index_selectable = -1
        closest_distance = float("inf")
        closest_distance_selectable = float("inf")
        for unit_id, unit in self.units.items():
            dist = distance(
                unit.position_x, unit.position_y, mouse_world_x, mouse_world_y
            )
            if dist < closest_distance:
                closest_distance = dist
                closest_unit_index = unit_id
            if dist < closest_distance_selectable and dist < self.selection_distance:
                closest_distance_selectable = dist
                closest_unit_index_selectable = unit_id
        if closest_unit_index_selectable != -1:
            unit = self.units[closest_unit_index_selectable]
            info_x = self.extend(self.screen_left, 10, ExtendDirection.RIGHT)
            info_y = self.extend(self.screen_bottom, 95, ExtendDirection.UP)
            line_height = 15 * self.gui_scale
            lines = [
                f"Unit Info:",
                f"Team: {self.teams[unit.team_index].name}",
                f"Direction: {round(unit.direction)}°",
                f"Health: {round(unit.health)}",
                f"Max Health: {round(unit.max_health)}",
            ]
            for i, line in enumerate(lines):
                self.draw_text(
                    line,
                    pos=V(info_x, info_y - i * line_height),
                    font=self.context_font.new_size(12 * self.gui_scale),
                    color=Color(200, 200, 200),
                    origin=Origin.TOPLEFT,
                )


def draw_fps(self):
    fps = 0 if self.deltatime == 0 else round(1 / self.deltatime)
    self.draw_text(
        str(fps),
        pos=V(
            self.extend(self.screen_left, 7, ExtendDirection.RIGHT),
            self.extend(self.screen_top, 2, ExtendDirection.DOWN),
        ),
        font=self.title_font.new_size(20 * self.gui_scale),
        color=Color(100, 100, 100),
        origin=Origin.TOPLEFT,
    )
