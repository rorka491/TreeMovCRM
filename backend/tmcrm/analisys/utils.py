def _calculate_attendances_rate(presents: int, total: int) -> float:
    """
    Вычисляет процент посещаемости.

    Формула: (presents / total) * 100

    :param presents: Количество посещений
    :param total: Общее количество
    :return: Процент посещаемости от 0 до 100
    """
    if total == 0:
        return 0.0
    return round((presents / total) * 100, 2)

def _calcutate_student_success_rate(total_quantity_grades: int, sum_grades):

    if total_quantity_grades == 0:
        return 0.0
    return round(sum_grades / total_quantity_grades, 2)


def format_duration(td):
    # td может быть timedelta или None
    if not td:
        return "0:00"
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"{hours}:{minutes:02d}"
