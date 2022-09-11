/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// StaffSalary is fixed negotiated salary that don't follow org||department||role salary rules.
type StaffSalary interface {
	StaffID() [16]byte                  //
	WeeklySalary() protocol.MoneyAmount //
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}
