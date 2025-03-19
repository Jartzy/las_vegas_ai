import React, { useState, useMemo } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, parseISO } from 'date-fns';
import { Event } from '../types/event';

interface EventCalendarProps {
  events: Event[];
}

const EventCalendar: React.FC<EventCalendarProps> = ({ events }) => {
  const [currentMonth, setCurrentMonth] = useState(new Date());

  // Determine the start and end dates for the current month.
  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });

  // Group events by day
  const eventsByDay = useMemo(() => {
    const eventMap: { [key: string]: Event[] } = {};

    events.forEach(event => {
      if (event.start_date) {
        // Parse ISO string to a Date object
        const eventDate = parseISO(event.start_date);
        // Use toDateString() as the key (e.g., "Mon Feb 14 2025")
        const dateKey = eventDate.toDateString();
        
        if (!eventMap[dateKey]) {
          eventMap[dateKey] = [];
        }
        eventMap[dateKey].push(event);
      }
    });

    return eventMap;
  }, [events]);

  // Render the calendar grid
  const renderCalendar = () => {
    return (
      <div className="grid grid-cols-7 gap-2">
        {/* Render days of the week headers */}
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="text-center font-bold text-gray-600">
            {day}
          </div>
        ))}
        {/* Render each day cell */}
        {daysInMonth.map(day => {
          const eventsOnDay = eventsByDay[day.toDateString()] || [];
          return (
            <div 
              key={day.toString()} 
              className={`p-2 border rounded-lg ${eventsOnDay.length > 0 ? 'bg-blue-50' : 'bg-white'}`}
            >
              <div className="text-right text-sm text-gray-700">
                {day.getDate()}
              </div>
              {eventsOnDay.length > 0 && (
                <div className="text-xs text-blue-600 mt-1">
                  {eventsOnDay.length} event{eventsOnDay.length > 1 ? 's' : ''}
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-xl p-6 shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <button 
          onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1, 1))}
          className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition"
        >
          ←
        </button>
        <h2 className="text-xl font-bold text-gray-800">
          {format(currentMonth, 'MMMM yyyy')}
        </h2>
        <button 
          onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1, 1))}
          className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition"
        >
          →
        </button>
      </div>
      {renderCalendar()}
    </div>
  );
};

export default EventCalendar;