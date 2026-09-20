/* For license and copyright information please see the LEGAL file in the code repository */

package errs

func init() {
	BadRequest.Init()
	ErrBadResponse.Init()
	ErrInternalError.Init()
	ErrProtocolHandler.Init()
	ErrGuestConnectionNotAllow.Init()
	ErrGuestConnectionMaxReached.Init()
	ErrNotStandardID.Init()
}
