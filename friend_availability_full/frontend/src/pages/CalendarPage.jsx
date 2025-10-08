import React, { useEffect, useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import { summaryByDate } from '../api'

export default function CalendarPage(){
  const [events, setEvents] = useState([])
  useEffect(()=>{
    const start = '2025-10-01'
    const end = '2025-10-31'
    summaryByDate({start, end}).then(r=>{
      const ev = r.data.map(d => ({
        title: `${d.available_count}/${d.group_size}`,
        start: d.date,
        allDay: true,
        extendedProps: { percentage: d.percentage }
      }))
      setEvents(ev)
    }).catch(()=>{})
  }, [])
  return (
    <div>
      <div className="header">Friend Availability</div>
      <div className="container">
        <FullCalendar plugins={[dayGridPlugin]} initialView="dayGridMonth" events={events} />
      </div>
    </div>
  )
}
