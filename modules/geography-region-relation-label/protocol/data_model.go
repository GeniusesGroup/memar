/* For license and copyright information please see the LEGAL file in the code repository */

package ggrrop

import (
	"memar/protocol"
	ggrp "org/modules/geography-region/protocol"
	lp "org/modules/label/protocol"
)

type DataModel interface {

	GeographyRegionID() ggrp.GeographyRegionUUID
	LabelID() lp.LabelUUID
	
	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
