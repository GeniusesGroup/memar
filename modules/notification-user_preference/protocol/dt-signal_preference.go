/* For license and copyright information please see the LEGAL file in the code repository */

package nupp

type SignalPreference uint8

const (
	SignalPreference_Unset SignalPreference = 0
	SignalPreference_App   SignalPreference = (1 << iota)
	SignalPreference_WebApp
	SignalPreference_Email
	SignalPreference_SMS
)
