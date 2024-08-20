/* For license and copyright information please see the LEGAL file in the code repository */

package arrrp

type Reason uint64

const (
	Reason_Unset Reason = 0 << iota
	Reason_LastChain

	// e.g. financial transaction request has sub request such as withdraw, deposit, reference, send notification, ...
	Reason_SubRequest
)
