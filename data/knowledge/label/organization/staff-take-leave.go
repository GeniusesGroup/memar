/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
	// usually four weeks of paid leave for each year of service. Shift-workers are entitled to five weeks of leave
	Type_Vacation = iota
	Type_Travel
	Type_Rest
	// Type_Study
	Type_Marriage
	Type_Casual

	Type_Sick // time off given by the company to allow employees to recover from an illness and take care of their health
	Type_Pain // Women period, ...
	Type_TemporaryDisability

	// Certain weather conditions make it extremely difficult, dangerous, and sometimes impossible for employees to travel to work.
	// Such conditions include heavy snow, a hurricane, or flash flooding.
	Type_AdverseWeather
	// or Time off in lieu (TOIL) for employees who have clocked in more hours than they were required to can be eligible for compensatory days off
	Type_Compensatory
	// Companies whose employees have served them for more than 3 years often
	// give these employees a sabbatical leave to reward them for their loyalty and hard work.
	Type_Sabbatical
	// Paid or unpaid time off gift
	Type_Gift
	// leave without pay
	Type_Unpaid

	Type_FamilyEvents
	// From taking care of the newborn to recovering from the delivery, maternity leave is an important time for new mothers.
	Type_Maternity
	// Paternity leave is granted to new fathers—  husbands or partners of a pregnant woman, surrogate parent,
	// or someone who adopted a child— to take care of their newborns without any worry.
	Type_Paternity
	// Losing a loved one is an unavoidable situation and in such events, employees take sudden leave.
	// Most HRs give their employees 3 to 7 days as bereavement leave, depending on the closeness of the relative.
	Type_Bereavement

	// Public holidays are days that are given as leave by the government.
	// Such holidays must be observed by every institution— schools, banks, government offices, and even private companies.
	Type_PublicHoliday
	// Christmas, Eid, Easter, Holi, Yom Kippur— your employee is sure to place importance on religious holidays that
	// they celebrate and would want the day off to spend time with their family and observe the festival.
	Type_ReligiousHolidays
	Type_JuryDuty
	Type_Protest
	Type_Volunteer
)
