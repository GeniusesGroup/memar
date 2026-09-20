/* For license and copyright information please see the LEGAL file in the code repository */

package errs

import (
	er "memar/error"
)

// Errors
var (
	// User
	UserNotAllow     er.Error
	UserNotOwnRecord er.Error

	// Society
	NotAllowSociety er.Error
	DeniedSociety   er.Error

	// Router
	NotAllowRouter er.Error
	DeniedRouter   er.Error

	// Day
	DayNotAllow er.Error
	DayDenied   er.Error

	// Hour
	HourNotAllow er.Error
	HourDenied   er.Error

	// Service
	ServiceNotAllow er.Error
	ServiceDenied   er.Error

	// CRUD
	CrudNotAllow er.Error
	CRUDDenied   er.Error

	// Delegate
	NotAllowToDelegate    er.Error
	NotAllowToNotDelegate er.Error
)

func init() {
	// User
	ErrUserNotAllow.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=user-not-allow")
	ErrUserNotOwnRecord.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=user-not-own-record")

	// Society
	ErrNotAllowSociety.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=not-allow-society")
	ErrDeniedSociety.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=denied-society")

	// Router
	ErrNotAllowRouter.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=not-allow-router")
	ErrDeniedRouter.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=denied-router")

	// Day
	ErrDayNotAllow.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=day-not-allow")
	ErrDayDenied.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=day-denied")

	// Hour
	ErrHourNotAllow.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=hour-not-allow")
	ErrHourDenied.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=hour-denied")

	// Service
	ErrServiceNotAllow.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=service-not-allow")
	ErrServiceDenied.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=service-denied")

	// CRUD
	ErrCrudNotAllow.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=crud-not-allow")
	ErrCRUDDenied.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=crud-denied")

	// Delegate
	ErrNotAllowToDelegate.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=not-allow-to-delegate")
	ErrNotAllowToNotDelegate.Init("domain/memar.scm.geniuses.group; package=authorization; type=error; name=not-allow-to-not-delegate")
}
