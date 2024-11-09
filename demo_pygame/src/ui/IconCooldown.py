import pygame

from demo_pygame.src.status.Attack import Attack
from demo_pygame.src.status.AttackFire import AttackFire
from demo_pygame.src.status.Heal import Heal


class IconCooldown:
    def __init__(self, game):
        self.game = game
        # Lấy các biểu tượng từ Game
        self.icons = {
            "attack": game.attack_icon,
            "attackfire": game.attackfire_icon,
            "heal": game.heal_icon
        }
        # Vị trí biểu tượng trên màn hình
        self.positions = {
            "attack": (50, game.screen.get_height() - 100),
            "attackfire": (110, game.screen.get_height() - 100),
            "heal": (170, game.screen.get_height() - 100)
        }

    def draw(self):
        """Vẽ biểu tượng và thời gian hồi chiêu dựa trên trạng thái cooldown."""
        cooldowns = {
            "attack": Attack,
            "attackfire": AttackFire,
            "heal": Heal
        }

        for skill, cooldown_class in cooldowns.items():
            icon_position = self.positions[skill]
            in_cooldown = not cooldown_class.can_create()
            if in_cooldown:
                # Tính thời gian hồi chiêu còn lại
                remaining_time = max(0, cooldown_class.cooldown - (pygame.time.get_ticks() - cooldown_class.last_used)) / 1000
                # Hiển thị biểu tượng mờ và thời gian
                self.game.screen.blit(self.dim_icon(self.icons[skill]), icon_position)
                self.draw_text(f"{remaining_time:.1f}s", icon_position[0] + 20, icon_position[1] + 70)
            else:
                # Hiển thị biểu tượng bình thường khi cooldown đã hoàn tất
                self.game.screen.blit(self.icons[skill], icon_position)

        pygame.display.update(pygame.Rect(50, self.game.screen.get_height() - 100, 200, 100))

    def dim_icon(self, icon):
        """Tạo biểu tượng mờ bằng cách điều chỉnh alpha."""
        dimmed_icon = icon.copy()
        dimmed_icon.fill((100, 100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
        return dimmed_icon

    def draw_text(self, text, x, y):
        """Vẽ text trên màn hình."""
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (x, y))
