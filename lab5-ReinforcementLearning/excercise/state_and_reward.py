class StateAndReward:
    """State discretization and reward helpers for the Q-learning controller."""

    @staticmethod
    def get_state_angle(angle, vx, vy):
        """State discretization function for the angle controller."""

        # Exercise 1a: Discretize the angle and return a unique state.

                
        # 3 states base Recto, Izq, Der
        # solo dice a donde apunta
        # el angulo esta en punto decimal, 0.0 es hacia arriba 3.14 es apuntar hacia abajo
        # los numeros positivos es que esta mirando a la derecha
        # los negativos significa que hacia la izquierda, son espejo uno de otro

        if angle < -1.2:
            return "FarLeft"
        elif angle < -0.4:
            return "Left"
        elif angle < 0.4:
            return "Upward"
        elif angle < 1.2:
            return "Right"
        else:
            return "FarRight"


    @staticmethod
    def get_reward_angle(angle, vx, vy):
        """Reward function for the angle controller."""

        # Exercise 1b: Return a reward that favors an upright rocket.

        reward = 0

        if abs(angle) < 0.2:
            reward = 20
        elif abs(angle) < 0.6:
            reward = 10
        else:
            reward = 0

        return reward

    @staticmethod
    def get_state_hover(angle, vx, vy):
        """State discretization function for the full hover controller."""

        # Exercise 4a: Build a state from angle, vx, and vy.

        if angle < -1.2:
            angle_state = "FarLeft"
        elif angle < -0.4:
            angle_state = "Left"
        elif angle < 0.4:
            angle_state = "Upward"
        elif angle < 1.2:
            angle_state = "Right"
        else:
            angle_state = "FarRight"

        if vx < -50:
            vx_state = "FarLeftX"
        elif vx < -10:
            vx_state = "LeftX"
        elif vx < 10:
            vx_state = "BalancedX"
        elif vx < 50:
            vx_state = "RightX"
        else:
            vx_state = "FarRightX"

        if vy < -50:
            vy_state = "FarDownY"
        elif vy < -10:
            vy_state = "DownY"
        elif vy < 10:
            vy_state = "BalancedY"
        elif vy < 50:
            vy_state = "UpY"
        else:
            vy_state = "FarUpY"

        return [angle_state, vx_state, vy_state]

    @staticmethod
    def get_reward_hover(angle, vx, vy):
        """Reward function for the full hover controller."""

        # Exercise 4b: Return a reward for hovering.
        a = abs(angle)
        x = abs(vx)
        y = abs(vy)

        # Angle should dominate (prevent flip)
        if a < 0.15:
            r_angle = 40
        elif a < 0.30:
            r_angle = 25
        elif a < 0.7:
            r_angle = 10
        elif a < 1.1:
            r_angle = -10
        else:
            r_angle = -35

        # Horizontal stability
        if x < 4:
            r_vx = 12
        elif x < 12:
            r_vx = 6
        elif x < 25:
            r_vx = 0
        else:
            r_vx = -8

        # Vertical stability (hover => near zero, not just negative)
        if y < 4:
            r_vy = 12
        elif y < 12:
            r_vy = 6
        elif y < 25:
            r_vy = 0
        else:
            r_vy = -10

        return r_angle + r_vx + r_vy

    @staticmethod
    def discretize(value, nr_values, min_value, max_value):
        """Uniform discretization with explicit underflow and overflow bins.

        Returns an integer between 0 and nr_values - 1.

        If value is lower than min_value, 0 is returned. If value is higher
        than max_value, nr_values - 1 is returned. Otherwise a value between
        1 and nr_values - 2 is returned.
        """
        if nr_values < 2:
            return 0

        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * (nr_values - 2)) + 1

    @staticmethod
    def discretize2(value, nr_values, min_value, max_value):
        """Uniform discretization without separate inner edge bins.

        Returns an integer between 0 and nr_values - 1.
        """
        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * nr_values)
