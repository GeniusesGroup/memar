/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type StaffTakeLeave interface {
	StaffID() StaffUUID             //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       //
	Type() StaffTakeLeave_Type      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type StaffTakeLeave_StorageServices interface {
	Save(dm StaffTakeLeave) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID StaffUUID, day utc.DayElapsed ,vo protocol.VersionOffset) (dm StaffTakeLeave, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_StaffIDs_BY_Day(day utc.DayElapsed, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FILTER_StaffIDs_BY_Type(t StaffTakeLeave_Type, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type StaffTakeLeave_Type uint8

const (
	StaffTakeLeave_Type_Unset StaffTakeLeave_Type = iota

	// usually four weeks of paid leave for each year of service. Shift-workers are entitled to five weeks of leave
	StaffTakeLeave_Type_Vacation
	StaffTakeLeave_Type_Travel
	StaffTakeLeave_Type_Rest
	StaffTakeLeave_Type_Study
	StaffTakeLeave_Type_Marriage
	StaffTakeLeave_Type_Casual

	StaffTakeLeave_Type_Sick // time off given by the company to allow employees to recover from an illness and take care of their health
	StaffTakeLeave_Type_Pain // Women period, ...
	StaffTakeLeave_Type_TemporaryDisability

	// Certain weather conditions make it extremely difficult, dangerous, and sometimes impossible for employees to travel to work.
	// Such conditions include heavy snow, a hurricane, or flash flooding.
	StaffTakeLeave_Type_AdverseWeather
	// or Time off in lieu (TOIL) for employees who have clocked in more hours than they were required to can be eligible for compensatory days off
	StaffTakeLeave_Type_Compensatory
	// Companies whose employees have served them for more than 3 years often
	// give these employees a sabbatical leave to reward them for their loyalty and hard work.
	StaffTakeLeave_Type_Sabbatical
	// Paid or unpaid time off gift
	StaffTakeLeave_Type_Gift
	// leave without pay
	StaffTakeLeave_Type_Unpaid

	StaffTakeLeave_Type_FamilyEvents
	// From taking care of the newborn to recovering from the delivery, maternity leave is an important time for new mothers.
	StaffTakeLeave_Type_Maternity
	// Paternity leave is granted to new fathers—  husbands or partners of a pregnant woman, surrogate parent,
	// or someone who adopted a child— to take care of their newborns without any worry.
	StaffTakeLeave_Type_Paternity
	// Losing a loved one is an unavoidable situation and in such events, employees take sudden leave.
	// Most HRs give their employees 3 to 7 days as bereavement leave, depending on the closeness of the relative.
	StaffTakeLeave_Type_Bereavement

	// Public holidays are days that are given as leave by the government.
	// Such holidays must be observed by every institution— schools, banks, government offices, and even private companies.
	StaffTakeLeave_Type_PublicHoliday
	// Christmas, Eid, Easter, Holi, Yom Kippur— your employee is sure to place importance on religious holidays that
	// they celebrate and would want the day off to spend time with their family and observe the festival.
	StaffTakeLeave_Type_ReligiousHolidays
	StaffTakeLeave_Type_JuryDuty
	StaffTakeLeave_Type_Protest
	StaffTakeLeave_Type_Volunteer
)
