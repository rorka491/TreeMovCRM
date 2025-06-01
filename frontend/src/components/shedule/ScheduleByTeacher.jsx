import React, { useState, useEffect } from 'react';

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

function ScheduleByTeacher() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/schedules/by-teachers/')
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

  const getDayOfWeek = (dateStr) => {
    const date = new Date(dateStr);
    const day = date.getDay();
    return day === 0 ? 6 : day - 1; 
  };

  const groupByLessonAndDay = (schedules) => {
    const result = {};
    schedules.forEach(s => {
      const lesson = s.lesson;
      const dayIndex = getDayOfWeek(s.date);
      if (!result[lesson]) result[lesson] = {};
      result[lesson][dayIndex] = s;
    });
    return result;
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;

  return (
    <div>
      {data.length === 0 && <div>Данные не найдены</div>}
      {data.map(({ teacher_id, schedules }) => {
        const grid = groupByLessonAndDay(schedules);
        const lessons = Object.keys(grid).sort((a, b) => a - b); // сортируем пары по номеру

        return (
          <div key={teacher_id} className="mb-12">
            <h2 className="text-xl font-semibold mb-4">Преподаватель: {teacher_id}</h2>
            <table className="table-auto border border-collapse w-full text-sm">
              <thead>
                <tr>
                  <th className="border px-2 py-1">Пара</th>
                  {DAYS.map((day, i) => (
                    <th key={i} className="border px-2 py-1">{day}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {lessons.map(lesson => (
                  <tr key={lesson}>
                    <td className="border px-2 py-1 font-medium">{lesson}</td>
                    {DAYS.map((_, dayIdx) => {
                      const cell = grid[lesson][dayIdx];
                      return (
                        <td key={dayIdx} className="border px-2 py-1 align-top">
                          {cell ? (
                            <>
                              <strong>{cell.title}</strong><br />
                              Время: {cell.start_time} — {cell.end_time}<br />
                              Ауд: {cell.classroom}
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

export default ScheduleByTeacher;
