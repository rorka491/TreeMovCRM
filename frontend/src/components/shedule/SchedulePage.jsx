

const SchedulePage = ({ schedules }) => (
    <div>
      <h2>Занятия</h2>
      {schedules.map(schedule => (
        <div key={schedule.id}>
          <strong>{schedule.title}</strong><br />
          {schedule.start_time} — {schedule.end_time}
        </div>
      ))}
    </div>
  );
  
  export default SchedulePage;