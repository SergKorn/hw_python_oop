from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    RESULT: str = ("Тип тренировки: {training_type}; "
                   "Длительность: {duration:.3f} ч.; "
                   "Дистанция: {distance:.3f} км; "
                   "Ср. скорость: {speed:.3f} км/ч; "
                   "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        return self.RESULT.format(**asdict(self))


class Training:
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    RUN_COEFF_1: int = 18
    RUN_COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * self.MIN_IN_HOUR
        return (
            (self.RUN_COEFF_1 * self.get_mean_speed() - self.RUN_COEFF_2)
            * self.weight
            / self.M_IN_KM
            * time_in_minutes
        )


class SportsWalking(Training):
    WLK_COEFF_1: float = 0.035
    WLK_COEFF_2: float = 0.029
    WLK_COEFF_3: int = 2

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * self.MIN_IN_HOUR
        return (
            self.WLK_COEFF_1 * self.weight
            + (self.get_mean_speed() ** self.WLK_COEFF_3 // self.height)
            * self.WLK_COEFF_2
            * self.weight
        ) * time_in_minutes


class Swimming(Training):
    LEN_STEP: float = 1.38
    SWM_COEFF_1: float = 1.1
    SWM_COEFF_2: int = 2

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
            (self.get_mean_speed() + self.SWM_COEFF_1)
            * self.SWM_COEFF_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    dict: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    if dict.get(workout_type) is None:
        raise Exception("Ошибка!!! Активность не определена ;)")
    return dict[workout_type](*data)


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
