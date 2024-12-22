/* For license and copyright information please see the LEGAL file in the code repository */

package ce_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	"memar/time/duration"
	time_p "memar/time/protocol"

	qs_p "org/modules/identity/quiddity-status/protocol"
	label_p "org/modules/knowledge/label/protocol"
	calendar_p "org/modules/organization/calendar/protocol"
)

// DataModel indicate the domain record data fields.
//
// Event is specific to each calendar, For any share purpose MUST use `task` domain.
//
// It will use to relate labels to repetitive day in each year.
// e.g. Friday is official holiday in `Iran` organization!
//
// It will use to relate labels to calendar seconds in each year.
// e.g. organization `start work` at 8a.m and `stop work` at 5p.m each day
// e.g. what hours in a day and days in weekday in utc time week the task active (end when indicate or related work will be done)
type DataModel interface {
	calendar_p.Field_CalendarID

	// Time can have repetitive epoch like `utc_epoch.DayInWeek` that indicate this event is repetitive too.
	// TODO::: embed or reference??
	time_p.Time
	// time_p.Field_Time

	label_p.Field_LabelID
	qs_p.Field_Status

	// TODO::: duration or two record as start and end??
	Duration() duration.Second // from Epoch()

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
