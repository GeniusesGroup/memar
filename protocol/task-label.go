/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// TaskLabel indicate the domain record data fields.
type TaskLabel interface {
	TaskID() TaskUUID    //
	Label() LabelUUID    //
	Time() protocol.Time // Save time
}
