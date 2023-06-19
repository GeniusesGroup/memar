/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	op "org/modules/org/protocol"
	pp "org/modules/product/protocol"
	pbp "org/modules/production-batch/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductBatchID() ProductBatchUUID           //
	ProductionBatchID() pbp.ProductionBatchUUID //
	ProductID() pp.ProductUUID                  //
	OwnerID() op.OrgUUID                        //
	SaveTime() protocol.Time                    //
	RequestID() urp.UserRequestUUID             //
}
