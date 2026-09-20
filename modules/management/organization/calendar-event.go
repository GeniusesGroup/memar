/* For license and copyright information please see the LEGAL file in the code repository */

package label

// Task, production, batch, ... related domain:
// e.g. staff(123) ManualStart the specific shift(as a task type)
// what hours in a day this staff must active to provide services or do projects
//
// ExpectedTime
// Deadline
// ManualStart
// ManualTemporaryEnd
// ManualEnd
// Start
// TemporaryEnd
// End

// It can also be just preference, not real action event.
// staff-shift-preference
//
// product-duration (Can USE valid after 7 days from purchase time)
// product-reserve-validity (Can BUY 15 minutes from add to invoice time)
// product-timing (what hours in a day the service active to provide services)
// product-time-validity (flight departure and arrival time, concert start and end time, ...)
//
// notification serve or silent

// Invoice domain:::
// invoice-Item-reserve-time
// ActionTime

// Earth UTC day:::
// Holiday
// Anniversary
// UnexpectedClosure

// Quiddity level:::
//
// It will change the status of the thing to Expired after specified time.
// e.g. The `rule`(123) or `order`(456) or `form`(789) or `question`(147) MUST invalid after certain of time.
// Validity

// Form:::
// form-start-point (Also can use `Start` or `End` instead of introduce new label.)

// Network Connection
// LastUsage (Also can use `Start` or `End` instead of introduce new label.)

// User:::
// Birthday
// VerifiedDate // User got famous blue badge(tick) like instagram, twitter,...
