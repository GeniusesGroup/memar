/* For license and copyright information please see LEGAL file in repository */

package protocol

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type (
	Service_Get_Request interface {
		QuiddityID() [16]byte
	}
	Service_Get_Response = QuiddityDomain
)
