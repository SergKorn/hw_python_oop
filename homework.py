class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность:{self.duration: .3f} ч.; '
            f'Дистанция:{self.distance: .3f} км; '
            f'Ср. скорость:{self.speed: .3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    run_coeff_1: int = 18
    run_coeff_2: int = 20
    min_in_hour: int = 60
    wlk_coeff_1: float = 0.035
    wlk_coeff_2: float = 0.029
    swm_coeff_1: float = 1.1
    swm_coeff_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * Training.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * Training.min_in_hour
        return ((Training.run_coeff_1 * self.get_mean_speed()
                - Training.run_coeff_2) * self.weight / Training.M_IN_KM
                * time_in_minutes)


class SportsWalking(Training):
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * Training.min_in_hour
        return (Training.wlk_coeff_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * Training.wlk_coeff_2 * self.weight) * time_in_minutes


class Swimming(Training):
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + Training.swm_coeff_1)
                * Training.swm_coeff_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    type_of_training = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking}
    return type_of_training[workout_type](*data)


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]), ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
