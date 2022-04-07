from dataclasses import dataclass
from typing import Dict, Type, Optional


@dataclass(init=True, repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        msg: str = (f'Тип тренировки: {self.training_type}; '
                    f'Длительность: {"%.3f" % self.duration} ч.; '
                    f'Дистанция: {"%.3f" % self.distance} км; '
                    f'Ср. скорость: {"%.3f" % self.speed} км/ч; '
                    f'Потрачено ккал: {"%.3f" % self.calories}.')

        return msg


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_HOUR: float = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MULT_1: float = 18
    CALORIES_MULT_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MULT_1 * self.get_mean_speed()
                - self.CALORIES_MULT_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MULT_1: float = 0.035
    CALORIES_MULT_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MULT_1 * self.weight
                + (
                    (self.get_mean_speed()**2 // self.height)
                    * self.CALORIES_MULT_2 * self.weight
                )
            )
            * self.duration * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MULT_1: float = 1.1
    CALORIES_MULT_2: float = 2
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

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MULT_1)
                * self.CALORIES_MULT_2 * self.weight)


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    trainings: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if trainings.get(workout_type) is None:
        print(f'Unknown training: {workout_type}')
        return None

    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Optional[Training] = read_package(workout_type, data)

        if training is None:
            print('Unable to run main function')
        else:
            main(training)
