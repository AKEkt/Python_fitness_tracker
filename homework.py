class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                + f'Длительность: {"%.3f" %self.duration} ч.; '
                + f'Дистанция: {"%.3f" %self.distance} км; '
                + f'Ср. скорость: {"%.3f" %self.speed} км/ч; '
                + f'Потрачено ккал: {"%.3f" %self.calories}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        coun = self.action
        step = self.LEN_STEP
        m_in_km = self.M_IN_KM
        return (coun * step) / m_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        d = self.get_distance()
        t = self.duration
        return d / t

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 18
        coeff_2 = 20
        s = self.get_mean_speed()
        w = self.weight
        m_in_km = self.M_IN_KM
        t_in_min = self.duration * 60
        return ((coeff_1 * s - coeff_2) * w) / m_in_km * t_in_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 0.035
        coeff_2 = 0.029
        w = self.weight
        s = self.get_mean_speed()
        h = self.height
        t_in_min = self.duration * 60
        return (coeff_1 * w + (s**2 // h) * coeff_2 * w) * t_in_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        d = self.length_pool
        c = self.count_pool
        m_in_km = self.M_IN_KM
        t = self.duration
        return (d * c) / m_in_km / t

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 1.1
        coeff_2 = 2
        s = self.get_mean_speed()
        w = self.weight
        return(s + coeff_1) * coeff_2 * w


def read_package(workout_type, data) -> Training:
    """Прочитать данные полученные от датчиков."""
    name_dict = {'SWM': Swimming,
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
