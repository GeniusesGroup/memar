/* For license and copyright information please see LEGAL file in repository */

package protocol

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type (
	Service_Register_Request interface {
		QuiddityID() [16]byte
		DomainID() protocol.MediaTypeID
	}
)
