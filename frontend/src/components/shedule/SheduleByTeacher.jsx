
const ScheduleByTeacher = () => {
    const [schedules, setSchedules] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      fetch('/api/schedules/by_teacher/') 
        .then(res => res.json())
        .then(data => {
          setSchedules(data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }, []);
  
    if (loading) return <div>Загрузка...</div>;
    if (!schedules.length) return <div>Расписания не найдены</div>;
  
    return (
      <div>
        <h2>Все расписания по преподавателям</h2>
        {schedules.map(schedule => (
          <div key={schedule.id}>
            <strong>{schedule.title}</strong><br />
            Преподаватель: {schedule.teacher.name}<br />
            {schedule.start_time} — {schedule.end_time}
          </div>
        ))}
      </div>
    );
  };
  
  export default ScheduleByTeacher;