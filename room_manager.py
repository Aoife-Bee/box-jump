import pygame
from backgrounds import Sky
from camera import Camera

class RoomManager:
    def __init__(self, rooms, doors, tile_size, build_func):
        self.rooms = rooms
        self.doors = doors
        self.tile_size = tile_size
        self.build_func = build_func
        self.spawn_px = (0, 0)

        self.room_id = None
        self.layout = None

        self.solid_tiles = []
        self.hazard_tiles = []
        self.liquid_tiles = []

        self.tiles_to_draw = []
        self.camera = None
        self.sky = None

        self.level_width_px = 0
        self.level_height_px = 0

        self.door_cooldown = 0.0

    def door_rect_px(self, door_def):
        c, r, w, h = door_def["rect"]
        return pygame.Rect(
            c * self.tile_size,
            r * self.tile_size,
            w * self.tile_size,
            h * self.tile_size,
            )
    
    def find_door_hit(self, player_rect):
        for door_def in self.doors.get(self.room_id, []):
            if player_rect.colliderect(self.door_rect_px(door_def)):
                return door_def
        return None
    
    def find_door_by_id(self, room_id, door_id):
        for door_def in self.doors.get(room_id, []):
            if door_def["id"] == door_id:
                return door_def
        return None
    
    def _reset_player_motion(self, player):
        player.velocity_x = 0
        player.velocity_y = 0

        player.jump_buffer = 0.0
        player.coyote = 0.0
        player.jump_cut_used = False
        player.jump_held = False

        player.is_sprinting = False
        player.was_sprinting = False

        player.is_grounded = False
        player.is_jumping = False

    def set_player_pos(self, player, x, y):
        player.x = float(x)
        player.y = float(y)
        player.update_rect()

    def spawn_player_at_door(self, player, door_def):
        door_rect_px = self.door_rect_px(door_def)

        x = door_rect_px.centerx - player.width / 2
        y = door_rect_px.centery - player.height / 2

        pad = self.tile_size

        edge = door_def.get("edge") 

        if edge == "left":
            x = door_rect_px.right + pad
            y = door_rect_px.bottom - player.height
        elif edge == "right":
            x = door_rect_px.left - player.width - pad
            y = door_rect_px.bottom - player.height
        elif edge == "up":
            y = door_rect_px.bottom + pad
        elif edge == "down":
            y = door_rect_px.top - player.height - pad

        self.set_player_pos(player, x, y)

    
    def load_room(self, room_id, player, arrive_door_id=None):
        self.room_id = room_id
        room_data = self.rooms[room_id]
        self.layout = room_data["layout"]

        self.solid_tiles, self.hazard_tiles, self.liquid_tiles, player_spawn = self.build_func(
            self.layout, tile_size=self.tile_size
        )
        self.spawn_px = (int(player_spawn[0]), int(player_spawn[1]))
        self.tiles_to_draw = self.solid_tiles + self.liquid_tiles

        self.level_width_px = len(self.layout[0]) * self.tile_size
        self.level_height_px = len(self.layout) * self.tile_size
        self.camera = Camera(self.level_width_px, self.level_height_px)
        self.sky = Sky(room_data["sky_top"], room_data["sky_bottom"])

        if arrive_door_id is not None:
            door_def = self.find_door_by_id(room_id, arrive_door_id)
            if door_def is not None:
                self.spawn_player_at_door(player, door_def)
                self._reset_player_motion(player)

                if door_def.get("edge") == "down":
                    player.velocity_y = -player.jump_speed * 0.75
                    player.is_grounded = False
                    player.is_jumping = True

                self.spawn_px = (int(player.x), int(player.y))
                self.door_cooldown = 0.25
                return
            
        self.set_player_pos(player, player_spawn[0], player_spawn[1])
        self._reset_player_motion(player)
        self.door_cooldown = 0.25

    def update_transition(self, dt, player):
        self.door_cooldown = max(0.0, self.door_cooldown - dt)
        if self.door_cooldown > 0.0:
            return False
        
        hit = self.find_door_hit(player.rect)
        if hit is None:
            return False
        
        to_room_id, to_door_id = hit["to"]
        self.load_room(to_room_id, player, arrive_door_id=to_door_id)
        return True
    
    def respawn_player(self, player):
        player.health.respawn()

        x, y = self.spawn_px
        self.set_player_pos(player, x, y)

        self._reset_player_motion(player)
        player.iframes = 0.5
        self.door_cooldown = 0.25
