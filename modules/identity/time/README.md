# Time
Event is specific to each calendar, For any share purpose MUST use `task` domain.

It will use to relate labels to repetitive day in each year.
e.g. Friday is official holiday in `Iran` organization!

It will use to relate labels to calendar seconds in each year.
e.g. organization `start work` at 8a.m and `stop work` at 5p.m each day
e.g. what hours in a day and days in weekday in utc time week the task active (end when indicate or related work will be done)

## time_p.Time

- It can also use as `time_p.Field_Time`
- Time can have repetitive epoch like `utc_epoch.DayInWeek` that indicate this event is repetitive too.

## Duration

duration or two record as start and end??
- It CAN use as any duration type such as `duration.Second` or `duration.Field_Second`
- `Duration() duration.Second // from Epoch()`
