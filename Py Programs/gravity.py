import pathlib
import pygame as py
from pygame import Vector2
import math
import pygame_gui as pym

py.init()
screen = py.display.set_mode((1080, 720))
clock = py.time.Clock()

manager = pym.UIManager((1080, 720), 'theme.json')

start_button = pym.elements.UIButton(
    relative_rect=py.Rect((970, 670), (100, 40)),
    text='START',
    manager=manager,
    object_id="#style"
)

sidebar = pym.elements.UIPanel(
    relative_rect=py.Rect((0, 0), (200, 720)),
    manager=manager,
    object_id="#panel"
)

mass_label = pym.elements.UILabel(
    relative_rect=py.Rect((-15, 90), (200, 65)),
    text="Object Mass: (Tons)",
    manager=manager,
    container=sidebar,
)

mass_input = pym.elements.UITextEntryLine(
    relative_rect=py.Rect((10, 130), (180, 30)),
    manager=manager,
    container=sidebar,
    object_id="#style"
)

add_button = pym.elements.UIButton(
    relative_rect=py.Rect((10, 200), (180, 30)),
    text='Add Body',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

mass_input.set_text("1000")

body_images = {
    "Planet": py.image.load(pathlib.Path(__file__).parent / "images" / "planetHabitable.png").convert_alpha(),
    "Dusty Planet": py.image.load(pathlib.Path(__file__).parent / "images" / "dustyPlanet.png").convert_alpha(),
    "Gas Giant": py.image.load(pathlib.Path(__file__).parent / "images" / "gasGiant.png").convert_alpha(),
    "Ice Giant": py.image.load(pathlib.Path(__file__).parent / "images" / "iceGiant.png").convert_alpha(),
    "Ice Giant2": py.image.load(pathlib.Path(__file__).parent / "images" / "iceGiant2.png").convert_alpha(),
    "Rocky": py.image.load(pathlib.Path(__file__).parent / "images" / "rocky.png").convert_alpha(),
    "White Dwarf": py.image.load(pathlib.Path(__file__).parent / "images" / "whiteDwarf.png").convert_alpha(),
    "Red Dwarf": py.image.load(pathlib.Path(__file__).parent / "images" / "redDwarf.png").convert_alpha(),
    "Yellow Giant": py.image.load(pathlib.Path(__file__).parent / "images" / "yellowGiant.png").convert_alpha(),
    "Blue Giant": py.image.load(pathlib.Path(__file__).parent / "images" / "blueGiant.png").convert_alpha(),
    "Red Giant": py.image.load(pathlib.Path(__file__).parent / "images" / "redGiant.png").convert_alpha(),
    "Black Hole": py.image.load(pathlib.Path(__file__).parent / "images" / "blackHole.png").convert_alpha()
}

body_types = {
    "Planet": "planet",
    "Dusty Planet": "planet",
    "Gas Giant": "planet",
    "Ice Giant": "planet",
    "Ice Giant2": "planet",
    "Rocky": "planet",
    "White Dwarf": "star",
    "Red Dwarf": "star",
    "Yellow Giant": "star",
    "Blue Giant": "star",
    "Red Giant": "star",
    "Black Hole": "black hole"
}

STAR_MASS_THRESHOLDS = [
    (50000, "Blue Giant"),
    (20000, "Yellow Giant"),
    (10000, "Red Giant"),
    (5000,  "Red Dwarf"),
    (0,     "White Dwarf"),
]

PLANET_MASS_THRESHOLDS = [
    (8000, "Gas Giant"),
    (5000, "Ice Giant"),
    (3000, "Rocky"),
    (0,    "Planet"),
]

type_dropdown = pym.elements.UIDropDownMenu(
    options_list=list(body_types.keys()),
    starting_option='Planet',
    relative_rect=py.Rect((20, 50), (150, 30)),
    manager=manager,
    container=sidebar,
    object_id="#style"
)

snap_toggle = pym.elements.UIButton(
    relative_rect=py.Rect((10, 240), (180, 30)),
    text='Snap to Grid: ON',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

revert_button = pym.elements.UIButton(
    relative_rect=py.Rect((10, 280), (180, 30)),
    text='REVERT TO DESIGN',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

# Deletes everything
clear_button = pym.elements.UIButton(
    relative_rect=py.Rect((10, 320), (180, 30)),
    text='CLEAR ALL',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

selection_label = pym.elements.UILabel(
    relative_rect=py.Rect((10, 10), (180, 30)),
    text="Nothing Selected",
    manager=manager,
    container=sidebar
)

delete_button = pym.elements.UIButton(
    relative_rect=py.Rect((10, 360), (180, 30)),
    text='DELETE BODY',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

change_type_button = pym.elements.UIButton(
    relative_rect=py.Rect((10, 400), (180, 30)),
    text='APPLY NEW TYPE',
    manager=manager,
    container=sidebar,
    object_id="#style"
)

class HeavenlyBody:
    def __init__(self, coord, vel, mass, types, img):
        self.coord = coord
        self.vel = vel
        self.acc = Vector2(0,0)
        self.mass = mass
        self.scale = 1
        self.img = img
        self.trail = []
        self.type = types.lower()
        self.glow_radius = 0
        self.glow_surf = None
        self.start_coord = Vector2(self.coord)
        self.start_vel = Vector2(self.vel)

        self.scale = calc_scale(self.mass, self.type)

        base_w, base_h = self.img.get_size()
        new_w = int(base_w * self.scale * zoomMultiplier)
        new_h = int(base_h * self.scale * zoomMultiplier)
        self.radius = new_h
        self.current_img = py.transform.scale(self.img, (new_w, new_h))
        self.save_state()

    def save_state(self):
        self.start_coord = Vector2(self.coord)
        self.start_vel = Vector2(self.vel)

    def reset_to_start(self):
        self.coord = Vector2(self.start_coord)
        self.vel = Vector2(self.start_vel)
        self.acc = Vector2(0,0)
        self.trail = []

    def update_visuals(self, zoom):
        base_w, base_h = self.img.get_size()
        new_w = int(base_w * self.scale * zoom)
        new_h = int(base_h * self.scale * zoom)
        self.radius = new_h
        self.current_img = py.transform.scale(self.img, (new_w, new_h))

        if self.type == "star":
            glow_radius = int(new_w * 0.8)
            glow_surf = py.Surface((glow_radius * 2, glow_radius * 2), py.SRCALPHA)
            for r in range(glow_radius, 0, -2):
                alpha = int(255 * (1 - r / glow_radius))
                py.draw.circle(glow_surf, (255, 255, 255, alpha), (glow_radius, glow_radius), r)
            self.glow_surf = glow_surf
            self.glow_radius = glow_radius
        else:
            self.glow_surf = None
            self.glow_radius = 0

class Effect:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.timer = 0
        self.duration = 60  # frames

    def update(self):
        self.timer += 1

    def is_done(self):
        return self.timer >= self.duration

    def draw(self, surface):
        progress = self.timer / self.duration  # 0 to 1

        # Flash of light — fades out quickly
        if progress < 0.3:
            flash_alpha = int(255 * (1 - progress / 0.3))
            flash_radius = int(80 * progress / 0.3)
            flash_surf = py.Surface((flash_radius * 2, flash_radius * 2), py.SRCALPHA)
            py.draw.circle(flash_surf, (255, 220, 100, flash_alpha), (flash_radius, flash_radius), flash_radius)
            pos = world_to_screen(self.pos)
            surface.blit(flash_surf, (int(pos.x - flash_radius), int(pos.y - flash_radius)))

        # Expanding ring — grows and fades
        ring_radius = int(150 * progress)
        ring_alpha = int(255 * (1 - progress))
        if ring_radius > 0:
            ring_surf = py.Surface((ring_radius * 2, ring_radius * 2), py.SRCALPHA)
            py.draw.circle(ring_surf, (255, 100, 30, ring_alpha), (ring_radius, ring_radius), ring_radius, 3)
            pos = world_to_screen(self.pos)
            surface.blit(ring_surf, (int(pos.x - ring_radius), int(pos.y - ring_radius)))

effects = []

bodies = []

saved_bodies = []

G = 6
softening = 2
distanceMultiplier = 2
trailMaxThick = 5
SUPERNOVA_MASS_THRESHOLD = 30000
GRID_SIZE = 50
zoomMultiplier = 1
is_playing = False
selected_body: HeavenlyBody | None = None
body_select: HeavenlyBody | None = None
body_selection = False
dragging_velocity = False
snap_enabled = True
camera_offset = py.Vector2(0, 0)
universe_center = py.Vector2(540, 360)

#-------- Helper Functions --------

def screen_to_world(scr_pos):
    world = (py.Vector2(scr_pos) - universe_center - camera_offset) / zoomMultiplier + universe_center
    return world

def world_to_screen(world_pos):
    relative_pos = (world_pos - universe_center) * zoomMultiplier
    scr_pos = universe_center + relative_pos + camera_offset
    return scr_pos

def calc_scale(mass, body_type):
    scale = math.log(mass, 10) * 0.7
    if body_type == "black hole":
        scale *= 0.3
    elif body_type == "star":
        scale *= 1.7
    return scale

def pick_image_for_mass(mass, body_type):
    if body_type == "star":
        for threshold, name in STAR_MASS_THRESHOLDS:
            if mass >= threshold:
                return name, body_images[name]
    elif body_type == "planet":
        for threshold, name in PLANET_MASS_THRESHOLDS:
            if mass >= threshold:
                return name, body_images[name]
    return "Black Hole", body_images["Black Hole"]

#--------- Physics Calculation ---------

def update_physics():
    for B in bodies: B.acc = Vector2(0, 0)
    if is_playing:
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                b1 = bodies[i]
                b2 = bodies[j]

                direction = b2.coord - b1.coord
                dist = direction.length() * distanceMultiplier
                f = G * b1.mass * b2.mass / (dist ** 2 + softening ** 2)

                if direction.length_squared() > 0:
                    norm = direction.normalize()
                    a1 = (f / b1.mass) * norm  # b1 pulled toward b2
                    a2 = (f / b2.mass) * norm  # b2 pulled toward b1 (opposite)
                    b1.acc += a1
                    b2.acc -= a2

        for B in bodies:
            B.vel += B.acc
            B.coord += B.vel
            B.trail.append(Vector2(B.coord))
            if len(B.trail) > 100: B.trail.pop(0)

        if is_playing:
            handle_collisions()
            for effect in effects[:]:
                effect.update()
                if effect.is_done():
                    effects.remove(effect)

def handle_collisions():
    global body_select, body_selection

    to_remove = set()
    to_add = []

    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            if i in to_remove or j in to_remove:
                continue

            b1 = bodies[i]
            b2 = bodies[j]

            # Check if bodies are touching using world-space radius
            dist = (b1.coord - b2.coord).length()
            combined_radius = (b1.current_img.get_width() / 2 + b2.current_img.get_width() / 2) / zoomMultiplier
            if dist > combined_radius:
                continue

            # Collision detected — handle by type
            midpoint = (b1.coord + b2.coord) / 2
            combined_mass = b1.mass + b2.mass
            larger = b1 if b1.mass >= b2.mass else b2

            t1, t2 = b1.type, b2.type

            if t1 == "black hole" or t2 == "black hole":
                # Black hole absorbs everything
                bh = b1 if t1 == "black hole" else b2
                other = b2 if t1 == "black hole" else b1
                bh.mass += other.mass
                bh.scale = calc_scale(bh.mass, "black hole")
                bh.update_visuals(zoomMultiplier)
                to_remove.add(j if t1 == "black hole" else i)

            elif t1 == "star" and t2 == "star":
                to_remove.update([i, j])
                if combined_mass >= SUPERNOVA_MASS_THRESHOLD:
                    # Supernova — spawn black hole and effect
                    effects.append(Effect(midpoint))
                    bh_body = HeavenlyBody(midpoint, (b1.vel + b2.vel) / 2, combined_mass * 0.6, "black hole", body_images["Black Hole"])
                    to_add.append(bh_body)
                else:
                    # Merge into bigger star
                    _, new_img = pick_image_for_mass(combined_mass, "star")
                    merged = HeavenlyBody(larger.coord, (b1.vel + b2.vel) / 2, combined_mass, "star", new_img)
                    to_add.append(merged)

            elif t1 == "star" or t2 == "star":
                # Star absorbs planet
                star = b1 if t1 == "star" else b2
                star.mass += (b2.mass if t1 == "star" else b1.mass)
                star.scale = calc_scale(star.mass, "star")
                _, star.img = pick_image_for_mass(star.mass, "star")
                star.update_visuals(zoomMultiplier)
                to_remove.add(j if t1 == "star" else i)

            else:
                # Planet + planet merge
                _, new_img = pick_image_for_mass(combined_mass, "planet")
                merged = HeavenlyBody(larger.coord, (b1.vel + b2.vel) / 2, combined_mass, "planet", new_img)
                to_add.append(merged)
                to_remove.update([i, j])

            # Deselect if selected body was removed
            if body_select in [b1, b2] and (i in to_remove or j in to_remove):
                body_select = None
                body_selection = False
                body_selected()

    for idx in sorted(to_remove, reverse=True):
        bodies.pop(idx)
    for b in to_add:
        b.update_visuals(zoomMultiplier)
        bodies.append(b)

#---------- UI Overlay ----------

def draw_world():
    top_left = screen_to_world((0, 0))
    bottom_right = screen_to_world((1080, 720))

    start_x = int(top_left.x // GRID_SIZE) * GRID_SIZE
    end_x = int(bottom_right.x // GRID_SIZE) * GRID_SIZE
    start_y = int(top_left.y // GRID_SIZE) * GRID_SIZE
    end_y = int(bottom_right.y // GRID_SIZE) * GRID_SIZE

    for x in range(int(start_x), int(end_x) + GRID_SIZE, GRID_SIZE):
        p1 = world_to_screen(Vector2(x, start_y))
        p2 = world_to_screen(Vector2(x, end_y))
        py.draw.line(screen, (40, 40, 40), p1, p2, 1)

    for y in range(int(start_y), int(end_y) + GRID_SIZE, GRID_SIZE):
        p1 = world_to_screen(Vector2(start_x, y))
        p2 = world_to_screen(Vector2(end_x, y))
        py.draw.line(screen, (40, 40, 40), p1, p2, 1)

    if is_playing:
        for B in bodies:
            if len(B.trail) < 2: continue
            for j in range(1, len(B.trail)):
                perc = j / len(B.trail)
                alpha = int(perc * 255)
                thick = max(1, int(perc * trailMaxThick * zoomMultiplier))
                start = world_to_screen(B.trail[j - 1])
                end = world_to_screen(B.trail[j])
                py.draw.line(screen, (alpha, alpha, alpha), start, end, thick)

    for B in bodies:
        pos = world_to_screen(B.coord)
        w, h = B.current_img.get_size()
        if B.glow_surf:
            screen.blit(B.glow_surf, (int(pos.x - B.glow_radius), int(pos.y - B.glow_radius)))
        screen.blit(B.current_img, (int(pos.x - w / 2), int(pos.y - h / 2)))

    for effect in effects:
        effect.draw(screen)

def draw_ui_overlays():
    if not is_playing:
        for B in bodies:
            start = world_to_screen(B.coord)
            end = world_to_screen(B.coord + (B.vel * 10))
            py.draw.line(screen, (0, 255, 0), start, end, 5)
            py.draw.circle(screen, (0, 255, 0), (int(end.x), int(end.y)), 6)

    if body_selection and body_select:
        pos = world_to_screen(body_select.coord)
        rad = (body_select.current_img.get_width() / 2) + 10
        py.draw.circle(screen, (255, 255, 255), (int(pos.x), int(pos.y)), int(rad), 2)

#----------- Events -----------

def body_selected():
    if body_selection and body_select:
        mass_input.set_text(str(body_select.mass))
        selection_label.set_text(f"Selected: {body_select.type.upper()}")
        delete_button.show()
        change_type_button.show()
    else:
        selection_label.set_text("Nothing Selected")
        delete_button.hide()
        change_type_button.hide()

def handle_zoom(event):
    global zoomMultiplier, camera_offset

    zoom_center_screen = py.Vector2(py.mouse.get_pos())
    world_pos_before = screen_to_world(zoom_center_screen)

    zoomMultiplier += event.y * 0.05
    zoomMultiplier = max(0.05, min(zoomMultiplier, 20))

    for B in bodies:
        B.update_visuals(zoomMultiplier)

    new_screen_pos = world_to_screen(world_pos_before)
    camera_offset -= (new_screen_pos - zoom_center_screen)

def handle_drag(event):
    global body_select, body_selection, selected_body, dragging_velocity
    if not sidebar.rect.collidepoint(event.pos):
        mouse_pos = py.Vector2(event.pos)

        body_select = None
        body_selection = False
        body_selected()

        for B in bodies:
            screen_pos = world_to_screen(B.coord)
            arrow_tip = world_to_screen(B.coord + (B.vel * 10))

            if mouse_pos.distance_to(arrow_tip) < 15:
                body_select = B
                body_selection = True
                selected_body = B
                dragging_velocity = True
                body_selected()
                break
            elif mouse_pos.distance_to(screen_pos) < B.current_img.get_width() / 2:
                body_select = B
                body_selection = True
                selected_body = B
                dragging_velocity = False
                body_selected()
                break

def handle_release():
    global selected_body, dragging_velocity
    selected_body = None
    dragging_velocity = False

def start_sim():
    global is_playing, saved_bodies
    if not is_playing:
        for B in bodies:
            B.save_state()
        saved_bodies = [
            HeavenlyBody(Vector2(B.coord), Vector2(B.vel), B.mass, B.type, B.img)
            for B in bodies
        ]
    is_playing = not is_playing  # Toggle Play/Pause
    start_button.set_text("PAUSE" if is_playing else "START")

def add_body():
    selected_name = type_dropdown.selected_option
    img_to_use = body_images[selected_name[0]]

    try:
        new_mass = float(mass_input.get_text())
    except ValueError:
        new_mass = 1000

    new_body = HeavenlyBody(Vector2(540, 360), Vector2(0, 0), new_mass, body_types[selected_name[0]], img_to_use)
    new_body.save_state()
    new_body.update_visuals(zoomMultiplier)
    bodies.append(new_body)

def delete_body():
    global body_select
    if body_select in bodies:
        bodies.remove(body_select)
        body_select = None  # Deselect after deleting
        selection_label.set_text("Nothing Selected")
        print("Body deleted.")

def change_body_type():
    global body_select
    if body_select:
        new_name = type_dropdown.selected_option[0]
        body_select.img = body_images[new_name]
        body_select.type = body_types[new_name].lower()

        body_select.scale = calc_scale(body_select.mass, body_select.type)

        body_select.update_visuals(zoomMultiplier)
        selection_label.set_text(f"Selected: {body_select.type.upper()}")
        print(f"Changed type to {new_name}")

def revert_universe():
    global is_playing, camera_offset, zoomMultiplier, saved_bodies, body_select, body_selection, effects
    is_playing = False
    start_button.set_text("START")
    camera_offset = Vector2(0, 0)
    zoomMultiplier = 1

    bodies.clear()
    for B in saved_bodies:
        restored = HeavenlyBody(Vector2(B.coord), Vector2(B.vel), B.mass, B.type, B.img)
        restored.update_visuals(zoomMultiplier)
        bodies.append(restored)

    body_select = None
    body_selection = False
    body_selected()
    effects.clear()

    print("Universe reverted to last design.")

def clear_universe():
    global is_playing, selected_body, camera_offset, zoomMultiplier
    is_playing = False
    start_button.set_text("START")
    bodies.clear()
    selected_body = None
    camera_offset = Vector2(0, 0)
    zoomMultiplier = 1
    print("Universe cleared.")

def toggle_snap():
    global snap_enabled
    snap_enabled = not snap_enabled
    snap_toggle.set_text(f"Snap to Grid: {'ON' if snap_enabled else 'OFF'}")

def handle_buttons(event):
    if event.ui_element == start_button:
        start_sim()
    if event.ui_element == add_button:
        add_body()
    if event.ui_element == delete_button:
        delete_body()
    if event.ui_element == change_type_button:
        change_body_type()
    if event.ui_element == revert_button:
        revert_universe()
    if event.ui_element == clear_button:
        clear_universe()
    if event.ui_element == snap_toggle:
        toggle_snap()

def handle_text_input(event):
    global body_select
    if event.ui_element == mass_input and body_select:
        try:
            new_mass = float(mass_input.get_text())
            if new_mass > 0:
                body_select.mass = new_mass
                body_select.scale = calc_scale(body_select.mass, body_select.type)
                body_select.update_visuals(zoomMultiplier)
                print(f"Updated mass to {new_mass}")
        except ValueError:
            mass_input.set_text(str(body_select.mass))

def event_handler():
    for event in py.event.get():
        if event.type == py.QUIT:
            return False
        if event.type == py.MOUSEWHEEL:
            handle_zoom(event)
        if not is_playing:
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_drag(event)
            if event.type == py.MOUSEBUTTONUP:
                if event.button == 1:
                    handle_release()
        if event.type == pym.UI_BUTTON_PRESSED:
            handle_buttons(event)
        if event.type == pym.UI_TEXT_ENTRY_FINISHED:
            handle_text_input(event)
        manager.process_events(event)
    return True

def update_drag():
    global selected_body, dragging_velocity, snap_enabled
    if selected_body:
        mouse_world = screen_to_world(py.mouse.get_pos())
        if dragging_velocity:
            if snap_enabled:
                snapped_x = round(mouse_world.x / (GRID_SIZE / 2)) * (GRID_SIZE / 2)
                snapped_y = round(mouse_world.y / (GRID_SIZE / 2)) * (GRID_SIZE / 2)
                selected_body.vel = (Vector2(snapped_x, snapped_y) - selected_body.coord) / 10
            else:
                selected_body.vel = (mouse_world - selected_body.coord) / 10
        else:
            if snap_enabled:
                snapped_x = round(mouse_world.x / GRID_SIZE) * GRID_SIZE
                snapped_y = round(mouse_world.y / GRID_SIZE) * GRID_SIZE
                selected_body.coord = Vector2(snapped_x, snapped_y)
            else:
                selected_body.coord = mouse_world
            selected_body.trail = []
            selected_body.save_state()

def update_camera():
    global camera_offset
    mouse_buttons = py.mouse.get_pressed()
    if mouse_buttons[2]:
        rel = py.mouse.get_rel()
        camera_offset += Vector2(rel)
    else:
        py.mouse.get_rel()

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    running = event_handler()
    update_drag()
    update_camera()
    manager.update(time_delta)

    screen.fill((0, 0, 0))
    update_physics()
    draw_world()
    draw_ui_overlays()

    manager.draw_ui(screen)
    py.display.update()

py.quit()