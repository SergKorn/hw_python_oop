from dataclasses import dataclass


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_RESULT_1 = "Тип тренировки: "
    TRAINING_RESULT_2 = "Длительность: "
    TRAINING_RESULT_3 = "Дистанция: "
    TRAINING_RESULT_4 = "Ср. скорость: "
    TRAINING_RESULT_5 = "Потрачено ккал: "

    def get_message(self):
        return (
            f"{self.TRAINING_RESULT_1}{self.training_type}; "
            f"{self.TRAINING_RESULT_2}{self.duration:.3f} ч.; "
            f"{self.TRAINING_RESULT_3}{self.distance:.3f} км; "
            f"{self.TRAINING_RESULT_4}{self.speed:.3f} км/ч; "
            f"{self.TRAINING_RESULT_5}{self.calories:.3f}."
        )


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    run_coeff_1: int = 18
    run_coeff_2: int = 20
    min_in_hour: int = 60

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * self.min_in_hour
        return (
            (self.run_coeff_1 * self.get_mean_speed() - self.run_coeff_2)
            * self.weight
            / self.M_IN_KM
            * time_in_minutes
        )


class SportsWalking(Training):
    wlk_coeff_1: float = 0.035
    wlk_coeff_2: float = 0.029
    wlk_coeff_3: int = 2
    min_in_hour: int = 60

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * self.min_in_hour
        return (
            self.wlk_coeff_1 * self.weight
            + (self.get_mean_speed() ** self.wlk_coeff_3 // self.height)
            * self.wlk_coeff_2
            * self.weight
        ) * time_in_minutes


class Swimming(Training):
    LEN_STEP: float = 1.38
    swm_coeff_1: float = 1.1
    swm_coeff_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.swm_coeff_1)
            * self.swm_coeff_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    type_of_training = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    redirection = type_of_training.get(workout_type)
    if redirection is None:
        raise print("Ошибка запроса! Тип тренировки не описан.")
    else:
        return redirection(*data)


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
