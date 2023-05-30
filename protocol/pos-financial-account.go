/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosFinancialAccount or pos operator is to supply a particular service.
type PosFinancialAccount interface {
	PosID() PosUUID                  //
	AccountID() FinancialAccountUUID //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}
