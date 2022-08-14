from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESS: ClassVar[str] = ('Тип тренировки: {:.13};'
                           + ' Длительность: {:.3f} ч.;'
                           + ' Дистанция: {:.3f} км;'
                           + ' Ср. скорость: {:.3f} км/ч;'
                           + ' Потрачено ккал: {:.3f}.'
                           )
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESS.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определить get_spent_calories в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_1: ClassVar[int] = 18
    COEFF_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        t_in_min: float = self.duration * 60
        return (((self.COEFF_1 * self.get_mean_speed() - self.COEFF_2)
                * self.weight) / self.M_IN_KM * t_in_min)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: ClassVar[float] = 0.035
    COEFF_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        t_in_min: float = self.duration * 60
        return ((self.COEFF_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_2 * self.weight)
                * t_in_min
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_1: ClassVar[float] = 1.1
    COEFF_2: ClassVar[int] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_1)
                * self.COEFF_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    name_dict: dict[str, type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking
                                            }

    return name_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
