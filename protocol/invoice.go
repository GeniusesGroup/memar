/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type InvoiceUUID = protocol.UUID

// Also usually known as shopping-cart, ... in GUI part of applications

// New invoice service

// delete invoice service : This state indicates that the invoice has been deleted.
// You can only delete an invoice in the draft state and not in any other state.

// GetIDsByDateTime(time protocol.Time, offset, limit uint64) (ids [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
