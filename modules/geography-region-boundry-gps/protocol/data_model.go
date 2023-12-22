/* For license and copyright information please see the LEGAL file in the code repository */

package ggcrp

import (
	"memar/protocol"
	gc "org/modules/geography-coordinate/protocol"
	ggr "org/modules/geography-region/protocol"
)
// todo::
type DataModel interface {
	
	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
	
}

