import React, { useState, useEffect } from 'react';

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

function ScheduleByGroup() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/schedules/by-groups/')
      .then(res => {
        if (!res.ok) throw new Error('Ошибка сети');
        return res.json();
      })
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Возвращает индекс дня недели от 0 (Пн) до 6 (Вс)
  const getDayOfWeekIndex = (dateStr) => {
    const date = new Date(dateStr);
    const day = date.getDay(); // 0 — Вс, 1 — Пн, ...
    return day === 0 ? 6 : day - 1;
  };

  // Группируем расписание по урокам и дням недели
  const groupByLessonAndDay = (schedules) => {
    const grouped = {};
    schedules.forEach(item => {
      const lessonNum = item.lesson;
      const dayIdx = getDayOfWeekIndex(item.date);
      if (!grouped[lessonNum]) grouped[lessonNum] = {};
      grouped[lessonNum][dayIdx] = item;
    });
    return grouped;
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;
  if (!data.length) return <div>Данные не найдены</div>;

  return (
    <div>
      {data.map(({ group, schedules }) => {
        const grid = groupByLessonAndDay(schedules);
        const lessons = Object.keys(grid)
          .map(Number)
          .sort((a, b) => a - b);

        return (
          <div key={group} className="mb-12">
            <h2 className="text-xl font-semibold mb-4">Группа: {group}</h2>
            <table className="table-auto border border-collapse w-full text-sm">
              <thead>
                <tr>
                  <th className="border px-2 py-1">Пара</th>
                  {DAYS.map((day, idx) => (
                    <th key={idx} className="border px-2 py-1">{day}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {lessons.map(lesson => (
                  <tr key={lesson}>
                    <td className="border px-2 py-1 font-medium">{lesson}</td>
                    {DAYS.map((_, dayIdx) => {
                      const cell = grid[lesson]?.[dayIdx];

                      return (
                        <td key={dayIdx} className="border px-2 py-1 align-top">
                          {cell ? (
                            <>
                              <strong>{cell.title}</strong><br />
                              Преп: {cell.teacher?.employer?.surname} {cell.teacher?.employer?.name} {cell.teacher?.employer?.patronymic}<br />
                              {cell.classroom ? (
                              <>
                                Ауд: {typeof cell.classroom.title === 'string' ? cell.classroom.title : JSON.stringify(cell.classroom.title)}, 
                                этаж {cell.classroom.floor}, 
                                корпус {cell.classroom.building}
                              </>
                              ) : '-'}
                              Время: {cell.start_time} — {cell.end_time}
                            </>
                          ) : (
                            '-'
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      })}
    </div>
  );
}

export default ScheduleByGroup;
