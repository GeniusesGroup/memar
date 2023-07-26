/* For license and copyright information please see the LEGAL file in the code repository */

package pinp

import (
	"memar/protocol"

	np "org/modules/notification/protocol"
	op "org/modules/org/protocol"
	pp "org/modules/product/protocol"
	wp "org/modules/warehouse/protocol"
)

// ProductInventoryNotify indicate the domain record data fields.
type ProductInventoryNotify interface {
	NotificationID() np.NotificationUUID // user only == timeline-user_notification / staff == any notification group
	ProductID() pp.ProductUUID
	// LogicOnWASM() []byte // TODO:::
	OrgID() []op.OrgUUID
	WarehouseID() []wp.WarehouseUUID // user max 2, staff max 10
	AmountOperator() []protocol.ComparisonOperator
	Amount() []int64
	StockOperator() []protocol.ComparisonOperator
	Stock() []int64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/*
func UserLogic(warehouseID wp.WarehouseUUID, amount int64, stock int64) (notify bool) {
	const desireOrgIDs = []OrgUUID{}
	const warehouseIDs = []wp.WarehouseUUID{}
	if Amount >= 10 {
		return true
	}
	if Amount <= 500 {
		return true
	}
	return
}
*/
