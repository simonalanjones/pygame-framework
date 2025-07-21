class InvaderMovementHelper:

    def handle_invader_movement(self, container):
        invader = self.get_invader_at_current_index(container)
        if invader and invader.active:
            if not container.invaders_moving_down:
                invader.move_across(container.invader_direction)
            else:
                invader.move_down(container.invader_down_direction)


    def get_invader_at_current_index(self, container):
        all_sprites = container.sprites()
        if 0 <= container.current_invader_index < len(all_sprites):
            return all_sprites[container.current_invader_index]


    def update_current_invader_index(self, container):
        if container.current_invader_index < container.get_invader_count() - 1:
            container.current_invader_index += 1
        else:
            container.current_invader_index = 0
            self.update_movement_flags(container)


    def update_movement_flags(self, container):
        if container.invaders_moving_down:
            container.invaders_moving_down = False

            if self.has_reached_vertical_limit(container):
                container.event_manager.notify("invaders_landed")
                container.invaders_have_landed = True

        if self.has_reached_horizontal_limits(container):
            container.invader_direction *= -1
            container.invaders_moving_down = True


    def has_reached_vertical_limit(self, container) -> bool:
        return any(
            invader.rect.y + invader.rect.height >= container.screen_bottom_limit
            for invader in container.sprites()
        )


    def has_reached_horizontal_limits(self, container) -> bool:
        return any(
            (invader.rect.x >= container.screen_right_limit and container.invader_direction > 0) or
            (invader.rect.x <= container.screen_left_limit and container.invader_direction < 0)
            for invader in container.sprites()
        )
