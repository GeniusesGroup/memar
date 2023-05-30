/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type TableUUID = protocol.UUID

// LabelTable indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
// TODO::: base on label or status or both??
type LabelTable interface {
	TableID() TableUUID             //
	Labels() []LabelUUID            //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}
