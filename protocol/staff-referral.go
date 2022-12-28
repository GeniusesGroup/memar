/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type StaffReferral interface {
	StaffID() [16]byte          // staff domain
	ReferralID() [16]byte       // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
